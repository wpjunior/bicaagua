function setFancyBox () {
    $("#album a.photo").fancybox({
	'overlayOpacity': 0.7,
	'transitionIn'	:	'elastic',
	'transitionOut'	:	'elastic',
	'speedIn'		:	600, 
	'speedOut'		:	200,
	'titlePosition': 'over',
    });
}

$(document).ready(function(e) {
    setFancyBox();
    $('div.photo').hover(function() {
	cap = $(this).find('p.caption');
        if (cap.text().trim().length)
	    cap.fadeIn(200);

    }, function() {
	cap = $(this).find('p.caption');
        if (cap.text().trim().length)
	    cap.fadeOut(200);

    });
});