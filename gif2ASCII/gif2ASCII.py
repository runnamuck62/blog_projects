import cv2
import numpy as np
import sys
from PIL import Image, ImageFont, ImageDraw
import os

#input and output files
file = sys.argv[1]
output = sys.argv[2]

#read image file and convert to grayscale
gif = cv2.VideoCapture(file)
frames = []
ret, frame = gif.read()


while ret:
    ret, frame = gif.read()
    if not ret:
        break

    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    #Scale image to 125px width
    original_height, original_width = grayscale.shape[:2]
    new_width = 75
    aspect_ratio = new_width / original_width
    new_height = int(original_height * aspect_ratio)
    resized = cv2.resize(grayscale, (new_width * 2, new_height))
    frames.append(resized)


text_frames = []

for frame in frames:
    pixels = []

    for row in frame:
        row_pixels = []
        for char in row:
            match char:
                case char if char <= 15:
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
    text_frames.append(pixels)

fnt = ImageFont.truetype("UbuntuMono-B.ttf", 9)
bbox = fnt.getbbox('A')
char_width = bbox[2]-bbox[0]
char_height = bbox[3]-bbox[1]
ascent, descent = fnt.getmetrics()
line_height = ascent + descent

padding_top = 5
padding_bottom = 5
img_height = line_height * new_height + padding_bottom + padding_top

padding_left = 5
padding_right = 5
img_width = char_width * (new_width * 2) + padding_left + padding_right

gif_frames = []
i = 0

for image in text_frames:
    final_image = '\n'.join(''.join(row) for row in image)

    # Measure exact text block
    temp_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(temp_img)
    bbox = draw.multiline_textbbox(
        (0, 0),
        final_image,
        font=fnt,
        spacing=0
    )
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    img_width = text_width + padding_left + padding_right
    img_height = text_height + padding_top + padding_bottom

    img = Image.new('RGB', (img_width, img_height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    draw.multiline_text(
        (padding_left, padding_top),
        final_image,
        font=fnt,
        fill=(0, 0, 0),
        spacing=0
    )
    gif_frames.append(img)
    i += 1
    print(f"converting frame {i} of {len(text_frames)}")
    
frame_one = gif_frames[0]
frame_one.save(output, format="GIF", append_images=gif_frames, save_all=True, duration=60, loop = 0)

