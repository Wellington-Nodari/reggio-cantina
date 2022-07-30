$(document).ready(function() {
var i = 2;
  $('.add').on('click', function() {
    var field = '<br><div>'+i+': <input placeholder="Select" list="menu" name="item" class="item" required>; <input placeholder="0" type="number" name="quantity" class="quantity" required>';
    $('.appending_div').append(field);
    i = i+1;
  })
})