# Exam generator

*Exam Generator* is a small Python script that allows to create a test from a simple YAML file. The main features are:
- Generates both the question and the answers file 
- Can generate multiple versions of a test, by randomizing questions and the order of choices
- Supports questions with multiple correct answers

A `sample-exam.yaml` file shows how to write a test.
The script uses LaTeX and the exam package as backend, meaning that you'll need a LaTeX distribution installed on your laptop. 

## Setup:
NOTE: the following packages are from the OS, so cannot be included inside a virtual environment. 

<code> sudo apt-get update </code>

<code> sudo apt-get install texlive-latex-base </code>

<code> sudo apt-get install texlive-fonts-recommended </code>

<code> sudo apt-get install texlive-fonts-extra </code>


## Virtual environment creation 


1. Create a virtual environment

`python3 -m venv myenv`

Replace `myenv` with your desired environment name

2. Activate the virtual environment

* On Linux/macOS: `source myenv/bin/activate`
* On Windows: `myenv\Scripts\activate`



## Execution of the program

`python3 exam-generator.py sample-exam.yaml q1-t1 --versions 3`

## Deactivation of the virtual environment
`deactivate`
