$(function() {
    $("#menu").delegate("a", "click", function() {
	var ID = this.id;
	$("a#"+ID).removeAttr('href'); //Makes Link unclickable
	$.post($SCRIPT_ROOT +'/navigate', { p: ID }, 
	      function(data) {
		  menu = $(data).find('ul#navigator');
		  content = $(data).find('div#content');
		  $("ul#navigator").replaceWith(menu);
		  $("div#content").replaceWith(content);
	      });
    });
});
