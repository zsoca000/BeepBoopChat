# BeepBoopChat

This repository serves as the semester project for the Prompt Engineering (BMEVITMAV82) course at the Department of Telecommunications and Artificial Intelligence, Budapest University of Technology and Economics.

## Scope of the software

Our software is designed to bring a beginner radio amateur closer to practical broadcasting. This is done by creating a platform between Morse code and human speech.

Morse code would not be sufficiently efficient without proper word abbreviations. Coding full words is too long and complicated, so radio operators use a language full of common abbreviations that is completely nonsense to an average human.

## Detailed description

Our software first decodes Morse code audio file input, which becomes radio amateur text. This creates an extended language that is easy to understand thanks to an LLM (Large Language Model). The user can then respond in a similar regular language, which is also translated by an LLM back into radio amateur text, which is converted by an algorithm into a Morse audio file.


![Application Flowchart](doc/flowchart.png)

Our software includes several features to further simplify its use, such as the possibility to predefine mandatory parameters, which will be included in the response message.

It was a pleasure to create this software, which was very challenging. It was fun to integrate LLM into a code and see it work.

## Installation

To install the required dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## Running the Application

To run the application, execute the following command:

```bash
python main.py
```

© 2025 Gábor Kreinicker and Zsolt Szász