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

async function handleFavoriteReview(event) {
  const id = $(event.target).parent().data('id');
  if (event.target.className === 'far fa-heart') {
    await axios.post(`/favorite/review/${id}`).then(function (response) {
      console.log(response);
    });
    $(event.target).attr('class', 'fas fa-heart');
  } else if (event.target.className === 'fas fa-heart') {
    await axios.delete(`/favorite/review/${id}`).then(function (response) {
      console.log(response);
    });
    $(event.target).attr('class', 'far fa-heart');
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
  if (event.target.className === 'edit-btn') {
    $(event.target).parent().parent().next().toggleClass('show');
    editRatingsContainer = $(event.target)
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
  if ($(event.target).hasClass('fa-star')) {
    const i = $(this).find('.star-ratings').children();
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

function handleEditStars(event) {
  if ($(event.target).hasClass('fa-star')) {
    const i = $(this).find('.edit-ratings').children();
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
  let today = new Date()
    .toISOString()
    .slice(0, 19)
    .replace('T', ' ')
    .split(' ')[0];
  review_data = {
    rating: currentStar,
    review: review,
    restaurant_id: window.location.pathname.split('/').pop(),
    created_at: today,
  };
  await axios
    .post('/review', review_data)
    .then((res) => {
      if (res.data == '/login') {
        window.location = res.data;
      } else if (res.data.success) {
        generateReview(res.data, generateStars(currentStar), review_data);
      }
    })
    .catch((res) => {
      console.log(res);
    });
  $('.review-comment').removeClass('show');
  $('.review-btn').text('Write A Review');
  rating = 0;
  $('#restaurant-review').val('');
  $('.star-ratings i').each(() => {
    $('.star-ratingsi').attr('class', 'far fa-star');
  });
}

function handleEditReview(event) {
  if (event.target.className === 'edit-btn') {
    $(this)
      .find('#edit-form')
      .on('submit', async function (event) {
        event.preventDefault();
        currentStar = rating;
        let review = $('#edit-restaurant-review').val();
        let today = new Date()
          .toISOString()
          .slice(0, 19)
          .replace('T', ' ')
          .split(' ')[0];
        reviewItem = $(this).closest('.review-item').data('id');
        data = {
          rating: currentStar,
          review: review,
          created_at: today,
        };

        await axios
          .patch(`/review/${reviewItem}`, data)
          .then((res) => {
            if (res.data == '/login') {
              window.location = res.data;
            } else {
              const reviewerStars = $(event.target)
                .parent()
                .parent()
                .find('.reviewer-stars')
                .empty();
              const comment = $(event.target)
                .parent()
                .parent()
                .find('.comment');
              $(comment).text(res.data.review);
              for (let i = 0; i < res.data.rating; i++) {
                reviewerStars.append('<i class="fa fa-star checked mg-r"></i>');
              }
            }
          })
          .catch((res) => {
            console.log(res);
          });

        $('.edit-review').removeClass('show');
      });
  }
}

async function deleteReview(event) {
  if (event.target.className === 'delete-btn') {
    const reviewID = $(event.target).closest('.review-item').data('id');
    const reviewContainer = $(event.target).closest('.review-item');
    await axios.delete(`/review/${reviewID}`).catch((res) => {
      if (res.data == '/login') {
        window.location = res.data;
      } else {
        $(reviewContainer).remove();
      }
    });
  }
}

function generateReview(data, generateStars, review_data) {
  const $reviewContainer = $('#review-items');
  let new_review = `
    <div data-id="${data.review_id}" class="review-item">
      <div class="review_user">
          <div class="user_image">
              <img class="reviewer-image" src="https://prospectdirect.com/wpstagemct/wp-content/uploads/2017/05/generic-profile-photo-3.jpg">
          </div>
          <div class="review-content">
            <div class="reviewer-details">
                <span class="reviewer-name">${data.user.first_name} ${
    data.user.last_name
  }</span>
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
                <span class="comment">"${review_data.review}"</span>
            </div>
        </div>
      </div>
      <div class="review-buttons">
      <div class="edit-button">
          <li class="edit-btn">Edit Review</li>
      </div>
      <div class="delete-button">
          <li class="delete-btn">Delete<i class="fas fa-trash"></i></li>
      </div>
    </div>
    <div class="edit-review">
      <form id="edit-form" method="GET" action="/">
          <div class="edit-ratings">
              ${generateEditStars(review_data.rating)}
          </div>
          <textarea id="edit-restaurant-review" maxlength="180" class="form-control" rows="3" placeholder="Edit Your Review">${
            review_data.review
          }</textarea>
          <p class="max-char">Max 180 Characters</p>
          <input class="review-btn add" type="submit" value="Edit">
      </form>
    </div>
  </div>
 
  `;

  $($reviewContainer).prepend(new_review);
}

function generateEditStars(rating) {
  stars = '';
  for (let i = 0; i < 5; i++) {
    if (i <= rating - 1) {
      stars += "<i class='fas fa-star'></i>";
    } else {
      stars += "<i class='far fa-star'></i>";
    }
  }
  return stars;
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
$('#review-items').on('click', showEditSection);
$('#review-form').on('submit', handleReview);
$('#review-items').on('click', handleEditReview);
$('.review-comment').on('click', handleStars);
$('#review-items').on('click', handleEditStars);
$('#review-items').on('click', deleteReview);
$('#review-items').on('click', handleFavoriteReview);
