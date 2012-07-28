
var Aloha = window.Aloha || (window.Aloha = {});

Aloha.settings = {
    floatingmenu: {
	width:200,
	pin:false,
	horizontalOffset:5,
	topalignOffset:40,
	
    },

    plugins: {
	format: {
	    config: ['b', 'i', 'p', 'del', 'title', 'pre'],
	    editables : {
		'#edit_no_menu': []
	    }
	}
    }
};