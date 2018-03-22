# pdffooter
Little tool to add a footer with pagenumbers, image and classification to a pdf file.

```bash 
$ ./pdffooter.py --help
usage: pdffooter.py [-h] [-c CLASSIFICATION] [-l LOGO] DOC

Little tool to add a footer with pagenumbers, image and classification to a
pdf file. Outputs file as output.pdf. Uses pdflatex to generate the pdf.

To only add pagenumbers:
./pdffooter.py test.pdf
To add pagenumbers and classification:
./pdffooter.py test.pdf -c Confidential To add pagenumbers, a classification
and an image/logo:
./pdffooter.py test.pdf -c Confidential -l logo.pdf To add pagenumbers and an
image/logo:
./pdffooter.py test.pdf -l logo.png

positional arguments:
  DOC                   The filename of the PDF of which you want to add
                        pagenumbers to. It'll number page 2 and up.

optional arguments:
  -h, --help            show this help message and exit
  -c CLASSIFICATION, --classification CLASSIFICATION
                        Sets the classification of the document in the footer,
                        default is no classification.
  -l LOGO, --logo LOGO  Sets a logo or image in the right footer of the
                        document, default is no image or logo. (tested with
                        logo.pdf and logo.png, does not work with logo.svg.)
```
