---
---

<style>

.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: var(--sans-serif);
  margin: 4rem 0 8rem; text-wrap: balance;
  text-align: center;
}

.hero h1 {
  margin: 2rem 0;
  max-width: none;
  font-size: 14vw;
  font-weight: 900;
  line-height: 1;
  background: linear-gradient(30deg, var(--theme-foreground-muted), currentColor);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero h2 {
  margin: 0;
  max-width: 34em;
  font-size: 20px;
  font-style: initial;
  font-weight: 500;
  line-height: 1.5;
  color: var(--theme-foreground-muted);
}

@media (min-width: 640px) {
  .hero h1 {
    font-size: 70px;
  }
}

</style>

<div class="hero">
  <h1>Datacenters dashboard</h1>
</div>

<h2>IDEAS</h2>
<ul>
    <li>compare current trajectories we know regarding ghg emissions targets of gafams and network operators, with sbti targets, and other targets ?</li>
    <li>graph representing the connections between norms and laws, relations beign "based on", "inspired from", "completes", ... with a color code for each norm that says if it comes from the industry, from the public , or a mixed origin</li>
    <li></li>
</ul>

<h2>Timeline of Datacenters regulations effects and obligations</h2>

<div class="card grid grid-cols-2">

```js
const height = view(
  Inputs.range([100, 500], {
    label: "Height",
    step: 10,
    value: 200,
  }),
);
const tickHeight = view(
  Inputs.range([10, 50], {
    label: "Tick Height",
    step: 5,
    value: 25,
  }),
);
const fontSizeInt = view(
  Inputs.range([8, 24], {
    label: "Font Size",
    step: 2,
    value: 16,
  }),
);
const lineLength = view(
  Inputs.range([10, 30], {
    label: "Maximum Character Length of Each Line",
    step: 1,
    value: 15,
  }),
);
const sideMargins = view(
  Inputs.range([10, 120], {
    label: "Left and Right Margins",
    step: 5,
    value: 70,
  }),
);

const data = await FileAttachment("regulations_deadlines.csv")
  .csv({ typed: true })
  .then((data) => {
    return data;
  });
console.log(data);

function wrapText(inputString, segmentLength) {
  const words = inputString.split(" ");
  let result = "";
  let currentLineLength = 0;
  let numberOfLines = 0;

  for (const word of words) {
    if (currentLineLength + word.length + 1 <= segmentLength) {
      // Add the word and a space to the current line
      result += (result === "" ? "" : " ") + word;
      currentLineLength += word.length + 1;
    } else {
      // Start a new line with the word
      result += "\n" + word;
      currentLineLength = word.length;
      numberOfLines++;
    }
  }

  // Count the last line
  if (result !== "") {
    numberOfLines++;
  }

  return {
    text: result,
    numberOfLines: numberOfLines,
  };
}
```

</div>

<div class="grid grid-cols-1">
  ${ resize((width) => Plot.plot({
    style: {
      fontSize: fontSizeInt + "px"
    },
    width,
    height,
    marginLeft: sideMargins,
    marginRight: sideMargins,
    x: { axis: null },
    y: { axis: null, domain: [-height / 2, height / 2] },
    marks: [
      Plot.ruleY([0]),
      Plot.ruleX(data, {
        x: "year",
        y: (d, i) => (i % 2 === 0 ? tickHeight : -tickHeight)
      }),
      Plot.dot(data, { x: "year", fill: "#fff", stroke: "#000" }),
      Plot.text(data, {
        x: "year",
        y: (d, i) => (i % 2 === 0 ? -fontSizeInt / 2 - 4 : fontSizeInt / 2 + 4),
        text: (d) => d.year.toString()
      }),
      Plot.text(data, {
        x: "year",
        y: (d, i) => d.composition.toString(),
        text: "composition"
      })
    ]
  }))}
</div>
