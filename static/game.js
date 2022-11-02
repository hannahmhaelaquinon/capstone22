//Add the array for the button color
var buttonColours = ["red", "blue", "green", "yellow"];
//Add the array for the auto generated pattern
var gamePattern = [];
//Add the array for the pattern clicked by the user
var userClickedPattern = [];

var started = false;
var level = 0;

//start the game
$(document).keypress(function() {
  if (!started) {
    $("#level-title").text("Level " + level);
    nextSequence();
    started = true;
  }
});

//checks what button the user clicks and calls the function to add sound,animate when pressed, and check answer
$(".btn").click(function() {

  var userChosenColour = $(this).attr("id");
  userClickedPattern.push(userChosenColour);
  //calls function to add sound, animate when press, and check answer
  playSound(userChosenColour);
  animatePress(userChosenColour);

  checkAnswer(userClickedPattern.length-1);
});

//Checks the array if the pattern pressed is the same with the generated one
function checkAnswer(currentLevel) {

    if (gamePattern[currentLevel] === userClickedPattern[currentLevel]) {
      if (userClickedPattern.length === gamePattern.length){
        setTimeout(function () {
          nextSequence();
        }, 1000);
      }
    } else {
      playSound("wrong");
      $("body").addClass("game-over");
      $("#level-title").text("Game Over, Press Any Key to Restart");

      setTimeout(function () {
        $("body").removeClass("game-over");
      }, 200);

      startOver();
    }
}

//Adds another level if  sequence is correct and when function is called
function nextSequence() {
  userClickedPattern = [];
  level++;
  $("#level-title").text("Level " + level);
  var randomNumber = Math.floor(Math.random() * 4);
  var randomChosenColour = buttonColours[randomNumber];
  gamePattern.push(randomChosenColour);

  $("#" + randomChosenColour).fadeIn(100).fadeOut(100).fadeIn(100);
  playSound(randomChosenColour);
}
//Button and background will change color when pressed 
function animatePress(currentColor) {
  $("#" + currentColor).addClass("pressed");
  setTimeout(function () {
    $("#" + currentColor).removeClass("pressed");
  }, 100);
}
//Adds sound effect to the game whwn button is pressed
function playSound(name) {
  var audio = new Audio("../../static/sounds/" + name + ".mp3");
  audio.play();
}
// restarts the game
function startOver() {
  level = 0;
  gamePattern = [];
  started = false;
}
