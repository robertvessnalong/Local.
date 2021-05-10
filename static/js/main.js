(function ($) {
  'use strict';

  let fullHeight = function () {
    $('.js-fullheight').css('height', $(window).height());
    $(window).resize(function () {
      $('.js-fullheight').css('height', $(window).height());
    });
  };
  fullHeight();

  let carousel = function () {
    $('.featured-carousel').owlCarousel({
      loop: true,
      autoplay: true,
      margin: 30,
      animateOut: 'fadeOut',
      animateIn: 'fadeIn',
      nav: true,
      dots: true,
      autoplayHoverPause: false,
      items: 1,
      navText: [
        "<span class='ion-ios-arrow-back'></span>",
        "<span class='ion-ios-arrow-forward'></span>",
      ],
      responsive: {
        0: {
          items: 1,
        },
        600: {
          items: 2,
        },
        1000: {
          items: 3,
        },
      },
    });
  };
  carousel();
})(jQuery);

let swiper = new Swiper('.mySwiper', {
  autoplay: {
    delay: 5000,
    disableOnInteraction: false,
  },
  effect: 'fade',
});

let swiperRestPage = new Swiper('.mySwiper-Rest-Page', {
  slidesPerView: 3,
});
