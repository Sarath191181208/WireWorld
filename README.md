# Wire World

Wireworld is a cellular automaton first proposed by **Brian Silverman** in 1987, as part of his program Phantom Fish Tank. It subsequently became more widely known as a result of an article in the **"Computer Recreations"** column of Scientific American. Wireworld is particularly suited to simulating transistors, and Wireworld is Turing-complete i.e It can simulate a turning machine.

Read more on Wikipedia : https://en.wikipedia.org/wiki/Wireworld

# Description

A Wireworld cell can be in one of four different states :

- empty <div style="color: black;">black</div>
- electron head <div style="color: blue;">blue</div>
- electron tail <div style="color: red;">red</div>
- conductor <div style="color: yellow;">yellow</div>.

As in all cellular automata, time proceeds in discrete steps called generations (sometimes "gens" or "ticks"). Cells behave as follows:

- empty → empty,
- electron head → electron tail,
- electron tail → conductor,
- conductor → electron head if exactly one or two of the neighbouring cells are electron heads, otherwise remains conductor.

## Demo

![Image](https://github.com/Sarath191181208/WireWorld/blob/master/images/Screenshot.png)

## Features

- A **Pan button** to pan board.
- A **Clear button** to totally clear the board.
- A **Start button** to toggle the visualization.
- A **Red button** to toggle the visbility of red color.
- **Save/Load** Features.
- **Zoom** Feature.
- Different **electronic components** like Diodes, Or Gate, And Gate etc...

## Run Locally

Clone the project

```bash
  git clone https://github.com/Sarath191181208/WireWorld.git
```

Go to the project directory

```bash
  cd ./WireWorld
```

Install dependencies

```bash
  pip3 install -r requirements.txt
```

Run the project Locally

```bash
  python main.py
```

## References

Wikipedia : https://en.wikipedia.org/wiki/Wireworld

Wikipedia : https://en.wikipedia.org/wiki/Cyclic_cellular_automaton

## Usage

- **Right click to delete the block.**
- Left click to insert.
- All the buttons are explained in features section.

## Hot keys

- SPACE : Toggle visualization
- C : Clear
- S : Save
- O : Load
- R : Toggle Red
- P : Toggle Pan

## Requirements

- python `Make sure to add to path`
- pygame `pip install pygame`
- pygame_gui `pip install pygame_gui`
