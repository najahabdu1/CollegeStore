//greeting
var user = document.getElementById("user").value;
var welcome;
var date = new Date();
var hour = date.getHours();
var minute = date.getMinutes();
var second = date.getSeconds();
if (minute < 10) {
  minute = "0" + minute;
}
if (second < 10) {
  second = "0" + second;
}
if (hour < 12) {
  welcome = "Good Morning";
} else if (hour < 17) {
  welcome = "Good Afternoon";
} else {
  welcome = "Good Evening";
}
document.write(welcome + " " + user);
