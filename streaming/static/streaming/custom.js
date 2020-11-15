let degrees = 0;
let zoom = 1;
let img = $("#panop");

// Function to increase image size
function enlargeImg() {
  // Set image size to 1.5 times original
  img.style.transform = "scale(1.5)";
  // Animation effect
  img.style.transition = "transform 0.25s ease";
}
// Function to reset image size
function resetImg() {
  // Set image size to original
  img.style.transform = "scale(1)";
  img.style.transition = "transform 0.25s ease";
}

$(".rotate").click(function rotateMe(e) {
  degrees += 90;
  $("#panop").css({
    transform: "rotate(" + degrees + "deg)",
    "-ms-transform": "rotate(" + degrees + "deg)",
    "-moz-transform": "rotate(" + degrees + "deg)",
    "-webkit-transform": "rotate(" + degrees + "deg)",
    "-o-transform": "rotate(" + degrees + "deg)",
  });
});

$(".reset").click(function rotateMe(e) {
  img = document.getElementById("panop");
  img.style.transform = "scale(1)";
  img.style.transition = "transform 0.25s ease";
});

$(".zoom-in").click(function rotateMe(e) {
  img = document.getElementById("panop");
  zoom += 0.1;
  img.style.transform = "scale(" + zoom + ")";
  img.style.transition = "transform 0.25s ease";
});

$(".zoom-out").click(function rotateMe(e) {
  img = document.getElementById("panop");
  zoom -= 0.1;
  img.style.transform = "scale(" + zoom + ")";
  img.style.transition = "transform -0.25s ease";
});
