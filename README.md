# Exam generator

*Exam Generator* is a small Python script that allows to create a test from a simple YAML file. The main features are:
- Generates both the question and the answers file 
- Can generate multiple versions of a test, by randomizing questions and the order of choices
- Supports questions with multiple correct answers

A `sample-exam.yaml` file shows how to write a test.
The script uses LaTeX and the exam package as backend, meaning that you'll need a LaTeX distribution installed on your laptop. 