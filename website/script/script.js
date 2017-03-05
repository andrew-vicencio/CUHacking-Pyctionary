var hand;
var c;
var cc;
var hs;
var arr;
var score;
var lvl;
var succ;
var backgrond;

window.onload=function() {
  c=document.getElementById('canvas');
  cc=c.getContext('2d');
  c.width = 640;
  c.height = 480;

  background = new Image();
  background.width = 640;
  background.height = 480;
  background.src ="file:///C:/Users/avice/Documents/Github/CUHacking/CUHacking-Pyctionary/website/images/maze.png";
  // window.alert(background.src);
  hand = {x: c.width-50, y: 100};
  hs = 10;

  cc.lineWidth=10;
  cc.strokeStyle='white';
  cc.beginPath();
  cc.moveTo(hand.x, hand.y);

  setInterval(update, 1000/24);
  setInterval(getPoints, 1000/24);
  // c.addEventListener('mousemove', function(e) {
  //   var rect = c.getBoundingClientRect();
  //   hand.x = (e.clientX-rect.left)/(rect.right-rect.left)*c.width;
  //   hand.y = (e.clientY-rect.top)/(rect.bottom-rect.top)*c.height;
  // });
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
  // cc.fillStyle='black';
  // cc.fillRect(0, 0, c.width, c.height);
  cc.drawImage(background, 0, 0);

  cc.fillStyle='black';
  // cc.fillRect(left.x-hs/2, left.y-hs/2, hs, hs);
  cc.fillRect(hand.x-hs/2, hand.y-hs/2, hs, hs);
  cc.lineTo(hand.x, hand.y);
  cc.stroke();
}

function changeBackground() {
  background.src="";
}
