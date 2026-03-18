function changeSummary() {
  var desired_transaction = document.getElementById(
    "desired_transaction"
  ).value;
  const pointsByPrice = paymentConfig.find(
    (data) => data.price === desired_transaction
  );
  document.getElementById("obtained-point").textContent = pointsByPrice.points;
  document.getElementById("payment-amount").textContent = desired_transaction;
  document.getElementById("total-payment").textContent = desired_transaction;
}
