$(document).ready(configure_events);

function configure_events() {
  $('.likebutton').click(like_btn_clicked);
  $('.dislikebutton').click(dislike_btn_clicked);
  $('#btn_sort').click(sort_cards);
}

function like_btn_clicked(e) {
  var current_count_element = $(e.currentTarget.parentElement).find('.like_count');
  var current_count = parseInt(current_count_element.text())
  current_count_element.text(current_count + 1);
}

function dislike_btn_clicked(e) {
  var current_count_element = $(e.currentTarget.parentElement).find('.like_count');
  var current_count = parseInt(current_count_element.text())
  current_count_element.text(current_count - 1);
}

function compare_reviews(a, b) {
 return parseInt($(a).find('.like_count').text()) - parseInt($(b).find('.like_count').text());
}

function sort_cards() {
  var list_of_reviews = $(".review").toArray();
  list_of_reviews.sort(compare_reviews);
  if ($('#chk_sorted_order_reverse').prop('checked')) {
    list_of_reviews.reverse();
  }
  for (var i = 0; i < list_of_reviews.length; i++) {
    $(list_of_reviews[i]).detach();
  }
  var reviews_body = $("#reviews");
  for (var i = 0; i < list_of_reviews.length; i++) {
    $(list_of_reviews[i]).appendTo(reviews_body);
  }
}
