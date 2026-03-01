# build_game_trees
Interactive web app for visualizing game theory concepts as game trees as extensive-form game trees — designed for students, researchers, and educators who want to explore simple game examples without writing a single line of code.

This project bridges the gap between Game Theory research and accessible UI design. Built for the PyGambit ecosystem, it allows researchers and students to dynamically construct, visualize, and analyze Extensive Form Games.

## Key Features
* **Form-Based Interface:** Define players, strategies, and payoffs through intuitive <u>dropdowns</u> and <u>input fields</u>.
* **Instant Rendering:** See your extensive-form game take shape in real-time.
* **Dynamic Tree Construction:** Real-time generation of N-player game trees across multiple decision stages.
* **Information Set Modeling:** Full support for simultaneous moves and imperfect information via automated information set grouping.
* **Recursive Visualization Engine:** Utilizes a custom recursive traversal algorithm to map PyGambit C-extensions to stable NetworkX graph structures, overcoming transient memory identity constraints.

## Techn Stack
* **Engine:** PyGambit (The industry-standard Game Theory library)
* **Structure:** NetworkX (Directed Acyclic Graph logic)
* **Rendering:** Matplotlib + Pydot (Hierarchical tree layouts)
* **Interface:** Streamlit + Custom CSS

## Motivation
This project grew out of a personal frustration: Students have no lightweight tool to experiment with simple extensive-form games. Coding trees from scratch in Python is a barrier for many learners.
Game Tree Visualizer is an attempt to make the exploratory, intuitive side of game theory more accessible using a very basic GUI
