// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function() {
  $('.js_switch').change(function() { 
    _id=this.id; 
    is_act=0;
    if (this.checked)
	is_act=1;
    else is_act=0;
    this.disabled=true;
    $.post('/switch', {
	id:_id,
	is_activate:is_act		
    }, function(data){
		var chkbox=$('#'+data.id);
		if (data.status > 0){
		    alert(data.msg);
		    chkbox.checked=!chkbox.checked;
		}
		chkbox.removeAttr("disabled");
	   });
    return false;
  });
  $('#reboot').click(function() {
     this.disabled=true;
     $.post('/reboot', {
	action:'rebot',
     }, function(data){
	    alert(data.msg);
	    if (data.status == 0)
		$('#reboot').removeAttr("disabled");
	});
  });
});

