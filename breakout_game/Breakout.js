/*
 * File: Breakout.js
 * -----------------
 * This program implements the Breakout game.
 */
"use strict";

/* Constants */
const GWINDOW_WIDTH = 360;           /* Width of the graphics window      */
const GWINDOW_HEIGHT = 600;          /* Height of the graphics window     */
const N_ROWS = 10;                   /* Number of brick rows              */
const N_COLS = 10;                   /* Number of brick columns           */
const BRICK_ASPECT_RATIO = 4 / 1;    /* Width to height ratio of a brick  */
const BRICK_TO_BALL_RATIO = 3 / 2;   /* Ratio of brick width to ball size */
const BRICK_TO_PADDLE_RATIO = 2 / 3; /* Ratio of brick to paddle width    */
const BRICK_SEP = 2;                 /* Separation between bricks         */
const TOP_FRACTION = 0.1;            /* Fraction of window above bricks   */
const BOTTOM_FRACTION = 0.05;        /* Fraction of window below paddle   */
const N_BALLS = 3;                   /* Number of balls in a game         */
const TIME_STEP = 10;                /* Time step in milliseconds         */
const INITIAL_Y_VELOCITY = 3.0;      /* Starting y velocity downward      */
const MIN_X_VELOCITY = 1.0;          /* Minimum random x velocity         */
const MAX_X_VELOCITY = 3.0;          /* Maximum random x velocity         */
const CENTER_WORD = 150;            /* Centers the word                   */

/* Derived constants */
const BRICK_WIDTH = (GWINDOW_WIDTH - (N_COLS + 1) * BRICK_SEP) / N_COLS;
const BRICK_HEIGHT = BRICK_WIDTH / BRICK_ASPECT_RATIO;
const PADDLE_WIDTH = BRICK_WIDTH / BRICK_TO_PADDLE_RATIO;
const PADDLE_HEIGHT = BRICK_HEIGHT / BRICK_TO_PADDLE_RATIO;
const PADDLE_Y = (1 - BOTTOM_FRACTION) * GWINDOW_HEIGHT - PADDLE_HEIGHT;
const BALL_SIZE = BRICK_WIDTH / BRICK_TO_BALL_RATIO;

/* Main program */

/* Function: Breakout */
// This function creates the breakout game. The player uses a ball to knock down as many bricks
// as possible by using the walls and the paddle below. Once a ball hits a brick, the brick is
// eliminated. The player has three chances before the game is over.
function Breakout() {
    let gw = new GWindow(GWINDOW_WIDTH, GWINDOW_HEIGHT);
    // Create the paddle
    let paddle = new GRect((GWINDOW_WIDTH / 2) - (PADDLE_WIDTH / 2), PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT);
    paddle.setFilled(true);
    paddle.setColor("Black");
    gw.add(paddle);

    let vx = 0;
    let vy = 0;
    let timer = 0;
    let chances = 3;
    let numBricksRemaining = N_ROWS * N_COLS;

    /* Function: createBall */
    // This function uses GObject to create the circlular ball and places it at the center of the window.
    function createBall() {
        let ball = new GOval((GWINDOW_WIDTH - BALL_SIZE) / 2, (GWINDOW_HEIGHT - BALL_SIZE) / 2, BALL_SIZE, BALL_SIZE);
        ball.setFilled(true);
        ball.setColor("Black");
        return ball;
    }

    let ball = undefined;

    /* Function: movePaddle */
    // This function tracks the paddle's x coordinate and checks for the boundary of the paddle to ensure that
    // the paddle does not leave the edges of the screen such as the right and left boundaries.
    let movePaddle = function(e) {
        let paddlex = e.getX();

        // Make sure the paddle does not leave the edge of the screen
        let paddle_edge = paddlex - PADDLE_WIDTH / 2;

        // Check if the paddle extends beyond the right edge
        let rightBoundary = GWINDOW_WIDTH - BRICK_SEP - PADDLE_WIDTH;
        if (paddle_edge > rightBoundary) {
            paddle_edge = rightBoundary;
        }

        // Check if the paddle extends beyond the left edge
        if (paddle_edge < BRICK_SEP) {
            paddle_edge = BRICK_SEP;
        }

        paddle.setLocation(paddle_edge, PADDLE_Y);
    }

    // Set up the brick color and location
    let x0 = BRICK_SEP;
    let y0 = GWINDOW_HEIGHT * TOP_FRACTION;
    let color_list = ["Red", "Orange", "Green", "Cyan", "Blue"];
    for (let i = 0; i < N_ROWS; i++) {
        let color_index = Math.floor(i / 2) % color_list.length;
        for (let j = 0; j < N_COLS; j++) {
            let rect = new GRect(x0, y0, BRICK_WIDTH, BRICK_HEIGHT);
            rect.setFilled(true);
            gw.add(rect);
            rect.setColor(color_list[color_index]);
            x0 += BRICK_WIDTH + BRICK_SEP;
        }
        x0 = BRICK_SEP;
        y0 += BRICK_HEIGHT + BRICK_SEP;
    }

    /* Function: clickAction */
    // This function responds to mouse clicks. It recreates a ball once
    // a chance is used up, sets the initial velocity, and animates the
    // ball's movement.
    function clickAction(e) {
        if (chances === 0 || ball !== undefined) {
            return;
        }
        ball = createBall();
        gw.add(ball);
        vx = randomReal(MIN_X_VELOCITY, MAX_X_VELOCITY);
        if (randomChance()) {
            vx = -vx;
        }
        vy = INITIAL_Y_VELOCITY;
        timer = setInterval(moveBall, TIME_STEP);
    }

    /* Function: moveBall */
    // This function updates the position of the ball and checks for collisions between the edges
    // of the window, the padddle, and the bricks. If the ball collides with the right or left boundary,
    // then the ball bounces off in a vertical direction. If the ball hits a brick, the direction is reversed
    // and the brick is removed. The number of chances that a user is allowed is also tracked, starting with 3,
    // and each time that the user's ball hits the bottom of the screen, once chance is deducted.
    function moveBall() {
        let x = ball.getX();
        let y = ball.getY();
        x += vx;
        y += vy;

        ball.move(vx, vy);

        // Reverses the x direction if the ball hits the right boundary of the window
        if (x + BALL_SIZE > GWINDOW_WIDTH) {
            vx = -vx
        }

        // Reverses the x direction if the ball hits the left boundary of the window
        if (x < 0) {
            vx = -vx;
        }

        // Reverses the y direction if the ball hits the top boundary of the window
        if (y < 0) {
            vy =-vy;
        }

        // If the ball hits the bottom boundary, the ball is removed, the game resets, and a chance is deducted.
        if (y + BALL_SIZE > GWINDOW_HEIGHT) {
            chances--;
            gw.remove(ball);
            ball = undefined;
            clearInterval(timer);
            timer = 0;
            if (chances === 0) {
                let msg = new GLabel("YOU LOST!", (GWINDOW_WIDTH - CENTER_WORD) / 2, GWINDOW_HEIGHT / 2);
                msg.setFont("30px 'Times New Roman'");
                gw.add(msg);
            }
            return;
        }

        let collider = getCollidingObject();
        // Checks if the ball collides with the paddle or the bricks
        if (collider !== null) {
            if (collider === paddle) {
                vy = -vy;
            }
            else {
                numBricksRemaining--;
                if (numBricksRemaining === 0) {
                    let msg = new GLabel("YOU WON!", (GWINDOW_WIDTH - CENTER_WORD) / 2, GWINDOW_HEIGHT / 2);
                    msg.setFont("30px 'Times New Roman'");
                    clearInterval(timer);
                    gw.add(msg);
                }
                vy = -vy;
                gw.remove(collider);
            }
        }

    }

    /* Function: getCollidingObject */
    // This function detects and returns the object that the ball collides with.
    // It determines the collision based on the four corners of the ball (topLeft,
    // topRight, bottomLeft, and bottomRight). If there is a collision between the
    // ball and another object, then that object is returned. If there is no collision,
    // then the function returns null to indicate that the ball did not interact with another
    // object.
    function getCollidingObject() {
        let r = BALL_SIZE / 2;
        let x = ball.getX();
        let y = ball.getY();
        let topLeft = gw.getElementAt(x, y);
        let topRight = gw.getElementAt(x + 2 * r, y);
        let bottomLeft = gw.getElementAt(x, y + 2 * r);
        let bottomRight = gw.getElementAt(x + 2 * r, y + 2 * r);

        if (topLeft !== null) {
            return topLeft;
        }

        if (topRight !== null) {
            return topRight;
        }

        if (bottomLeft !== null) {
            return bottomLeft;
        }

        if (bottomRight !== null) {
            return bottomRight;
        }

        return null;
    }
    // Moves the ball
    gw.addEventListener("click", clickAction);
    gw.addEventListener("mousemove", movePaddle);
}
