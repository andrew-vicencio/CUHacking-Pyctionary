var left;
var right;
var c;
var cc;
var hs;
var arr;

window.onload=function() {
  c=document.getElementById('canvas');
  cc=c.getContext('2d');
  left = {x: 0, y: 100};
  right = {x: c.width-50, y: 100};
  hs = 10;

  cc.beginPath();
  cc.moveTo(right.x, right.y);
  cc.lineWidth=10;
  cc.strokeStyle='white';

  setInterval(update, 1000/60);
  c.addEventListener('mousemove', function(e) {
    var rect = c.getBoundingClientRect();
    var oldx = right.x;
    var oldy = right.y;
    right.x = (e.clientX-rect.left)/(rect.right-rect.left)*c.width;
    right.y = (e.clientY-rect.top)/(rect.bottom-rect.top)*c.height;
  });
}

// function canvasStyle() {
//   d=document.getElementById('top');
//   c.width=100vw;
//   c.height=100vh;
// }

function update() {
  cc.fillStyle='black';
  cc.fillRect(0, 0, c.width, c.height);

  cc.fillStyle='white';
  cc.fillRect(left.x-hs/2, left.y-hs/2, hs, hs);
  cc.fillRect(right.x-hs/2, right.y-hs/2, hs, hs);
  cc.lineTo(right.x, right.y);
  cc.stroke();
}
