package main

import (
	"math/rand"

	rl "github.com/gen2brain/raylib-go/raylib"
)

// create a struct for our circle
type Circle struct {
	X, Y      float32
	radius    float32
	color     rl.Color
	speedx    float32
	speedy    float32
	gravity   float32
	dampening float32
	mass      float32
}

// method for moving our circle
func (c *Circle) Move(screenWidth int32, screenHeight int32) {
	c.X += c.speedx
	c.speedy += c.gravity
	c.Y += c.speedy

	if c.X-c.radius <= 0 {
		c.X = c.radius
		c.speedx *= -1
		c.speedx *= c.dampening
	}
	if c.X+c.radius >= float32(screenWidth) {
		c.X = float32(screenWidth) - c.radius
		c.speedx *= -1
		c.speedx *= c.dampening
	}
	if c.Y-c.radius <= 0 {
		c.Y = c.radius
		c.speedy *= -1
		c.speedy *= c.dampening

	}
	if c.radius+c.Y >= float32(screenHeight) {
		c.Y = float32(screenHeight) - c.radius
		c.speedy *= -1
		c.speedy *= c.dampening
	}

}

func (c *Circle) Check_Collision_Circles(other_circle Circle) (bool, rl.Vector2) {
	var self_pos rl.Vector2 = rl.NewVector2(c.X, c.Y)
	var other_pos rl.Vector2 = rl.NewVector2(other_circle.X, other_circle.Y)
	if rl.CheckCollisionCircles(self_pos, c.radius, other_pos, other_circle.radius) {
		var collisionVector rl.Vector2 = rl.Vector2Subtract(other_pos, self_pos)
		var normalizedVector rl.Vector2 = rl.Vector2Normalize(collisionVector)
		return true, normalizedVector
	} else {
		return false, rl.NewVector2(0, 0)
	}
}

func (c *Circle) Resolve_Collision_Circles(other *Circle, normal rl.Vector2) {
	// --- Step 1: Separate overlapping circles (positional correction) ---
	delta := rl.Vector2Subtract(
		rl.NewVector2(other.X, other.Y),
		rl.NewVector2(c.X, c.Y),
	)
	dist := rl.Vector2Length(delta)
	overlap := (c.radius + other.radius) - dist

	slop := float32(0.01)   // ignore tiny overlaps
	percent := float32(0.2) // correct only 20% per frame
	if overlap > slop {
		correction := rl.Vector2Scale(normal, (overlap/2)*percent)
		c.X -= correction.X
		c.Y -= correction.Y
		other.X += correction.X
		other.Y += correction.Y
	}

	// --- Step 2: Collision impulse (velocity response) ---
	v1 := rl.NewVector2(c.speedx, c.speedy)
	v2 := rl.NewVector2(other.speedx, other.speedy)

	relativeVel := rl.Vector2Subtract(v2, v1)
	velAlongNormal := rl.Vector2DotProduct(relativeVel, normal)

	// if moving apart, skip
	if velAlongNormal > 0 {
		return
	}

	e := float32(.8) // restitution (1 = bouncy, <1 = damped)
	j := -(1 + e) * velAlongNormal / 2.0
	impulse := rl.Vector2Scale(normal, j)

	c.speedx -= impulse.X
	c.speedy -= impulse.Y
	other.speedx += impulse.X
	other.speedy += impulse.Y

}

func Apply_Click_Force(c *Circle) {
	if rl.IsMouseButtonDown(rl.MouseButtonLeft) {
		var mousPos rl.Vector2 = rl.GetMousePosition()
		var cPos rl.Vector2 = rl.NewVector2(c.X, c.Y)
		var delta rl.Vector2 = rl.Vector2Subtract(cPos, mousPos)
		var distance float32 = rl.Vector2Length(delta)
		var normal rl.Vector2 = rl.Vector2Normalize(delta)
		var force rl.Vector2 = rl.Vector2Scale(normal, 1)
		if distance < 100 {
			c.speedx += force.X * (100 / distance)
			c.speedy += force.Y * (100 / distance)
		}
	}
}

func main() {
	//define Window size up our app
	const screenWidth int32 = 800
	const screenHeight int32 = 450
	const numBalls int32 = 300

	//set window size and fps of the app
	rl.InitWindow(int32(screenWidth), int32(screenHeight), "Drawing Example")
	defer rl.CloseWindow()
	rl.SetTargetFPS(60)

	var circles []Circle
	for i := 0; i < int(numBalls); i++ {
		c := Circle{
			X:         float32(rand.Intn(int(screenWidth-50)) + 25),
			Y:         float32(rand.Intn(int(screenHeight-50)) + 25),
			radius:    10,
			color:     rl.NewColor(uint8(rand.Intn(255)), uint8(rand.Intn(255)), uint8(rand.Intn(255)), 255),
			speedx:    rand.Float32()*6 - 3,
			speedy:    rand.Float32()*6 - 3,
			gravity:   0,
			dampening: 1,
		}
		circles = append(circles, c)
	}
	//event loop
	for !rl.WindowShouldClose() {
		rl.BeginDrawing()
		rl.ClearBackground(rl.RayWhite)
		for i := range circles {
			c := &circles[i]
			c.Move(screenWidth, screenHeight)
			Apply_Click_Force(c)
			for j := i + 1; j < len(circles); j++ {
				if hit, normal := c.Check_Collision_Circles(circles[j]); hit {
					c.Resolve_Collision_Circles(&circles[j], normal)
				}
			}
			rl.DrawCircle(int32(c.X), int32(c.Y), c.radius, c.color)
		}
		rl.DrawFPS(10, 10)
		rl.EndDrawing()

	}

}
