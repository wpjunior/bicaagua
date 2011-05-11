$(document).ready(function (e) {
    function onEditCB(e) {
	var id = parseInt($(this).parents('div.photo').attr('rel'));
	var thumburl = $('div.photo[rel="'+id+'"] img').attr('src');
	var title = $('div.photo[rel="'+id+'"] a.photo').attr('title');
	
	$("div#editwindow").find('input[name="photo_id"]').val(id);
	$("div#editwindow").find('input[name="name"]').val(title);
	$("div#editwindow").find('img.thumbnail').attr('src', thumburl);
	$("div#editwindow").show();
	$.fancybox({'href': '#editwindow',
		    'onClosed'		: function() {
			$("#editwindow").hide();
		    }});
	return false;
    }

    function onDeleteCB(e) {
	var id = parseInt($(this).parents('div.photo').attr('rel'));
	if (!confirm("tem certeza que deseja apagar essa imagem?"))
	    return;

	$.post($('div#editwindow form').attr('action'),
	       {'photo_id': id, 'action': 'delete_image'},
	       function (data) {
		   $('div.photo[rel="'+id+'"]').remove();
	       });
    }
    $("#addphoto").click( function (e) {
	$("#photo-upload").show();
	$.fancybox({'href': '#photo-upload',
		    'onClosed'		: function() {
			$("#photo-upload").hide();
			window.location.reload();
		    }});
    });

    $('div#editwindow form').submit(function (e) {
	function onEdit(data) {
	    if (data.error) {
		alert(data.error);
		return;
	    }
	    
	    $.fancybox.close();
	    $('div#editwindow').hide();
	    $('div.photo[rel="'+data.id+'"] a.photo').attr('title', data.name);
	    $('div.photo[rel="'+data.id+'"] b.title').text(data.name);
	}
	data = $(this).serialize();
	$.post($(this).attr('action'), data, onEdit);
	return false;
    });

    $("div.photo a.edit").click (onEditCB);
    $("div.photo a.delete").click (onDeleteCB);
});