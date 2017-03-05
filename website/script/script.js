var hand;
var c;
var cc;
var hs;
var arr;
var score;
var lvl;
var succ;

window.onload=function() {
  c=document.getElementById('canvas');
  cc=c.getContext('2d');
  hand = {x: c.width-50, y: 100};
  hs = 10;

  cc.beginPath();
  cc.moveTo(hand.x, hand.y);
  cc.lineWidth=10;
  cc.strokeStyle='white';

  setInterval(update, 1000/24);
  setInterval(getPoints, 1000/24);
  // c.addEventListener('mousemove', function(e) {
  //   var rect = c.getBoundingClientRect();
  //   right.x = (e.clientX-rect.left)/(rect.right-rect.left)*c.width;
  //   right.y = (e.clientY-rect.top)/(rect.bottom-rect.top)*c.height;
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
  cc.fillStyle='black';
  cc.fillRect(0, 0, c.width, c.height);

  cc.fillStyle='white';
  // cc.fillRect(left.x-hs/2, left.y-hs/2, hs, hs);
  cc.fillRect(hand.x-hs/2, hand.y-hs/2, hs, hs);
  cc.lineTo(hand.x, hand.y);
  cc.stroke();

}
