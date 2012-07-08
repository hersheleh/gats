

Aloha.ready( function() {
      
    Aloha.jQuery('#edit').aloha();
});


$(document).ready(function() {
    $("#content").delegate("button.post","click",function(){
 	var text = $('p.add_post').html();
	var image = $('#upload_target').contents().find('body').html();
	$.post($SCRIPT_ROOT + '/edit/add_news', 
	       { news_post: text,
		 filename: image }, 
	       function(data){
		   update_news(data);
	       });
    });
});     
	
$(document).ready(function() {
    $('#content').delegate("button.delete","click",function(){
	var ID = this.id;
	$.post($SCRIPT_ROOT + '/edit/delete_news', {del: ID},
	       function(data) { 
		   update_news(data);
	       });
    });
});

function update_news(data) {
    new_data = $(data).find('div#posted_content');
    $("div#posted_content").replaceWith(new_data);
}


var swfu;

window.onload = function() {
    var settings_object = {
	// PATHS TO SWFUPLOAD CODE
	upload_url : $SCRIPT_ROOT +'/upload',
	flash_url : $SCRIPT_ROOT+"/static/SWFUpload/Flash/swfupload.swf",
	
	prevent_swf_caching: 'true',
	
	// BUTTON CONFIGURATION
	button_placeholder_id: 'swfupload-container',
	button_image_url: '/static/images/button_upload.png',
	button_window_mode : SWFUpload.WINDOW_MODE.TRANSPARENT,
	button_width: '61',
	button_height:'22',
	
	// 
	file_queued_handler: fileQueued
	/*upload_progress_handler: uploadProgress,
	upload_error_handler: uploadError,
	upload_success_handler: uploadSuccess,
	upload_complete_handler: uploadComplete*/
    }
    swfu = new SWFUpload(settings_object);
};

function fileQueued(file) {
    $('#filename-text').val(file.name);
}

function uploadFile(form, e) {

    try {
	swfu.startUpload();
	
    } catch(ex) {
	
    }
}