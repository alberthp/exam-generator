#!/usr/bin/env python

import sys
import yaml 
import random
import subprocess
import argparse

def read_yaml(fname):
    with open(fname, 'r') as f:
        content = yaml.safe_load(f.read())
        return content

def make_question(question, answers, max_answers): 
    ca = answers['correct']
    wa = answers['wrong']
    catex = list(map(lambda s: "    \CorrectChoice{" + s + "}", ca))
    watex = list(map(lambda s: f"    \\choice {s}", random.sample(wa, max_answers - len(ca))))
    print(catex)
    print(watex)
    fatex = catex + watex
    random.shuffle(fatex)
    tex = [
        f"  \question {question}",
        "  \\begin{checkboxes}"
    ]
    tex += fatex
    tex.append("  \\end{checkboxes}")
    tex.append("\\vspace{0.5cm}")
    return tex

def make_questions(yaml, max_answers):
    tex = ["\\begin{questions}"]
    questions = []
    for question in yaml['questions']:
        questions.append(make_question(question['question'], question['answers'], max_answers))
    random.shuffle(questions)
    for question in questions:
        tex += question
    tex += ["\end{questions}"]
    return tex

def make_descr(yaml):
    tex = ["\subsection*{Instructions}", "\\begin{itemize}"]
    tex += map(lambda s: "\item{" + s + "}", yaml)
    tex += ["\\end{itemize}"]
    return tex

def make_exam(yaml, max_answers=4):
    title = yaml['title']
    institution = yaml['institution']
    course = yaml['course']
    edition = yaml['edition']
    descr = yaml['description']
    tex = [ 
        "\\usepackage{tcolorbox}",
        "\\usepackage{listings}",
        "\lstset{basicstyle=\\ttfamily,breaklines=true}",
        "\lstset{framextopmargin=50pt,frame=bottomline}",
        "\\renewcommand\labelitemi{-}",
        "\pagestyle{headandfoot}",
        "\\runningheadrule",
        "\\runningheader{" + course + "}{}{" + edition + "}",
        "\\firstpagefootrule",
        "\\firstpagefooter{\\today}{" + institution + "}{\\thepage\,/\,\\numpages}",
        "\\runningfootrule",
        "\\runningfooter{\\today}{" + institution + "}{\\thepage\,/\,\\numpages}",
        "\\usepackage{etoolbox}",
        "\BeforeBeginEnvironment{checkboxes}{\\vspace*{0.25cm}\par\\nopagebreak\minipage{\linewidth}}",
        "\AfterEndEnvironment{checkboxes}{\\vspace*{0.25cm}\endminipage}"
        "\\begin{document}",
        "\\begin{tcolorbox}[width=\\textwidth]",
        "\section*{\centering " + title + "}",
        "\end{tcolorbox}",
        "\\vspace{0.5cm}"
          ]   
    tex += make_descr(descr)
    tex += ["\\vspace{1cm}", "\par\\noindent\\rule{\\textwidth}{0.4pt}"]
    tex += make_questions(yaml, max_answers)
    tex += [ "\end{document}" ]
    questions_tex = [ "\documentclass[addpoints,12pt]{exam}" ] + tex
    answers_tex = [ "\documentclass[answers,addpoints,12pt]{exam}" ] + tex
    return (questions_tex, answers_tex)

def print_tex(tex, outfile):
    with open(outfile, "w") as o:
        for line in tex:
            o.write(f"{line}\n")


parser = argparse.ArgumentParser(description='Create exam and answers from a template.')
parser.add_argument('input', type=str, help='the input YAML file')
parser.add_argument('prefix', type=str, help='prefix for the output files')
parser.add_argument('--versions', type=int, default=1,
                    help='number of versions to produce')
args = parser.parse_args(sys.argv[1:])
print(args)
content = read_yaml(args.input)
latex_cmd = "/Library/TeX/texbin/pdflatex" 

for version in range(0, args.versions):
  (questions, answers) = make_exam(content['exam'])
  questions_file = f"{args.prefix}-questions-v{version}.tex"
  answers_file = f"{args.prefix}-answers-v{version}.tex"
  print_tex(questions, questions_file) 
  print_tex(answers, answers_file) 
  subprocess.run([latex_cmd, questions_file])
  subprocess.run([latex_cmd, questions_file])
  subprocess.run([latex_cmd, answers_file])
  subprocess.run([latex_cmd, answers_file])