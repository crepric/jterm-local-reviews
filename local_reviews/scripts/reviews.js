$(document).ready(configure_events);

function configure_events() {
  $('.likebutton').click(like_btn_clicked);
  $('.dislikebutton').click(dislike_btn_clicked);
  $('#btn_sort').click(sort_cards);
}

function like_btn_clicked(e) {
  var current_count_element = $(e.currentTarget.parentElement).find('.like_count');
  $.post('/ua/voteinc',
         {id: $(e.currentTarget).closest('article').data('id')},
         function (data) {
           current_count_element.text(data.likes);
         })
}

function dislike_btn_clicked(e) {
  var current_count_element = $(e.currentTarget.parentElement).find('.like_count');
  $.post('/ua/votedec',
         {id: $(e.currentTarget).closest('article').data('id')},
         function (data) {
           current_count_element.text(data.likes);
         })
}

// Needed for sorting. Could have used an anonymous function
function compare_reviews(a, b) {
 return parseInt($(a).find('.like_count').text()) - parseInt($(b).find('.like_count').text());
}

function sort_cards() {
  var list_of_reviews = $(".review").toArray();
  list_of_reviews.sort(compare_reviews);
  if ($('#chk_sorted_order_reverse').prop('checked')) {
    // Or I could have used a different compare function while sorting.
    list_of_reviews.reverse();
  }
  for (var i = 0; i < list_of_reviews.length; i++) {
    $(list_of_reviews[i]).detach();
  }
  var reviews_body = $("#reviews");
  // A slight bug of this approach is that entries with the same
  // count don't necessarily appear in the same order every time.
  for (var i = 0; i < list_of_reviews.length; i++) {
    $(list_of_reviews[i]).appendTo(reviews_body);
  }
}
