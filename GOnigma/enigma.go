package main

import "fmt"

var letters = []string{"A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"}
var rotor1 = map[string]string{
	"A": "Q",
	"B": "G",
	"C": "Z",
	"D": "U",
	"E": "N",
	"F": "S",
	"G": "V",
	"H": "E",
	"I": "K",
	"J": "B",
	"K": "X",
	"L": "C",
	"M": "T",
	"N": "M",
	"O": "A",
	"P": "D",
	"Q": "I",
	"R": "R",
	"S": "O",
	"T": "H",
	"U": "L",
	"V": "Y",
	"W": "P",
	"X": "J",
	"Y": "F",
	"Z": "W"}

func main() {
	fmt.Println(rotor1["A"])
}
