# Collation similarity statistics between pairs of witnesses. Output: HTML table with heatmap and values for number (and percentage) of agreements.
# Created: 06 Novembre 2017, Violeta
# Usage: python3 collation-statistics.py -i <inputfile> -o <outputfile>

import json
import os, sys, getopt
import unidecode, string

def cell_to_string(c):
    string = ''
    for token in c:
        if 'n' in token:
            string += token['n']
        elif 't' in token:
            string += token['t']
    return string

def agree(text1, text2):
    #return unidecode.unidecode(text1.translate("".maketrans('','',string.punctuation))).lower() == unidecode.unidecode(text2.translate("".maketrans('','',string.punctuation))).lower()
    return text1 == text2

def count_agree(inputfilename, collatexdata, verbose):
    witnesses = collatexdata["witnesses"]
    collation = collatexdata["table"]
    if verbose:
        print('Number of witnesses: ' + str(len(witnesses)))
    if verbose:
        print('Number of tokens in collation: ' + str(len(collation)))

    text_agr = "<html>"
    text_agr += "\n<head>"
    text_agr += "\n\t<title>ENLAC Collation  Statistics</title>"

    text_agr += "\n\t<style>"
    text_agr += "\n\t\ttable {\n\t\t\tborder-collapse: collapse; margin:auto\n\t\t}"
    text_agr += "\n\t\ttr td {\n\t\t\ttext-align: right\n\t\t}"
    text_agr += "\n\t\ttr td:nth-child(1){\n\t\t\ttext-align: left;\n\t\t\tbackground: lightgrey;\n\t\t}"
    # text_agr += "\n\t\ttr:nth-child(odd) {\n\t\t\tbackground: white;\n\t\t}"
    # text_agr += "\n\t\ttr:nth-child(even) {\n\t\t\tbackground: lightgrey;\n\t\t}"
    text_agr += "\n\t\ttd > a\n\t\t\t{opacity: 0\n\t\t}"
    text_agr += "\n\t</style>"
    text_agr += "\n</head>"

    text_agr += "\n<body>"

    text_agr += "\n<h1> Collation Statistics </h1>"
    text_agr += "\n<div style='text-align: center;'><p>Click on table cells to compare witnesses</p></div>"

    agreeAll = 0
    totalAll = len(collation)
    for row in collation:
        agreeRow = True
        for x in witnesses:
            index = witnesses.index(x)
            agreeRow = agreeRow and agree(cell_to_string(row[index]), cell_to_string(row[index - 1]))
        if agreeRow:
            agreeAll += 1

    percentage_sim_overall = "{0:.0f}%".format(agreeAll/totalAll * 100)

    text_agr += "\n<table border='1'>\n<tr>\n<th style='text-align:right'>" + \
        "<a href= '" + inputfilename + ".html'" + "target='_blank'>" + \
        percentage_sim_overall + "</a>" + \
        " (<a href='../4-collation-html/" + inputfilename + "_ct.html'" + "target='_blank'>" + \
        str(agreeAll) + "/" + str(totalAll) + "</a>)</th>\n"

    for x in witnesses:
        text_agr += "\n<th style='text-align:right'>" + str(witnesses.index(x) + 1) + "</th>"
    text_agr += "\n</tr>\n"

    for x in witnesses:
        text_agr += "\n\n<tr>"
        text_agr += "\n<td style='text-align:left'><b>" + \
            "<a href='../1-wf-css/" + x + ".xml' target='_blank'>" + \
            str(witnesses.index(x) + 1) + ". " + x + "</a>" + \
            "</b></td>"
        for y in witnesses:
            text_agr += "\n<td"
            agr = 0
            total_both = 0

            index1 = witnesses.index(x)
            index2 = witnesses.index(y)

            if index1 < index2:
                #go through the collation table, row by row
                #to find places where witness x and y agree
                for row in collation:
                    str1 = cell_to_string(row[index1])
                    str2 = cell_to_string(row[index2])

                    if (str1 + str2 != ''):
                        total_both += 1
                        if agree(str1, str2):
                            agr += 1

                percentage_sim = "{0:.0f}%".format(agr/total_both * 100) # format(agr/len(collation) * 100)
                opposite = "{0:.0f}%".format((1 - agr/total_both) * 100)
                text_agr += " style='background:rgb(" + opposite + ", " + opposite + ", " + opposite + ")"

                #text_agr += ";color:red"
                #text_agr += ";color:rgb(" + percentage_sim + ", " + percentage_sim + ", " + percentage_sim + ")"
                text_agr += "'>"
                text_agr += "<a title='" + percentage_sim + " (" + str(agr) + "/" + str(total_both) + ")" +\
                    "' href='diff_" + inputfilename + "_" + x + "-" + y + ".html" + "'>"
                text_agr += percentage_sim
                #text_agr += str(agr) + " (" + percentage_sim + ")"
                text_agr += "</a>"

            else:
                text_agr += ">" # td.

            text_agr += "</td>"
        text_agr += "\n</tr>"
    text_agr += "\n</table>\n</body>\n</html>"

    return text_agr

def main(argv):
    inputfile = ''
    outputfile = ''
    verbose = False
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
            print ('collation-statistics.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt == '-v':
            verbose = True
    if verbose:
        print('Input file:' + inputfile)
        print('Output file:' + outputfile)
    # print('OS:' + sys.platform)

    if (inputfile == "") or (outputfile == ""):
        print("Command line error.")
        print("Usage:" + 'collation-statistics.py -i <inputfile> -o <outputfile>')
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
            #print(count_agree(jsondata))
            htmlfile = open(outputfile, "w")
            htmlfile.write(count_agree(os.path.basename(inputfile), jsondata, verbose))
            htmlfile.close()
            # print("Opening output file (" + outputfile + ")...")
            # if not(sys.platform.startswith('win')):
            #    os.system('open ' + outputfile)
        except ValueError as e:
            print("Invalid JSON file: " + str(e))

if __name__ == "__main__":
    main(sys.argv[1:])
