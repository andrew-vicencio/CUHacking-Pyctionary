var hand;
var c;
var cc;
var hs;
var lvl;
var success;
var collision;
var background;
var sT;
var time;
var yay;
var aww;
var theme;

window.onload=function() {
  cInit();
  bkgrndInit();
  pInit();
  uiInit();

  // yay = document.createElement("AUDIO");
  // aww = document.createElement("AUDIO");
  // theme = document.createElement("AUDIO");
  //
  // aww.src = "C:\Users\avice\Documents\Github\CUHacking\CUHacking-Pyctionary\website\music\The Price is Right Losing Horn - Gaming Sound Effect (HD).mp3"
  // yay.src = "C:\Users\avice\Documents\Github\CUHacking\CUHacking-Pyctionary\website\music\MLG Air Horn Sound Effect FREE.mp3"
  // theme.src = "C:\Users\avice\Documents\Github\CUHacking\CUHacking-Pyctionary\website\music\Jeopardy Theme.mp3"
  // theme.autoplay = true;
  // theme.loop = true;

  setInterval(update, 1000/24);
  setInterval(getPoints, 1000/24);
  // c.addEventListener('mousemove', function(e) {
  //   var rect = c.getBoundingClientRect();
  //   hand.x = (e.clientX-rect.left)/(rect.right-rect.left)*c.width;
  //   hand.y = (e.clientY-rect.top)/(rect.bottom-rect.top)*c.height;
  // });
}

function cInit() {
  c=document.getElementById('canvas'); //gets the Canvas Element
  cc=c.getContext('2d'); //gets the Rendering Context for the Canvas Element i.e. how you want it to draw on the canvas
  //c dimensions
  c.width = 640;
  c.height = 480;
  //cc font-size
  cc.font="50px Georgia";
}

function bkgrndInit() {
  background = new Image();
  background.width = 640;
  background.height = 480;
  background.src ="file:///C:/Users/avice/Documents/Github/CUHacking/CUHacking-Pyctionary/website/images/maze.png";
}

function pInit() {
  hand = {x: c.width-hs/2, y: hs/2};
  hs = 10;

  cc.lineWidth=10;
  cc.strokeStyle='white';
  cc.beginPath();
  cc.moveTo(hand.x, hand.y);
}

function uiInit() {
  sT = performance.now();
  lvl = 1;
  collision = false;
  success = false;
}

function getPoints() {
        $.ajax({
            type: "POST",
            contentType: "application/json; charset=utf-8",
            url: "/getpts",
            success: function(data) {
                hand.x = data.x;
                hand.y = data.y;
                collision = data.w;
            }
        });
}

function update() {
  cc.fillStyle='white';
  cc.drawImage(background, 0, 0);
  // cc.fillText("Level: " + lvl, 3*c.width/5, c.height - 25);

  if (!success){
    cc.font="50px Georgia"
    time = Math.floor((performance.now() - sT) / 1000);
    cc.fillText("Time: " + time, c.width/2 - 100, 50);
  } else {
    cc.fillText("You won in " + time + "seconds!", c.width/2 - 80, 50);
    lvl = 1;
  }

  if (!collision){
    cc.fillStyle='black';
    cc.fillRect(hand.x-hs/2, hand.y-hs/2, hs, hs);
    cc.lineTo(hand.x, hand.y);
    cc.stroke();
  } else {
    cc.font="25px Georgia"
    cc.fillText("You lost! Next map loading in " + (2 - time), c.width/2 - 165, c.height-25);
    setTimeout(changeBackground, 2000);
  }
}

function changeBackground() {
  background.src="file:///C:/Users/avice/Documents/Github/CUHacking/CUHacking-Pyctionary/website/images/maze1.png";
  uiInit();
  collision = false;
  sT = performance.now();
  time = time;
}
