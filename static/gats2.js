$(function() {
    $("#menu").delegate("a", "click", function() {
	var ID = this.id;
	$("a#"+ID).removeAttr('href'); //Makes Link unclickable
	$.post($SCRIPT_ROOT +'/navigate', { p: ID }, function(data) {
	    navigate(data,ID);
	    location.hash = "gats_"+ID;
	});
	       
    });
});

$(function() {
    $(window).hashchange(function() {
	var ID = location.hash;
	$.post($SCRIPT_ROOT + '/navigate', { p : ID  }, function(data) {
	    navigate(data,ID);
	});
    });


    $(window).hashchange();
});

function navigate(data, ID) {
    menu = $(data).find('ul#navigator');
    content = $(data).find('div#content');
    $("ul#navigator").replaceWith(menu);
    $("div#content").replaceWith(content);
}

