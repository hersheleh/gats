
$(document).ready(function() {
    $("li").click(function() {
	var ID = this.id;
	$("a#"+ID).removeAttr('href');
	$("li#"+ID).load($SCRIPT_ROOT + '/navigate #'+ID, { p: ID });
    });
});
