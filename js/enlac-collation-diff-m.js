// Adds interaction to HTML files of type collation.json.html (which show multiple witnesses with color-coded differences):
// On mouse over, the corresponding units in all witnesses are highlighted in red.
// On click, the corresponding units in all witnesses are zoomed.
// On double click, all occurrences are highlighted in dark orange. Double clicking again switches highlighting (on/off).

//Usage:
//Add the following lines to the HTML file (inside the head or the body tag).
//    <script type="text/javascript" src="http://code.jquery.com/jquery-latest.min.js"></script>
//    <script type="text/javascript" src="../js/enlac-collation-diff-m.js"></script>
$(document).ready(function() {

    var variantColor = "#5DBCD2" //UNIL

    $("body").css('background-color', "#5DBCD2");
    $("table").css('background-color', "white");
    $("span.v").css('background-color', "yellow");

    $("body").css("font-family", "Lucida Grande", "Cardo", "Arial Unicode MS","Galilee Unicode Gk", "New Athena Unicode", "Athena Unicode", "Palatino Linotype", "Titus Cyberbit Basic", "Vusillus Old Face", "Alphabetum", "Galatia SIL", "Code 2000", "GentiumAlt", "Gentium", "Minion Pro", "GeorgiaGreek", "Vusillus Old Face Italic", "Everson Mono", "Aristarcoj", "Porson", "Legendum", "Aisa Unicode", "Hindsight Unicode", "Caslon", "Verdana", "Tahoma");

    var originalBGColor = "";
    var originalColor = "";
    var originalSize = $("span").css("fontSize");
    var currentId = 0;
    var dblclickContent = "";
    var counter = 0;
    var maxId = parseInt($('span').last()[0].id);
    //console.log(maxId);

    $("span.v").mouseover(function (event) {
        currentId = parseInt($(this).attr('id'));

        originalBGColor = $(this).css('background-color');
        originalColor = $(this).css('color');

        $("span[id=" + currentId + "]").css("fontSize", parseInt(originalSize) + 4 + "px");
        $("span[id=" + currentId + "]").css("font-weight", "Bold");
        $("span[id=" + currentId + "]").css("border", "2px solid " + variantColor);
        $("span[id=" + currentId + "]").css("border-radius", "5px");
    });

    $("span.v").mouseout(function(event) { //restore
        $("span[id=" + currentId + "]").css('background-color', originalBGColor);
        $("span[id=" + currentId + "]").css('fontSize', originalSize);
        $("span[id=" + currentId + "]").css("font-weight", "normal");
        $("span[id=" + currentId + "]").css("border", "none");
    });

    /*
    $("span").click(function(event) {
        $("span[id=" + currentId + "]").css("fontSize", parseInt(originalSize) + 10 + "px");

        // restore color to originalColor
        $('span').filter(function() {
                         return ( $(this).css('background-color') == 'rgb(255, 140, 0)' ); //darkorange
                         }).css('background-color', originalBGColor);
    });*/

    $("span").dblclick(function(event) {
       counter += 1
       // restore color to originalColor
       $('span').filter(function() {
                        return ( $(this).css('background-color') == 'rgb(255, 140, 0)' ); //darkorange
                        }).css('background-color', originalBGColor);
       // apply color on this & chain
       dblclickContent = $(this).text().trim();
       $('span').filter(function(){ return $(this).text().trim() === dblclickContent;}).css('background-color', 'rgb(255, 140, 0)'); //darkorange

       if (counter % 2 == 0){
           // restore color again
           $('span').filter(function() {
                            return ( $(this).css('background-color') == 'rgb(255, 140, 0)' ); //darkorange
                            }).css('background-color', originalBGColor);

       }

       /*
         $('span').filter(function(){ return $(this).text() === dblclickContent;}).css("fontSize", parseInt(originalSize) + 10 + "px");
         $('span').filter(function(){ return $(this).text() === dblclickContent;}).css("border", "5px solid red");
            $('span').filter(function(){ return $(this).text() === dblclickContent;}).css("border-radius", "15px");
        */
    });


    $(document).keydown(function(e){
          e.preventDefault();
          switch (e.keyCode) {
              case 37: //left arrow
                  //console.log("left")
                  //console.log(currentId);
                  $("span[id=" + currentId + "]").mouseout();
                  //$("#" + currentId).css('background-color') == 'red'
                  do {
                      currentId -= 1;
                  //console.log($("#L" + currentId).css('background-color'));
                  }
                  while ((currentId >= 0) && (! $("#" + currentId).hasClass('v')))
                  $("span[id=" + currentId + "]").mouseover();
              break;
              case 39: //right arrow
                  //console.log("right")
                  //console.log(currentId);
                  //$("#" + currentId).css('background-color') == 'red'

                  $("span[id=" + currentId + "]").mouseout();
                      do {
                      currentId += 1;
                      }
                      while ((currentId <= maxId) && (! $("#" + currentId).hasClass('v')))
                      $("span[id=" + currentId + "]").mouseover();
              default:
                      break;
          }
    });

});
