
var name_of_uploaded_file = "";
var defaultValue = "";


$(document).ready(function() {
    $('input, textarea').click(function() {
	if(this.value == this.defaultValue) {
	    $(this).focus().val('');
	}
    });
    
    $('input, textarea').blur(function() {
	if(this.value == '') {
	    $(this).val(this.defaultValue);
	}
    }); 

    $('.add_post').click(function() {
	var value = $(this).html();
	if (value.search('Write something here..') != -1)  {
	    $(this).html(" ");
	}
    });
});


Aloha.ready( function() {
      
    Aloha.jQuery('#edit').aloha();
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
	var extra_info = $("#extra_info").val();
	$.post($SCRIPT_ROOT + '/edit/add_show',
	       {show_date: show_date,
		venue : venue,
		city : city,
		extra_info : extra_info},
	       function(data) {
		   update_shows(data);
	       });
    });
});


function update_news(data) {
    new_data = $(data).find('div#posted_content');
    $("div#posted_content").replaceWith(new_data);
    //$("img.post_image").width(550);
}

function update_photos(data) {
    new_photos = $(data).find('div#photo_gallery');
    $("div#photo_gallery").replaceWith(new_photos);
}

function update_shows(data) {
    new_shows = $(data).find('div#show_list');
    $('div#show_list').replaceWith(new_shows);
}


// ########################################################################
/* THESE FUNCTIONS CONFIGURE AND DICTATE 
   THE FUNCTIONALITY OF SWFUPLOAD */

var swfu;

window.onload = function() {
    var settings_object = {
	// PATHS TO SWFUPLOAD CODE
	upload_url : $SCRIPT_ROOT +'/upload',
	flash_url : $SCRIPT_ROOT+"/static/SWFUpload/Flash/swfupload.swf",
	file_post_name: 'file',
	
	prevent_swf_caching: 'true',
	
	// BUTTON CONFIGURATION
	button_placeholder_id: 'swfupload-container',
	button_image_url: $SCRIPT_ROOT+'/static/images/button_upload.png',
	button_window_mode : SWFUpload.WINDOW_MODE.TRANSPARENT,
	button_width: '61',
	button_height:'22',
	
	// 
	file_queued_handler: fileQueued,
	upload_progress_handler: uploadProgress,
	
	upload_error_handler: uploadError,
	upload_success_handler: uploadSuccess
	/*
	upload_complete_handler: uploadComplete*/
    }
    swfu = new SWFUpload(settings_object);
};

function fileQueued(file) {
    $('#filename-text').val(file.name);
    $('#create_file').submit();
}

function uploadFile(form, e) {
    try {
	swfu.startUpload();
    } catch(ex) {}
    return false;
}

function uploadProgress(file, bytesLoaded, bytesTotal) {

    try {
	var percent = Math.ceil((bytesLoaded / bytesTotal) * 100);
	$('#upload-progressbar-container').css("display", "block");
	$('#upload-progressbar').css("width", percent+'%')
    } catch (e) {
    }
}

function uploadError(file, errorCode, message) {
}

function uploadSuccess(file, serverData, recievedResponse) {
    try {
	name_of_uploaded_file = serverData;
	setThumbnail(serverData);
    } catch (e){}

}

function setThumbnail(filename) {
    $("img#thumbnail").attr('src', $SCRIPT_ROOT+"/static/files/images/"+
			    filename);
    $("img#thumbnail").width(100);
    $("span#upload_done").text("Upload Complete");
}

// ##################################################################################
