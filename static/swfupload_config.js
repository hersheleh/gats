
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
    $("img#thumbnail").attr('src', $SCRIPT_ROOT+"/uploads/"+
			    filename);
    $("img#thumbnail").width(100);
    $("span#upload_done").text("Upload Complete");
}

// ##################################################################################
