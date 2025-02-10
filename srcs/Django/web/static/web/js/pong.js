/*------------Canvas and background setup---------*/
let time = 0;
let aitrigger = 1;


//console.log("yes it does1");
document.addEventListener('DOMContentLoaded', (event) => {
	//console.log("yes it does2");
    const canvas = document.getElementById("TheGame");


    canvas.width = window.innerWidth * 90/100;
    canvas.height =  window.innerHeight* 50/100;
    const ctx = canvas.getContext("2d");

    // Le reste du code de ton jeu...


let width = 25;
let height = 100;
let maxBounceAngle = Math.PI / 3;
let speed = 10;

function getRandomArbitrary(min, max) {
  return Math.random() * (max - min) + min;
}
/*----------------------------------------------*/
class Ball {
  constructor(x, y, radius) {
    this.x = x;
    this.y = y;
    this.radius = radius;
    this.diameter = radius * 2;
    this.dx = 5;
    this.dy = 0;
  }

  isPlayerHit(p) {
    if (this.x + this.radius >= p.x && this.x - this.radius <= p.x + width &&
        this.y + this.radius >= p.y && this.y - this.radius <= p.y + height)
      return true;
    return false;
  }

  drawBall() {
    ctx.beginPath();
    ctx.fillStyle = "white";
    ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
    ctx.fill();
    ctx.closePath();
  }

  calculate_bounceAngle(paddle) {
    let intersectionY = this.y; // Point of intersection between the paddle and the ball
    let relativeIntersectY = (paddle.y + (height / 2)) - intersectionY; // Approximation of where the ball hit the paddle
    let normalizedRelativeIntersectionY = relativeIntersectY / (height / 2); // Normalize the relative intersection
    let bounceAngle = normalizedRelativeIntersectionY * maxBounceAngle;
    return bounceAngle;
  }

  moveBall(p1, p2) {
    ctx.beginPath();
    ctx.fillStyle = "black";
    ctx.arc(this.x, this.y, this.radius + 1, 0, Math.PI * 2);
    ctx.fill();
    ctx.closePath();

    if (this.isPlayerHit(p1)) {
      this.dx = speed * Math.cos(this.calculate_bounceAngle(p1));
      if (this.dx < 0)
        this.dx *= -1;
      this.dy = speed * Math.sin(this.calculate_bounceAngle(p1));
    } else if (this.isPlayerHit(p2)) {
      this.dx = -speed * Math.cos(this.calculate_bounceAngle(p2));
      this.dy = speed * Math.sin(this.calculate_bounceAngle(p2));
    } else if (this.y - this.radius <= 0 || this.y + this.radius >= canvas.height)
      this.dy *= -1;
    else if ((this.x <= 25 || this.x >= canvas.width - 25) && (!this.isPlayerHit(p2) || !this.isPlayerHit(p1))) {
      if (this.x <= 25)
        this.dx = -5; // Reset speed
      else
        this.dx = 5;
      this.x = canvas.width / 2; // Reset ball to center
      this.y = canvas.height / 2;
      this.dy = 0;
      trigger = 0;
    }
    this.x += this.dx;
    this.y += this.dy;
    this.drawBall();
  }
}

class Player {
  constructor(x, y) {
    this.x = x;
    this.y = y;
    this.points = 0;
  }

  movePlayer(y) {
    if ((y < 0 && this.y > 0) || (y > 0 && this.y < canvas.height - 100))
      this.y += y;
  }

  drawPlayer() {
    ctx.fillStyle = "white";
    ctx.fillRect(this.x, this.y, width, height);
  }
}

let p1 = new Player(10, canvas.height/2);
let p2 = new Player(canvas.width - 35, canvas.height/2);

let ball = new Ball(canvas.width / 2, canvas.height / 2, 10);

let trigger = 0;

// Track key states
const keys = {};

// Update key state on keydown
document.addEventListener('keydown', (event) => {
  keys[event.key] = true;
});

// Update key state on keyup
document.addEventListener('keyup', (event) => {
  keys[event.key] = false;
});



function calculate_delay() {
  if (aitrigger === 0)
    time++;
  if (time >= 350) {
    aitrigger = 1;
    time = 0;
  }
}

function movement() {
  if ((keys["z"] || keys["w"])) {
    p1.movePlayer(-(speed + 5));
  }
  if (keys["s"]) {
    p1.movePlayer(speed + 5);
  }
  if (keys["ArrowUp"]) {
    aitrigger = 0;
    p2.movePlayer(-(speed + 5));
  }
  if (keys["ArrowDown"]) {
    aitrigger = 0;
    p2.movePlayer(speed + 5);
  }
  calculate_delay();
  if (keys[" "])
    trigger = 1;
  if (aitrigger === 1 && ball.x >= canvas.width / 2 && ball.dx > 0 && trigger === 1)
    aiBot();
}

function aiBot() {
  if (ball.y <= (p2.y + height / 2) - 15)
    p2.movePlayer(-(speed - 5));
  else if (ball.y > (p2.y + height / 2) + 15)
    p2.movePlayer(speed - 5);
}

function drawFrame() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "black";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ball.drawBall();

  movement();
  if (trigger === 1)
    ball.moveBall(p1, p2);
  p1.drawPlayer();
  p2.drawPlayer();
  if (ball.x <= 25)
    p2.points++;
  if (ball.x >= canvas.width - 25)
    p1.points += 1;

  document.getElementById("p1-points").innerText = p1.points;
  document.getElementById("p2-points").innerText = p2.points;
  window.addEventListener("resize", resizeCanvas);
  requestAnimationFrame(drawFrame);
}

p1.drawPlayer();
p2.drawPlayer();

drawFrame();

/*---CANVAS-RESIZING---*/
function resizeCanvas()
{
	canvas.width = window.innerWidth * 0.90;
    canvas.height =  window.innerHeight* 50/100;
	p2.x = canvas.width - 35;
	p2. y = canvas.height/2;
	if (trigger === 0)
	{
		ball.x = canvas.width / 2;
		ball.y = canvas.height / 2;
	}
}
console.log(window.innerHeight);
});
