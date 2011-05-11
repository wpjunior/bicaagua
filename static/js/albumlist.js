$(document).ready(function (e) {
    $('div.album').hover(function() {
        $(this).find('p.caption').fadeIn(200);
    }, function() {
	$(this).find('p.caption').fadeOut(200);
    });

    $('a.to_button').button();
    $('div.album a.delete').click (function (e) {
	var id = parseInt($(this).parents('div.album').attr('rel'));
	if (!confirm("Tem certeza que deseja apagar esse album ?")) {
	    return
	}
	$.post('/albuns/action/', {'action': 'delete_album', 'album_id': id},
	       function (data) {
		   if (data.error) {
		       alert(data.error)
		       return;
		   }
		   window.location.reload();
	       });
    });
});