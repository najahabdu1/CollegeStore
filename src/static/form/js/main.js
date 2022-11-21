(function ($) {
  "use strict";

  /*==================================================================
    [ Focus Contact2 ]*/
  $(".input2").each(function () {
    if ($(this).val().trim() != "") {
      $(this).addClass("has-val");
    } else {
      $(this).removeClass("has-val");
    }
    $(this).on("blur", function () {
      if ($(this).val().trim() != "") {
        $(this).addClass("has-val");
      } else {
        $(this).removeClass("has-val");
      }
    });
  });

  /*==================================================================
    [ Validate ]*/
  var product = $('.validate-input input[name="product"]');
  var description = $('.validate-input input[name="description"]');
  var price = $('.validate-input input[name="price"]');
  var quantity = $('.validate-input input[name="quantity"]');
  var image = $("#img");

  $(".validate-form").on("submit", function () {
    var check = true;

    if ($(product).val().trim() == "") {
      showValidate(product);
      check = false;
    }

    if ($(description).val().trim() == "") {
      showValidate(description);
      check = false;
    }

    if (
      $(price)
        .val()
        .trim()
        .match(/^\d*[0-9](|.\d*[0-9]|,\d*[0-9])?$/) == null
    ) {
      showValidate(price);
      check = false;
    }

    if (
      $(quantity)
        .val()
        .trim()
        .match(/^\d*[0-9](|.\d*[0-9]|,\d*[0-9])?$/) == null
    ) {
      showValidate(quantity);
      check = false;
    }

    if ($(image).val() == "") {
      showValidate(image);
      check = false;
    }

    return check;
  });

  $(".validate-form .input2").each(function () {
    $(this).focus(function () {
      hideValidate(this);
    });
  });

  function showValidate(input) {
    var thisAlert = $(input).parent();

    $(thisAlert).addClass("alert-validate");
  }

  function hideValidate(input) {
    var thisAlert = $(input).parent();

    $(thisAlert).removeClass("alert-validate");
  }
})(jQuery);

// productUpdation image preview change
function changeImg(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();

    reader.onload = function (e) {
      $("#preview").attr("src", e.target.result);
      $("#preview").attr("hidden", false);
    };

    reader.readAsDataURL(input.files[0]);
  }
}

$("#img").change(function () {
  if ($("#img").val() == "") {
    $(this).removeClass("has-val");
    $("#preview").attr("hidden", true);
  } else {
    $(this).addClass("has-val");
    changeImg(this);
  }
});
