
import cv2
import numpy as np
import sys

file = sys.argv[1]
output = sys.argv[2]
img = cv2.imread(file)

grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

original_height, original_width = grayscale.shape[:2]
new_width = 125
aspect_ratio = new_width / original_width
new_height = int(original_height * aspect_ratio)

resized = cv2.resize(grayscale, (new_width, new_height))

pixels = []

for row in resized:
    row_pixels = []
    for char in row:
        match char:
            case char if char < 15:
                row_pixels.append("$")
            
            case char if 15 < char <= 30:
                row_pixels.append("8")

            case char if 30 < char <= 45:
                row_pixels.append("#")
            
            case char if 45 < char <= 60:
                row_pixels.append("h")

            case char if 60 < char <= 75:
                row_pixels.append("p")
            
            case char if 75 < char <= 90:
                row_pixels.append("Z")

            case char if 90 < char <= 105:
                row_pixels.append("L")

            case char if 105 < char <= 120:
                row_pixels.append("Y")
            
            case char if 120 < char <= 135:
                row_pixels.append("v")
            
            case char if 135 < char <= 150:
                row_pixels.append("r")

            case char if 150 < char <= 165:
                row_pixels.append("/")

            case char if 165 < char <= 180:
                row_pixels.append(")")
            
            case char if 180 < char <= 195:
                row_pixels.append("[")
            
            case char if 195 < char <= 210:
                row_pixels.append("_")

            case char if 210 < char <= 225:
                row_pixels.append(">")

            case char if 225 < char <= 240:
                row_pixels.append("I")

            case char if 240 < char <= 255:
                row_pixels.append("^")

            
    pixels.append(row_pixels)

print(pixels)


with open (output, 'a') as file:
    for row in pixels:
        chars = ' '.join(i for i in row)
        file.write(chars + '\n')

file.close


