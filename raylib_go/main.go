package main

import (
	"math"

	rl "github.com/gen2brain/raylib-go/raylib"
)

type Ball struct {
	X, Y    float32
	radius  float32
	speedX  float32
	speedY  float32
	gravity float32
	damping float32
	color   rl.Color
}

func (b *Ball) Update(screenWidth, screenHeight int32) {
	b.X += b.speedX
	b.speedY += b.gravity
	b.Y += b.speedY

	if b.X-b.radius <= 0 {
		b.X = b.radius
		b.speedX *= -1
		b.speedX *= b.damping
	}
	if b.X+b.radius >= float32(screenWidth) {
		b.X = float32(screenWidth) - b.radius
		b.speedX *= -1
		b.speedX *= b.damping
	}
	if b.Y-b.radius <= 0 {
		b.Y = b.radius
		b.speedY *= -1
	}
	if b.Y+b.radius >= float32(screenHeight) {
		b.Y = float32(screenHeight) - b.radius
		b.speedY *= b.damping
		b.speedY *= -1
	}
}

func (b *Ball) Draw() {
	rl.DrawCircle(int32(b.X), int32(b.Y), b.radius, b.color)
}

type Game struct {
	screenWidth  int32
	screenHeight int32
	Ball         Ball
}

func (g *Game) Update() {
	g.Ball.Update(g.screenWidth, g.screenHeight)
}

func (g *Game) Draw(screenWidth int32, screenHeight int32) {
	rl.BeginDrawing()
	rl.ClearBackground(rl.LightGray)

	rl.DrawText("Press Space to Bounce Ball", screenWidth/2-(rl.MeasureText("Press Space to Bounce Ball", 20)/2), screenHeight/2, 20, rl.Black)
	g.Ball.Draw()

	rl.EndDrawing()
}

func main() {
	screenWidth := int32(800)
	screenHeight := int32(450)

	rl.SetTargetFPS(60)

	rl.InitWindow(screenWidth, screenHeight, "BallTest")
	defer rl.CloseWindow()

	game := Game{
		screenWidth:  screenWidth,
		screenHeight: screenHeight,
		Ball: Ball{
			X:       float32(screenWidth / 2),
			Y:       float32(screenHeight / 2),
			speedX:  8.0,
			speedY:  0.0,
			gravity: 0.8,
			damping: 0.9,
			radius:  25.0,
			color:   rl.Red,
		},
	}

	for !rl.WindowShouldClose() {
		if rl.IsKeyPressed(rl.KeySpace) {
			game.Ball.speedY = -20
			if game.Ball.speedX > 0 {
				game.Ball.speedX += 3
			} else {
				game.Ball.speedX += -3
			}
		}
		if math.Abs(float64(game.Ball.speedY)) < 0.2 {
			game.Ball.speedY = 0
		}
		game.Update()
		game.Draw(screenWidth, screenHeight)
	}
}
