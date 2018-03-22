#!/usr/bin/env python2

import argparse
import os
import subprocess

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


import textwrap as _textwrap
class MultilineFormatter(argparse.HelpFormatter):
    def _fill_text(self, text, width, indent):
        text = self._whitespace_matcher.sub(' ', text).strip()
        paragraphs = text.split('|n ')
        multiline_text = ''
        for paragraph in paragraphs:
            formatted_paragraph = _textwrap.fill(paragraph, width, initial_indent=indent, subsequent_indent=indent) + '\n'
            multiline_text = multiline_text + formatted_paragraph
        return multiline_text



def Main():
    parser = argparse.ArgumentParser(
    description="""Little tool to add a footer with pagenumbers, image and classification to a pdf file. Outputs file as output.pdf. Uses pdflatex to generate the pdf. |n |n To only add pagenumbers: |n
                ./pdffooter.py test.pdf |n
              To add pagenumbers and classification:|n
                ./pdffooter.py test.pdf -c Confidential 
              To add pagenumbers, a classification and an image/logo:|n
                ./pdffooter.py test.pdf -c Confidential -l logo.pdf
              To add pagenumbers and an image/logo:|n
                ./pdffooter.py test.pdf -l logo.png
            """, formatter_class=MultilineFormatter)
    parser.add_argument("DOC", help="The filename of the PDF of which you want to add pagenumbers to. It'll number page 2 and up.")
    parser.add_argument("-c", "--classification", help="Sets the classification of the document in the footer, default is no classification.", default=" ")
    parser.add_argument("-l", "--logo", help="Sets a logo or image in the right footer of the document, default is no image or logo. (tested with logo.pdf and logo.png, does not work with logo.svg.)", default=" ")



    args = parser.parse_args()
    
    document = str(args.DOC)
    logo= str(args.logo)

    if logo == " ":
        logo=""
    else: 
        logo="""\\rfoot{\includegraphics[width=2cm]{"""+str(args.logo)+"""}}% sets logo or image on the right"""

    print bcolors.HEADER + "The input pdf file is "  + str(args.DOC)+ "." + bcolors.ENDC


    print bcolors.HEADER + "The classification of the file is set to "+ str(args.classification)+ "." + bcolors.ENDC
    print bcolors.HEADER + "The header includes the following logo or image: "+ str(args.logo)+ "." + bcolors.ENDC
    content = r"""\documentclass[10pt]{article}
\usepackage[final]{pdfpages}
\usepackage{fancyhdr}
\renewcommand{\familydefault}{\sfdefault}

\topmargin 70pt
\oddsidemargin 70pt

\pagestyle{fancy}
\cfoot{\textsf\thepage}%sets pagenumber in the center
\lfoot{"""+str(args.classification)+"""}% sets classification on the left
"""+(logo)+"""

\\renewcommand {\\footrulewidth}{0pt}% makes sure there is no line above the footer
\\renewcommand {\headrulewidth}{0pt}% makes sure there is no line below the header

\\begin{document}
\includepdf[pages=1]{"""+str(document)+"""}%skips first page with footer
\includepdfset{pagecommand=\\thispagestyle{fancy}}
\includepdf[pages=2-]{"""+str(document)+"""}% adds footer to second page and beyond
\end{document}
"""

    
    print bcolors.HEADER + "The generated en used template for pdflatex is: \n"+ bcolors.ENDC + bcolors.OKBLUE + content + bcolors.ENDC

    



    with open('output.tex','w') as f:
        f.write(content)

    cmd = ['pdflatex', '-interaction', 'nonstopmode', 'output.tex']
    proc = subprocess.Popen(cmd)
    proc.communicate()

    retcode = proc.returncode
    if not retcode == 0:
        os.unlink('output.pdf')
        raise ValueError('Error {} executing command: {}'.format(retcode, ' '.join(cmd))) 

    os.unlink('output.tex')
    os.unlink('output.log')
    os.unlink('output.aux')


if __name__ == '__main__':
    Main()
