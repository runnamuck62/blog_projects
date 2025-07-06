import cv2
import numpy as np
import webbrowser


firefox = webbrowser.get('firefox')
cap = cv2.VideoCapture(0)
last_mean = 0
first_run = True
process_time = 0


while(True):
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    result = np.abs(np.mean(gray) - last_mean)
    print(result)
    last_mean= np.mean(gray)
    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break
    if process_time < 100:
        process_time += 1
        continue
    if result > 0.8:
        print("Motion detected!")
        firefox.open_new_tab('https://www.youtube.com/watch?v=53yPfrqbpkE&autoplay=1')
        break


cap.release()
cv2.destroyAllWindows()