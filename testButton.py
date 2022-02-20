from gpiozero import Button
from signal import pause

button = Button(27)

while True:
    if button.is_pressed:
        print("Button is pressed")
    else:
        print("Button is not pressed")
        
pause()
