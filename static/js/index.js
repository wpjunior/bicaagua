$(document).ready (function (e) {
    $('.slider').ulslide({
	statusbar: true,
	width: 400,
	height: 'auto',
	affect: 'fade',
	duration: 500,
	autoslide: 8000

    });
    $('.mini-slider').ulslide({
	statusbar: true,
	width: 200,
	height: 'auto',
	affect: 'fade',
	duration: 500,
	autoslide: 4000

    });
});