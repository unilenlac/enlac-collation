# Visualisation of differences between (pairs of) witnesses, based on CollateX JSON collation data.
# Output:
#   1) visualisation of pairs of witnesses: n*(n-1)/2 HTML documents, where n = number of witnesses.
#   2) -- ,, --                  all witnesses together: 1 HTML document
# Created: 23 Novembre 2017, Violeta Seretan
# Usage: python3 collation-diff.py -i <inputFile> [-o <outputDir>]
# Example: python3 ~/Documents/dev/python/collation-diff.py -i ~/Documents/runs/tpen2stemmaweb/2017-10-24-Grec/output/collation-grec.json

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

def getToken(obj):
    str = ''
    for token in obj:
        if 't' in token:
            str += token['t']
    return str

def getNorm(obj):
    str = ''
    for token in obj:
        if 'n' in token:
            str += token['n']
    return str

def agree(text1, text2):
    return text1 == text2

def generate_html_files(inputfile, collatexdata, outputDir):
    witnesses = collatexdata["witnesses"]
    collation = collatexdata["table"]
    #print('Number of witnesses: ' + str(len(witnesses)))
    #print('Number of tokens in collation: ' + str(len(collation)))

    files = 0
    for x in witnesses:
        for y in witnesses:
            index1 = witnesses.index(x)
            index2 = witnesses.index(y)
            if index1 < index2:
                # generate an HTML file displaying (dis)agreements
                htmlText = "<html>\n\t<head>"
                htmlText += "\n\t\t<title>ENLAC - Collation</title>"
                htmlText += "\n\t\t<meta charset='UTF-8'/>"
                htmlText += "\n\t\t<style>.v {background-color: yellow;}</style>"
                htmlText += "\n\t\t<link rel=\"stylesheet\" href=\"enlac.css\">"
                htmlText += "\n\t\t<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js\"></script>"
                htmlText += "\n\t\t<script src=\"enlac-collation-diff.js\"></script>"
                htmlText += "\n\t</head>\n"

                htmlText += "<body>\n<center><h1 style='font-size:40px;color:black'>ENLAC - Collation</h1></center>" + \
                    "<table style='line-height:200%' border='1' width='100%'>\n<tr>\n<th width='50%'>" + \
                    "<a href='../1-wf-css/" + x + ".xml' target='_blank'>" + x + "</a>" + \
                    "</th><th>" + \
                    "<a href='../1-wf-css/" + y + ".xml' target='_blank'>" + y + "</a>" + \
                    "</th>\n</tr>\n"

                total_both = 0; agr = 0
                cell1 = ''; cell2 = ''

                # browse collation row by row and display agreement/disagreement
                for idx, row in enumerate(collation):

                    str1 = cell_to_string(row[index1])
                    str2 = cell_to_string(row[index2])

                    if (str1 + str2 != ''): # both might be empty, in case of collation with additional witnesses (a third, fourth etc).
                        total_both += 1
                        if agree(str1, str2):
                            agr += 1
                            colorText = ""
                        else:
                            colorText = " class='v'"

                    token1 = getToken(row[index1])
                    token2 = getToken(row[index2])

                    cell1 += "<span id='L" + str(idx) + "'" + colorText + ">" + token1 + "</span> "
                    cell2 += "<span id='R" + str(idx) + "'" + colorText + ">" + token2 + "</span> "

                htmlText += "<tr><td valign='top'>" + cell1 + "</td><td valign='top'>" + cell2 + "</td></tr>"
                htmlText += "\n</table>"

                percentage_sim = "{0:.0f}%".format(agr/total_both * 100)
                agrStr = "\n<p>Agreements: " + str(agr) + "/" + str(total_both) + " (" + percentage_sim + ")"
                htmlText += agrStr + "</p>"

                # add link to collation table (partial, for this witness pair only)
                htmlText += "\n<p><a href='../4-collation-html/" + inputfile + "_"+ x + "-" + y + "_ct.html' target='_blank'>Collation table</a></p>"

                htmlText += "\n</body>\n</html>"

                outputfile= outputDir + "diff_" + inputfile + "_"+ x + "-" + y + ".html"
                htmlfile = open(outputfile, "w")
                htmlfile.write(htmlText)
                htmlfile.close()
                #print("New file: " + outputfile + "\t" + agrStr)
                files += 1
    #print("Files created: " + str(files))

def generate_html_concordance(inputfile, collatexdata, outputDir):
    # creates one HTML file containing all witnesses with color-coded differences.
    witnesses = collatexdata["witnesses"]
    collation = collatexdata["table"]
    #print('Number of witnesses: ' + str(len(witnesses)))
    #print('Number of tokens in collation: ' + str(len(collation)))

    # table with one row and as many cells as there are witnesses

    htmlText = "<html>\n\t<head>"
    htmlText += "\n\t\t<title>ENLAC - Collation</title>"
    htmlText += "\n\t\t<meta charset='UTF-8'>"
    htmlText += "\n\t\t<style>.v {background-color: yellow;}</style>"
    htmlText += "\n\t\t<link rel=\"stylesheet\" href=\"enlac.css\">"
    htmlText += "\n\t\t<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js\"></script>"
    htmlText += "\n\t\t<script src=\"enlac-collation-diff-m.js\"></script>"
    htmlText += "\n\t</head>\n"

    htmlText += "<body>\n<center><h1 style='font-size:40px;color:black'>ENLAC - Collation</h1></center>"
    htmlText += "<table style='line-height:200%' border='1' width='100%'>\n\t\t<tr>\n"

    for w in witnesses:
        htmlText += "<th><a href='../1-wf-css/" + w + ".xml'>" + w + "</a></th>"
    htmlText += "</tr>\n\t\t<tr>\n"

    for w in witnesses:
        newCell = ''
        for idx, row in enumerate(collation):
            equal = True
            text = getToken(row[0])
            normText = getNorm(row[0])

            for x in witnesses:
                i = witnesses.index(x)
                newText = getToken(row[i])
                normNewText = getNorm(row[i])
                equal = equal and (agree(normText, normNewText) or agree(text, newText))
            if equal:
                colorText = ""
            else:
                # highlight differences
                colorText = "class='v'" #" style='background-color: yellow'";
            newCell += "<span id='" + str(idx) + "'" + colorText + ">" + getToken(row[witnesses.index(w)]) + "</span> "

        htmlText += "<td id='" + w + "' valign='top'>" + newCell + "</td>\n"

    htmlText += "\n\t\r</tr></table>"
    htmlText += "\n<p><a href='../4-collation-html/" + inputfile + "_ct.html'" + "target='_blank'>Collation table</a></p>"

    htmlText += "\n\t</body>\n</html>"

    outputfile= outputDir + inputfile + ".html"
    htmlfile = open(outputfile, "w")
    htmlfile.write(htmlText)
    htmlfile.close()
    # print("New file: " + outputfile)
    # print("Opening output file (" + outputfile + ")...")
    # if not(sys.platform.startswith('win')):
    #   os.system('open ' + outputfile)

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
            print ('collation-statistics.py -i <inputfile> -o <outputDir>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--odir"):
            outputDir = arg
    # print('Input file:' + inputfile)
    # print('Output directory:' + outputDir)

    if (inputfile == ""):
        print("Command line error.")
        print("Usage:" + 'collation-diff.py -i <inputFile> -o <outputDir>')
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
            generate_html_concordance(os.path.basename(inputfile), jsondata, outputDir)
        except ValueError as e:
            print("Invalid JSON file: " + str(e))

if __name__ == "__main__":
    main(sys.argv[1:])
