
var name_of_uploaded_file = "";
var defaultValue = "";


$(document).ready(function() {
    $('input, textarea').focus(function() {
	if(this.value == this.defaultValue) {
	    $(this).val('');
	}
    });
    
    $('input, textarea').blur(function() {
	if(this.value == '') {
	    $(this).val(this.defaultValue);
	}
    }); 

    $('.add_post').focus(function() {
	text_disapear("Write something here...");
    });
    
    $('.extra_info').focus(function() {
	text_disapear("Extra Info");
    });
});



Aloha.ready( function() {
      
    Aloha.jQuery('#edit').aloha();
    Aloha.jQuery('#edit_no_menu').aloha();
});


$(document).ready(function() {
    $("#content").delegate("button.post","click",function(){
 	var text = $('p.add_post').html();
	var title = $("input[name='post_title']").val();
	$.post($SCRIPT_ROOT + '/edit/add_news', 
	       { news_post: text,
		 post_title : title,
		 filename: name_of_uploaded_file }, 
	       function(data){
		   update_news(data);
	       });
    });
});     
	
$(document).ready(function() {
    $('#content').delegate("button.delete","click",function() {
	var ID = this.id;
	$.post($SCRIPT_ROOT + '/edit/delete_news', {del: ID},
	       function(data) { 
		   update_news(data);
	       });
    });
});

$(document).ready(function() {
    $('#content').delegate("button.add_photo","click",function() {
	$.post($SCRIPT_ROOT + '/edit/add_photo', 
	       { filename: name_of_uploaded_file },
	       function(data) {
		   update_photos(data);
	       });
    });
});

$(document).ready(function() {
    $('#content').delegate("button.delete_photo","click", function() {
	var ID = this.id;
	$.post($SCRIPT_ROOT + '/edit/delete_photo', 
	       {photo_id_to_delete: ID},
	       function(data) {
		   update_photos(data);
	       });
    });
});

$(document).ready(function() {
    $('#content').delegate("button.add_show","click", function() {
	
	var show_date = $("#show_date").val();
	var venue = $("#venue").val();
	var city = $("#city").val();
	var extra_info = $('#extra_info').html();
	if (validate_date(show_date)) {
	    
	    $.post($SCRIPT_ROOT + '/edit/add_show',
		   {show_date: show_date,
		    venue : venue,
		    city : city,
		    extra_info : extra_info},
		   function(data) {
		       update_shows(data);
		   });
	}
	else {
 	    $("#show_date").val("Invalid Date");
	    $("#show_date").css('color', '#FF0000');
	    $('#show_date').focus(function() {
		if(this.value == "Invalid Date") {
		    $(this).val('');
		    $("#show_date").css('color', 'white');
		}
	    
	    });
	}
    });
			  
});

function text_disapear(text) {
    var value = $(this).html();
    if (value.search(text) != -1) {
	$(this).html(" ");
    }
}

function update_news(data) {
    new_data = $(data).find('div#posted_content');
    $("div#posted_content").replaceWith(new_data);
    //$("img.post_image").width(550);
}

function update_photos(data) {
    new_photos = $(data).find('div#photo_gallery');
    $("div#photo_gallery").replaceWith(new_photos);
}
		  
function set_extra_info() {
    if("" != input_value[0].defaultValue) {
	return input_value.val();
    }
    else {
	return "";
    }    
}

function validate_date(date) {
    var entered_date = Date.parseExact(date,"MM/dd/yy");
    if (entered_date == null) {
	return false;
    }
    else {
	return true;
    }
}

function update_shows(data) {
    new_shows = $(data).find('div#show_list');
    $('div#show_list').replaceWith(new_shows);
}
