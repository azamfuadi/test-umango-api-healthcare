function displayPaperCutToken() {
  var x = document.getElementById("ppc-token");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}

function displayHiddenValue(id) {
  var x = document.getElementById(id);
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}

function displayPaypayAPISecret() {
  var x = document.getElementById("paypay_api_secret");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}

function displayPaypayMerchantId() {
  var x = document.getElementById("paypay_merchant_id");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}

function setCheckboxValue() {
  var paypayChecked = document
    .getElementById("paypay_enabled")
    .getAttribute("checked");
  console.log(paypayChecked);
}

function changeFileInputText(input) {
  let file_Name_Display = document.getElementById("fileNameDisplay");
  if (input.files.length > 0) {
    file_Name_Display.innerText = input.files[0].name;
  }
}

function removeUrlMessage() {
  window.location = window.location.href.split("?")[0];
}

$(document).on("click", ".open-EditPrice", function () {
  var price = $(this).data("price");
  var points = $(this).data("points");
  var id = $(this).data("id");
  document.getElementById("new_price").value = price;
  document.getElementById("new_points").value = points;
  document.getElementById("price_id").value = id;
  document.getElementById("pricing_form").action = "/update-price";
});

$(document).on("click", ".open-DeletePrice", function () {
  var id = $(this).data("id");
  var price = $(this).data("price");
  var points = $(this).data("points");
  document.getElementById("selected_price_id").value = id;
  document.getElementById("selected_price").value = price;
  document.getElementById("selected_points").value = points;
});

$("#multipleAccountCheckbox").change(function () {
  if ($(this).is(":checked")) {
    // $("#personalAccountTargetForm").show();
    document.getElementById("personalAccountTargetForm").style.display =
      "block";
    document.getElementById("personalAccountCharge").value = "Y";
  } // checked
  else {
    // $("#personalAccountTargetForm").hide();
    document.getElementById("personalAccountTargetForm").style.display = "none";
    document.getElementById("personalAccountCharge").value = "N";
  }
});

$(document).ready(function () {
  const element = $("#alertModal");
  if (element) {
    element.modal("show");
    element.on("hidden.bs.modal", function (e) {
      // Perform actions here after the modal has completely hidden,
      removeUrlMessage();
    });
  }
});
