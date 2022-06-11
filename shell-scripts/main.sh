#!/bin/sh

#check arguments
if [ $# -lt 1 ]
then
    printf "\nUsage:\tinputfolder"
    printf "\n\tinputfolder \t-- path to ENLAC output (containing subfolders \1-wf to \4-collations)\n"
    exit 0
fi

INPUT=$1

rm -r $INPUT/1-wf-css/ 2> /dev/null
mkdir -p $INPUT/1-wf-css
cp /enlac-collation/html/enlac.css $INPUT/1-wf-css
cp /enlac-collation/html/tei-enlac.css $INPUT/1-wf-css
cp /enlac-collation/html/tei-enlac-notes-off.css $INPUT/1-wf-css
cp /enlac-collation/html/notes-on.jpg $INPUT/1-wf-css
cp /enlac-collation/html/notes-off.jpg $INPUT/1-wf-css
cp /enlac-collation/js/enlac-revision.js $INPUT/1-wf-css

rm -r $INPUT/4-collation-html/ 2> /dev/null
mkdir -p $INPUT/4-collation-html/
cp /enlac-collation/html/enlac.css $INPUT/4-collation-html

rm -r $INPUT/5-diff/ 2> /dev/null
mkdir -p $INPUT/5-diff/
cp /enlac-collation/html/enlac.css $INPUT/5-diff
cp /enlac-collation/js/enlac-collation-diff.js $INPUT/5-diff
cp /enlac-collation/js/enlac-collation-diff-m.js $INPUT/5-diff


PYTHON_SCRIPTS_PATH="/enlac-collation/python/"

if find $INPUT/1-wf/ -name "*.xml" | wc -l | grep -qw "0";
then
    printf "\nNo XML files found."
    exit 0
else
    printf "\n`find $INPUT/1-wf/ -name "*.xml" | wc -l` XML files found"
fi

if find $INPUT/4-collations/ -name "*.json" | wc -l | grep -qw "0";
then
    printf "\nNo JSON collation files found."
    exit 0
else
    printf "\n`find $INPUT/4-collations/ -name "*.json" | wc -l` JSON collation files found\n"
fi


printf "\nRenaming XML transcription files with the corresponding sigla..."
for file in `ls $INPUT/1-wf |grep ".xml"`
do
    SIGIL=`sed -rn 's/.*xml:id="([^"]*)".*/\1/p' $INPUT/1-wf/$file`
    cp $INPUT/1-wf/$file $INPUT/1-wf-css/"$SIGIL.xml"
done

printf "\nGenerating revision pages..."
for file in `ls $INPUT/1-wf-css|grep ".xml"`
do
    # add editorial hyphen
    sed -r -i 's/([^ ])(<lb n="[[:alnum:]]*" *\/>[^ ])/\1<supplied resp="editor">-<\/supplied>\2/g' $INPUT/1-wf-css/$file
    sed -r -i 's/([^ ])(<lb *\/>[^ ])/\1<supplied resp="editor">-<\/supplied>\2/g' $INPUT/1-wf-css/$file

    # add CSS stylesheet declaration
    sed -i '2i <?xml-stylesheet type="text/css" href="tei-enlac.css"?>' $INPUT/1-wf-css/$file

    # add second CSS stylesheet declaration (turn off notes)
    cp $INPUT/1-wf-css/$file $INPUT/1-wf-css/notes-off-$file
    sed -i '3i <?xml-stylesheet type="text/css" href="tei-enlac-notes-off.css"?>' $INPUT/1-wf-css/notes-off-$file
done
printf "\nRevision files stored in: $INPUT/1-wf-css\n"

printf "Generating main ENLAC Revision page..."
html="$INPUT/1-wf-css/revision.html"
printf "<html>\n<head>\n\t<meta charset=\"utf-8\"/>\n\t<title> ENLAC Revision</title>" > $html
printf "\n\t<style>table {margin: auto}\n\ta {text-decoration: none; padding: 8px 16px;}" >> $html
printf "\n\ta:hover {background-color: #4CAF50; color: white;}" >> $html
printf "\n\t.arrow {background-color: #4C9950; color: lightgrey; border-radius: 50%%;}</style>" >> $html
printf "\n\t<script type=\"text/javascript\" src=\"https://code.jquery.com/jquery-3.3.1.min.js\"></script>" >> $html
printf "\n\t<script type=\"text/javascript\" src=\"enlac-revision.js\"></script>\n</head>\n" >> $html
printf "<body>\n\t<table height=\"100%%\" width=\"75%%\"><tr><td><a id=\"prev\" class=\"arrow\">&#8249;</a></td><td width=\"50%%\">\n" >> $html
printf "<select id=\"mslist\" style=\"font-size:20px; width:400px;\">" >> $html
for file in `ls $INPUT/1-wf-css/*.xml|grep -v "notes-off-"`
do
    fname=`basename $file`
    printf "\n\t\t<option>$fname</option>" >> $html
done
printf "\n\t</select>" >> $html

printf "\n\t<img id=\"switch\" src=\"notes-on.jpg\" alt=\"Notes on/off\" style=\"height:24px;max-width:2\%%;max-height:2%%\"/>" >> $html
printf "\n\t<span id=\"switchb\" style=\"font-size:20px;font-family:verdana\">Notes</span>" >> $html
printf "\n\t<iframe id=\"xml\" width=\"100%%\" height=\"100%%\" frameBorder=\"0\"></iframe>" >> $html
printf "\n\t</td><td align=\"right\"><a id=\"next\" class=\"arrow\">&#8250;</a></td></tr></table>" >> $html
printf "\n</body>\n</html>" >> $html

printf "\nRevision page generated (1-wf-css/revision.html)\n"


printf "\nGenerating HTML version of collation tables..."

for file in `ls $INPUT/4-collations/`
do
  python3 $PYTHON_SCRIPTS_PATH/collation-table-simple.py -i $INPUT/4-collations/$file -o $INPUT/4-collation-html/${file}_ct.html
  python3 $PYTHON_SCRIPTS_PATH/collation-table-pairs.py -i $INPUT/4-collations/$file -o $INPUT/4-collation-html/
done
printf "\nFiles: `ls -l $INPUT/4-collation-html/*_ct.html | wc -l | xargs` (See $INPUT/4-collation-html/)\n"

for file in `ls $INPUT/4-collation-html|grep "_ct.html"`
do
  # add CSS stylesheet declaration
  sed -i '3i <link rel="stylesheet" type="text/css" href="enlac.css" />' $INPUT/4-collation-html/$file
done

printf "\nGenerating ENLAC Collation pages..."
for file in `ls $INPUT/4-collations/`
do
  python3 $PYTHON_SCRIPTS_PATH/collation-diff.py -i $INPUT/4-collations/$file -o $INPUT/5-diff/
done
printf "\nFiles (HTML): `ls -l $INPUT/5-diff/diff* | wc -l | xargs` (See $INPUT/5-diff/)\n"

printf "\nGenerating ENLAC Statistics pages..."
for file in `ls $INPUT/4-collations/`
do
  python3 $PYTHON_SCRIPTS_PATH/collation-statistics.py -i $INPUT/4-collations/$file -o $INPUT/5-diff/${file%.json}-stat.html
done
printf "\nFiles: `ls -l $INPUT/5-diff/*-stat.html | wc -l | xargs` (See $INPUT/5-diff/)\n"

for file in `ls $INPUT/5-diff/*.html`
do
    # add CSS stylesheet declaration
    sed -i '3i <link rel="stylesheet" type="text/css" href="enlac.css" />' $file
done
