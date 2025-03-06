/*------------Canvas and background setup---------*/
let aitrigger = 0;//trigger for ai game mode
let	friendtrigger = 0;//trigger for online game mode
let clienttrigger = 0;
let trigger = 0;
let username;
let user_id;
let p1, p2;
let ball;
let hostname = "ye";
let width = 10;
let height = 30;
let maxBounceAngle = Math.PI / 3;
let speed = 1;
let refresh_rate = 10

function movep2(data)
{
	if (data.player_id != username)
	{
		p2.y = data.position.y;
	}
}

/*------------CLIENT-PLAYER-MOVEMENT----------------------------------------*/
function move_remote_ball(data)
{
	trigger = data.trigger;
	ball.dx = -data.ball.dx;
	ball.dy = data.ball.dy;
	ball.x += ball.dx;
	ball.y = data.ball.y;
	clienttrigger = 0;
	console.log("username : ", username, " hostname ", hostname, "trigger: ", trigger, "clienttrigger: ", clienttrigger, "friendtrigger: ", friendtrigger);
	if (p1.points != data.points.p1)
		p1.points = data.points.p1;
	if (p2.points != data.points.p2)
		p2.points = data.points.p2;

}
/*----------END-CLIENT-PLAYER-MOVEMENT-------------------------------------*/

document.addEventListener('DOMContentLoaded', () => {
	const canvas =  document.getElementById("TheGame");
	const ctx = canvas.getContext("2d");
/*----------------------END-SETUP--------------------------------------------------*/
	class Player {
		constructor(x, y) {
			this.x = x;
			this.y = y;
			this.points = 0;
		}

		movePlayer(y) {

			if ((y < 0 && this.y > 0) || (y > 0 && this.y < canvas.height - height))
			this.y += y;
		}

		drawPlayer() {
			ctx.fillStyle = "white";
			ctx.fillRect(this.x, this.y, width, height);
		}
	}


	class Ball {
		constructor(x, y, radius) {
			this.x = x;
			this.y = y;
			this.radius = radius;
			this.diameter = radius * 2;
			this.dx = 1;
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
				if (hostname != username)
					sendBallUpdate();

			}
				else if (this.isPlayerHit(p2)) {
					this.dx = -speed * Math.cos(this.calculate_bounceAngle(p2));
					this.dy = speed * Math.sin(this.calculate_bounceAngle(p2));
					if (hostname != username)
						sendBallUpdate();

			}
			else if (this.y - this.radius <= 0 || this.y + this.radius >= canvas.height)
				{
					this.dy *= -1;
				}
			else if ((this.x <= width / 2 || this.x >= canvas.width - width / 2) && (!this.isPlayerHit(p2) || !this.isPlayerHit(p1))) {
					if (this.x <= width / 2 )
					{
						if (p2.points < 10)
							p2.points++;
						this.dx = -1; // Reset speed
					}
					else
					{
						if (p1.points < 10)
							p1.points++;
						this.dx = 1;
					}

					this.x = canvas.width / 2; // Reset ball to center
					this.y = canvas.height / 2;
					this.dy = 0;
					trigger = 0;
					if (hostname != username)
						sendBallUpdate();		
				}
			this.x += this.dx;
			this.y += this.dy;
			this.drawBall();
		}
	}

	p1 = new Player(10, canvas.height/2);
	p2 = new Player(canvas.width - (width * 2), canvas.height/2);
	ball = new Ball(canvas.width / 2, canvas.height / 2, 5);

	/*------------------------------KEY-TRACKING---------------*/
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

	function movement() {
	
		if (keys["z"] || keys["w"]) {
			p1.movePlayer(-(speed));
			if (friendtrigger === 1) 
				sendPlayerUpdate();
		}
		if (keys["s"]) {
			p1.movePlayer(speed);
			if (friendtrigger === 1)
				sendPlayerUpdate();
		}
		if (keys[" "] && (aitrigger === 1 || (friendtrigger === 1 && username != hostname)) && trigger === 0)
		{
			trigger = 1;
			sendBallUpdate();
		}
		if (aitrigger === 1 && ball.x >= canvas.width / 2 && ball.dx > 0 && trigger === 1)
			aiBot();
	}
	/*----------------------------END-KEY-TRACKING---------------*/

	function aiBot() {
		if (ball.y <= (p2.y + height / 2))
			p2.movePlayer(-(speed));
		else if (ball.y > (p2.y + height / 2))
			p2.movePlayer(speed);
	}
	
	function reInitialize()
	{
		let TheGame = document.getElementById('TheGame');
		let scoreboard = document.getElementById('scoreboard');
		let winText = document.getElementById('winText');
		let winner = document.getElementById('winner');

		TheGame.classList.remove('active');
		scoreboard.classList.remove('active');
		if (p1.points === 10)
			winText.innerText += "Player one won !";
		else
		winText.innerText += "Player two won !";
		winner.classList.add('active');
		ball.x = canvas.width / 2;
		ball.y = canvas.height / 2;
		p1.y = canvas.height / 2;
		p2.y = canvas.height / 2;
		p2.points = 0;
		p1.points = 0;
		trigger = 0;
	}

	function drawFrame() {
		ctx.clearRect(0, 0, canvas.width, canvas.height);
		ctx.fillStyle = "black";
		ctx.fillRect(0, 0, canvas.width, canvas.height);
		ball.drawBall();
		p1.drawPlayer();
		p2.drawPlayer();

		if (is_in_bottom === 0)
			movement();
		if (trigger === 1 && (aitrigger === 1 || (friendtrigger === 1 && hostname != username)))// to change on setup
				ball.moveBall(p1, p2);
		if (trigger === 1 && friendtrigger === 1 && hostname === username && clienttrigger === 0)
			ball.moveBall(p1, p2);
		if (p1.points === 10 || p2.points == 10)
			reInitialize();
		document.getElementById("p1-points").innerText = p1.points;
		document.getElementById("p2-points").innerText = p2.points;

		requestAnimationFrame(drawFrame);
	}
	drawFrame();
/*---------------------HOST-MOVEMENT-------------------------------------------------------------------------*/
	function sendPlayerUpdate() {
		if (window.mySocket.readyState === WebSocket.OPEN) {
			const sending_data = {
				type: "movement",
				player_id: document.getElementById('username').innerText,
				position: {y: p1.y },
				target_group: "user_" + user_id,
			};
			window.mySocket.send(JSON.stringify(sending_data));
		} else
			console.warn("WebSocket not ready. State:", window.mySocket.readyState);
	}

	function sendBallUpdate()
	{
		if (window.mySocket.readyState === WebSocket.OPEN) {
			const sending_data = {
				type: "ball_movement",
				player_id: document.getElementById('username').innerText,
				ball: {x: ball.x, y: ball.y, dx: ball.dx, dy: ball.dy},
				points: {p1: p1.points, p2: p2.points},
				target_group: "user_" + user_id,
				trigger: trigger,
			};
	
			//console.log("Sending WebSocket message:", JSON.stringify(data));
			window.mySocket.send(JSON.stringify(sending_data));
		}
		else
			console.warn("WebSocket not ready. State:", window.mySocket.readyState);
	}
/*----------------END-HOST-MOVEMENT-------------------------------------------------------------------------*/

})