let rating = 0;

$(document).ready(function () {
  $('.js-fullheight').css('height', $(window).height());
  $(window).resize(function () {
    $('.js-fullheight').css('height', $(window).height());
  });

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

  $('.user-carousel').owlCarousel({
    loop: false,
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
});

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
    await axios.delete(`/favorite/${id}`).then(function (response) {
      if (response.data == '/login') {
        window.location = response.data;
      } else {
        $('.favorite-btn i').attr('class', 'far fa-heart');
      }
    });
  } else if ($('.favorite-btn i').hasClass('far fa-heart')) {
    await axios.post(`/favorite/${id}`).then(function (response) {
      if (response.data == '/login') {
        window.location = response.data;
      } else {
        $('.favorite-btn i').attr('class', 'fas fa-heart');
      }
    });
  }
}

function showReviewSection() {
  $('.review-comment').toggleClass('show');
  if ($('.review-comment').is(':visible')) {
    $(this).text('Cancel');
  } else {
    $(this).text('Write A Review');
  }
}

function showEditSection(event) {
  if ($(event.target).hasClass('edit-btn')) {
    $(this).parent().parent().next().toggleClass('show');
    editRatingsContainer = $(this)
      .parent()
      .parent()
      .next()
      .find('.edit-ratings i');
    currentStar = [];
    $(editRatingsContainer).each(function (index) {
      if (this.className == 'fas fa-star') {
        currentStar.push(this);
      }
    });
    rating = currentStar.length;
  }
}

function handleStars(event) {
  if ($(event.target).parent().hasClass('star-ratings')) {
    if ($(event.target).hasClass('fa-star')) {
      const i = $(this).children();
      $(i).each(function (index) {
        $(this).attr('class', 'far fa-star');
        if (event.target == this) {
          rating = index + 1;
          $(this).attr('class', 'fas fa-star');
          $(this).prevAll().attr('class', 'fas fa-star');
        }
      });
    }
  } else if ($(event.target).parent().hasClass('edit-ratings')) {
    const i = $(this).children();
    $(i).each(function (index) {
      $(this).attr('class', 'far fa-star');
      if (event.target == this) {
        rating = index + 1;
        $(this).attr('class', 'fas fa-star');
        $(this).prevAll().attr('class', 'fas fa-star');
      }
    });
  }
}

async function handleReview(event) {
  event.preventDefault();
  currentStar = rating;
  let review = $('#restaurant-review').val();
  let today = new Date().toLocaleDateString();
  data = {
    rating: currentStar,
    review: review,
    restaurant_id: window.location.pathname.split('/').pop(),
    created_at: today,
  };
  await axios
    .post('/review', data)
    .then((res) => {
      if (res.data.success) {
        generateReview(res.data, generateStars(currentStar), data.review);
      }
    })
    .catch((res) => {
      console.log(res);
    });
  $('.review-comment').removeClass('show');
  $('.review-btn').text('Write A Review');
  rating = 0;
  $('#restaurant-review').val('');
}

async function handleEditReview(event) {
  event.preventDefault();
  currentStar = rating;
  console.log(currentStar);
  let review = $('#edit-restaurant-review').val();
  let today = new Date().toLocaleDateString();
  reviewItem = $(this).closest('.review-item').data('id');
  data = {
    rating: currentStar,
    review: review,
    created_at: today,
  };
  await axios
    .patch(`/review/${reviewItem}`, data)
    .then((res) => {
      console.log(res);
    })
    .catch((res) => {
      console.log(res);
    });
  $('.edit-review').removeClass('show');
}

async function deleteReview(event) {}

function generateReview(data, generateStars, review) {
  const $reviewContainer = $('#review-items');
  let new_review = `
    <div data-id="${data.id}" class="review-item">
      <div class="review_user">
          <div class="user_image">
              <img class="reviewer-image" src="https://prospectdirect.com/wpstagemct/wp-content/uploads/2017/05/generic-profile-photo-3.jpg">
          </div>
          <div class="review-content">
            <div class="reviewer-details">
                <span class="reviewer-name">${data.user.first_name} ${data.user.last_name}</span>
                <span class="reviewer-location">${data.user.location}</span>
                <div class="reviewer-feed">
                    <i class="fas fa-comments"></i>
                    <span class="reviewer-total">${data.user.reviews}</span>
                </div>
            </div>
            <div class="reviewer-rating">
                <div class="reviewer-stars">
                    ${generateStars}
                </div>
                <div class="created">
                    <span class="created-date">${data.created_at}</span>
                </div>
            </div>
            <div class="reviewer-comment">
                <span class="comment">"${review}"</span>
            </div>
        </div>
      </div>
  </div>
  `;

  $($reviewContainer).prepend(new_review);
}

function generateStars(currentStar) {
  stars = '';
  for (i = 0; i < currentStar; i++) {
    stars += '<i class="fa fa-star checked"></i>';
  }
  return stars;
}

$('.favorite-btn').on('click', handleFavorite);
$('li.review-btn').on('click', showReviewSection);
$('.edit-btn').on('click', showEditSection);
$('.star-ratings').on('click', handleStars);
$('#review-form').on('submit', handleReview);
$('#edit-form').on('submit', handleEditReview);
$('.edit-ratings').on('click', handleStars);
