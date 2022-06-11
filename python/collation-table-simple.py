# Visualisation of Collatex JSON output as HTML table. Useful for huge collations, which are impractical to display as graphs.
# Input: Collation in JSON format (e.g., as output by Collatex).
# Output: HTML table showing tokens as rows and witnesses as columns.
# Simpler version of collation_table.py.
# Created 27 August 2019, Violeta Seretan
# Usage: python3 collation-table-simple.py -i <inputFile> -o <outputFile>
# Example:
#

import json
import os, sys, getopt
import collections
from collections import Counter

def generate_html_file(jsondata, outfname_arg):

    witnesses = jsondata["witnesses"]
    collation = jsondata["table"]

    # generate the HTML file
    htmlText = "<html>\n\t<head>"
    htmlText += "\n\t\t<title>ENLAC - Collation Table</title>"
    htmlText += "\n\t\t<meta charset='UTF-8'/>"
    htmlText += "\n\t\t<style>td:first-child {text-align: right; font-weight: bold;}"
    htmlText += "\n\t\t\ttr {background-color: white; color: lightgrey;}"
    htmlText += "\n\t\t\t thead tr {background-color: lightgrey;}"
    htmlText += "\n\t\t\t.v {background-color: lightyellow; color: black;}</style>"

    htmlText += "\n\t</head>\n\t<body>\n\t<h1>Collation Table</h1>"

    htmlText += "\n<table border='1' style='border-collapse:collapse; margin: auto'>\n"

    # table headers: witness links
    htmlText += '<thead>\n<tr>'
    htmlText += "\n<th></th>"
    for w in witnesses:
        htmlText += "\n<th>" + "<a href='../1-wf-css/" + w + ".xml' target='_blank'>" + w + "</a></th>"
    htmlText += '\n</tr>\n</thead>'

    # table body: first token index, then one cell/witness showing token (t) and normalised form (n)
    htmlText += '\n<tbody>\n'
    for idx, row in enumerate(collation):
        variants = []
        for w in row:
            if not w:
                variants.append('')
            else:
                for token in w:
                    variants.append(token['n'])
        d = collections.Counter(variants)
        different = (len(d) > 1)

        htmlText += "\n<tr"
        if different:
            htmlText += " class='v'"

        htmlText += "><td>" + str(idx + 1) + "</td>"
        for w in witnesses:
            index = witnesses.index(w)
            tForm = ''.join(token['t'] for token in row[index])
            nForm = ''.join(token['n'] for token in row[index])
            htmlText += "\n<td>" + tForm + "</td>"
        htmlText += "\n</tr>\n"
    htmlText += "\n</tbody>\n</table>"

    htmlText += "\n</body>\n</html>"

    htmlfile = open(outfname_arg, "w")
    htmlfile.write(htmlText)
    htmlfile.close()

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:",["ifile=","ofile="])
    except getopt.GetoptError as err:
        print("Command line error.")
        # print help information and exit:
        print(str(err))  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('collation-table.py -i <inputFile> -o <outputFile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    if (inputfile == "") or (outputfile == ""):
        print("Command line error.")
        print("Usage:" + 'collation-table.py -i <inputFile> -o <outputFile>')
        sys.exit(2)
    if not(os.path.exists(inputfile)):
        print("Check input file.")
        sys.exit(2)
    if not(os.path.isfile(inputfile) and os.path.getsize(inputfile) > 0):
        print("Empty input file.")
        sys.exit(2)
    with open (inputfile, encoding='utf-8') as jsonfile:
        try:
            jsondata = json.load(jsonfile)
            generate_html_file(jsondata, outputfile)
        except ValueError as e:
            print("Invalid JSON file: " + str(e))

if __name__ == "__main__":
    main(sys.argv[1:])
