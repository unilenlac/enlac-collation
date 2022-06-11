# Generation of HTML views for comparing pairs of witnesses (one file per witness pair in the collation input).
# Input: Collation in JSON format (e.g., as output by Collatex).
# Output: n*(n-1)/2 HTML documents, where n = number of witnesses.
# Each HTML table shows tokens as rows and  two witnesses as columns.
# Created 13 September 2019, Violeta Seretan
# Usage: python3 collation-table-pairs.py -i <inputFile> -o <outputFile>
# Example:
# python3 collation-table-pairs.py -i collation-witnesses.json -o 4-collation-html/

import json
import os, sys, getopt

def cell_to_string(c):
    string = ''
    for token in c:
        if 'n' in token:
            string += token['n']
        elif 't' in token:
            string += token['t']
    return string

def agree(text1, text2):
    return text1 == text2

def generate_html_files(inputfile, jsondata, outputDir):

    witnesses = jsondata["witnesses"]
    collation = jsondata["table"]

    for x in witnesses:
        for y in witnesses:
            index1 = witnesses.index(x)
            index2 = witnesses.index(y)
            if index1 < index2:
                # generate HTML file displaying a (partial) collation table
                htmlText = "<html>\n\t<head>"
                htmlText += "\n\t\t<title>ENLAC Collation Table " + x + " vs " + y + "</title>"
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
                htmlText += "\n<th>" + "<a href='../1-wf-css/" + x + ".xml' target='_blank'>" + x + "</a></th>"
                htmlText += "\n<th>" + "<a href='../1-wf-css/" + y + ".xml' target='_blank'>" + y + "</a></th>"
                htmlText += '\n</tr>\n</thead>'

                # table body: first token index, then one cell/witness showing token (t) and normalised form (n)
                htmlText += '\n<tbody>\n'

                total_both = 0; agr = 0
                for idx, row in enumerate(collation):

                    str1 = cell_to_string(row[index1])
                    str2 = cell_to_string(row[index2])

                    if (str1 + str2 != ''): # both might be empty, in case of collation with additional witnesses (a third, fourth etc).
                        total_both += 1
                        htmlText += "\n<tr"
                        if agree(str1, str2):
                            agr += 1
                        else:
                            htmlText += " class='v'"

                        htmlText += "><td>" + str(idx + 1) + "</td>"

                        tForm1 = ''.join(token['t'] for token in row[index1])
                        tForm2 = ''.join(token['t'] for token in row[index2])
                        # nForm = ''.join(token['n'] for token in row[index1])

                        htmlText += "\n<td>" + tForm1 + "</td>"
                        htmlText += "\n<td>" + tForm2 + "</td>"
                        htmlText += "\n</tr>\n"

                htmlText += "\n</tbody>\n</table>"

                htmlText += "\n<center>"
                percentage_sim = "{0:.0f}%".format(agr/total_both * 100)
                agrStr = "Agreements: " + str(agr) + "/" + str(total_both) + " (" + percentage_sim + ")"
                htmlText += agrStr
                htmlText += "\n</center>"

                htmlText += "\n</body>\n</html>"

                outputfile = outputDir + inputfile + "_"+ x + "-" + y + "_ct.html"
                htmlfile = open(outputfile, "w")
                htmlfile.write(htmlText)
                htmlfile.close()

def main(argv):
    inputfile = ''
    outputDir = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:",["ifile=","odir="])
    except getopt.GetoptError as err:
        print("Command line error.")
        # print help information and exit:
        print(str(err))  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('collation-table-pairs.py -i <inputfile> -o <outputDir>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--odir"):
            outputDir = arg
    # print('Input file:' + inputfile)
    # print('Output directory:' + outputDir)

    if (inputfile == ""):
        print("Command line error.")
        print("Usage:" + 'collation-table-pairs.py -i <inputfile> -o <outputDir>')
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
            generate_html_files(os.path.basename(inputfile), jsondata, outputDir)
        except ValueError as e:
            print("Invalid JSON file: " + str(e))

if __name__ == "__main__":
    main(sys.argv[1:])
