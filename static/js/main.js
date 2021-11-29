$(function () {
    $('.for_movies_shots_slider').slick({
        autoplay: true,
        autoplaySpeed: 7000,
        infinite: true,
        speed: 500,
        fade: true,
        arrows: false,
        cssEase: 'linear',
        slidesToShow: 1,
        slidesToScroll: 1,
        asNavFor: '.movies_shots_slider',
    });
    $('.movies_shots_slider').slick({
        slidesToShow: 2,
        slidesToScroll: 1,
        asNavFor: '.for_movies_shots_slider',
        arrows: true,
        centerMode: true,
        focusOnSelect: true
    });
})