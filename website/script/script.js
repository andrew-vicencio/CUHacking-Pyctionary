var hand;
var c;
var cc;
var hs;
var arr;
var score;
var lvl;
var succ;
var backgrond;
var date;
var sT;

window.onload=function() {
  cInit();
  bkgrndInit();
  pInit();
  uiInit();

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
  cc.font="50px Georgia"
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
  score = 0;
  lvl = 0;
  sT = performance.now();
  // window.alert(date.getTime());
}

function getPoints() {
        $.ajax({
            type: "POST",
            contentType: "application/json; charset=utf-8",
            url: "/getpts",
            success: function(data) {
                hand.x = data.x;
                hand.y = data.y;
            }
        });
}

function update() {
  cc.fillStyle='white';
  // cc.fillRect(0, 0, c.width, c.height);
  cc.drawImage(background, 0, 0);
  cc.fillText("Score: " + score, c.width/8, c.height - 25);
  cc.fillText("Level: " + lvl, 3*c.width/5, c.height - 25);
  if (!succ){
    cc.fillText("Time: " + Math.floor((performance.now() - sT) / 1000), c.width/2 - 100, 50);
  }

  cc.fillStyle='black';
  // cc.fillRect(left.x-hs/2, left.y-hs/2, hs, hs);
  cc.fillRect(hand.x-hs/2, hand.y-hs/2, hs, hs);
  cc.lineTo(hand.x, hand.y);
  cc.stroke();
}

function changeBackground() {
  background.src="";
}
