$(document).ready(function () {
    $('.list-group').on('scroll', function () {
        var scrollLeft = $(this).scrollLeft();
        var scrollWidth = $(this).get(0).scrollWidth;
        var clientWidth = $(this).get(0).clientWidth;
        var maxScroll = scrollWidth - clientWidth;

        if (scrollLeft === 0) {
            $('.fade-left').hide();
        } else {
            $('.fade-left').show();
        }

        if (scrollLeft === maxScroll) {
            $('.fade-right').hide();
        } else {
            $('.fade-right').show();
        }
    });

    $('.arrow').click(function () {
        var direction = $(this).hasClass('left-arrow') ? '-=100' : '+=100';
        $('.list-group').animate({
            scrollLeft: direction
        }, 500);
    });
});
