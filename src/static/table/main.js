$(".button").on("click", function (e) {
  e.preventDefault();
  id = $(this).attr("id");
  console.log(id);
  $(".detail." + id).toggleClass("open");
  $("html, body").toggleClass("open");
});

$(".close").on("click", function (e) {
  e.preventDefault();
  $("textarea[name^='textarea']").val("");
  $(".detail." + id).toggleClass("open");
  $("html, body").toggleClass("open");
});

$(document).ready(function () {
  $("#message").keydown(function () {
    if (event.keyCode == 13) {
      $("#submit").click();
      return false;
    }
  });
});
