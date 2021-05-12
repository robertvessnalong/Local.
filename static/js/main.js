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

async function handleFavorite() {
  const id = $(this).data('id');
  const i = $('.favorite-btn i');
  if ($('.favorite-btn i').hasClass('fas fa-heart')) {
    await axios.delete(`/favorite/${id}/remove`);
    $('.favorite-btn i').attr('class', 'far fa-heart');
  } else if ($('.favorite-btn i').hasClass('far fa-heart')) {
    await axios.post(`/favorite/${id}`);
    $('.favorite-btn i').attr('class', 'fas fa-heart');
  }
}

$('.favorite-btn').on('click', handleFavorite);
