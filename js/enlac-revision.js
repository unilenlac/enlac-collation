
$(document).ready(function() {

    var ms = $('#mslist option:first').text();;
    var htmlpath = $("#switch").attr('src').substring(0, $("#switch").attr('src').indexOf("notes-"));
    //console.log(htmlpath)
    var notes = "true"

    $("#xml").attr('src', ms);

    $("#switch").click(function(event) {
        if (ms != "") {
            if (notes) {
               ms = "notes-off-" + ms;
               $("#switch").attr('src', htmlpath + "notes-off.jpg");
               //$("#switchb").html("Notes Off");
            }
            else if ( ms.indexOf("notes-off-") !== -1) {
               ms = ms.substring("notes-off-".length);
               $("#switch").attr('src', htmlpath + "notes-on.jpg");
               //$("#switchb").html("Notes On");
            }
            notes = ! notes;
            //console.log(ms);
            $("#xml").attr('src', ms)
        }

            /*
            $("#switch").attr('src', "notes-off.jpg");
            }

             if ( $("#xml").attr('src') == "Vat_gr_2125.xml") {
             $("#xml").attr('src', "Vat_gr_2125-notes-off.xml");
             //$(this).css("opacity", "1");
             $("#switch").attr('src', "notes-off.jpg");
             }
             else {
             $("#xml").attr('src', "Vat_gr_2125.xml");
             //$(this).css("opacity", "0.5");
             $("#switch").attr('src', "notes-on.jpg");
             } */
    });

    $("#prev").click(function(event) {
      $("#mslist > option:selected")
          .prop("selected", false)
          .prev()
          .prop("selected", true);
      $('#mslist').change();  
    });

    $("#next").click(function(event) {
      $("#mslist > option:selected")
          .prop("selected", false)
          .next()
          .prop("selected", true);
      $('#mslist').change();
    });

    $('#mslist').on('change', function() {
        ms = $('#mslist option:selected').text();
        if (! notes) { ms = "notes-off-" + ms}
        $("#xml").attr('src', ms);
    })

});
