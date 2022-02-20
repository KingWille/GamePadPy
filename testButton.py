from gpiozero import Button
from signal import pause

button = Button(27)
button.wait_for_press()
print("Button is pressed")
