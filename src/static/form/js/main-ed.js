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
  var prd1 = $('.validate-input input[name="prd1"]');
  var prd2 = $('.validate-input input[name="prd2"]');
  var prd3 = $('.validate-input input[name="prd3"]');
  var prd4 = $('.validate-input input[name="prd4"]');
  // var message = $('.validate-input textarea[name="message"]');

  $(".validate-form").on("submit", function () {
    var check = true;

    if ($(prd1).val().trim() == "") {
      showValidate(prd1);
      check = false;
    }

    if ($(prd2).val().trim().match(/^\s*[a-zA-Z,\s]+\s*$/) == "") {
      showValidate(prd2);
      check = false;
    }

    if ($(prd3).val().trim().match(/^[0-9]{1,4}([.][0-9]{1,3})?$/) == null) {
      showValidate(prd3);
      check = false;
    }

    if ($(prd4).val().trim().match(/^\d*$/) == null) {
      showValidate(prd4);
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
    };

    reader.readAsDataURL(input.files[0]);
  }
}

$("#img").change(function () {
  if ($('#img').val() == '') {
    $(this).removeClass("has-val");
    $("#preview").attr("hidden", true);
    $("#default").attr("hidden", false);
  }
  else {
    $("#preview").attr("hidden", false);
    $("#default").attr("hidden", true);
    $(this).addClass("has-val");
    changeImg(this);
  }
});
