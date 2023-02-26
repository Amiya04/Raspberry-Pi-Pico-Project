from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from machine import Pin, PWM
import time


# Passive piezo buzzer connected to pin GP18
buzzer = PWM(Pin(18))

# Play an A5 note (=440 Hz) for one second
buzzer.duty_u16(16384) # 16384 = 25% duty cycle
buzzer.freq(440)       # A5 = 440 Hz
time.sleep(1)
buzzer.duty_u16(0)



# Init I2C using pins GP14 & GP15
i2c = I2C(1, scl = Pin(15), sda = Pin(14), freq = 400000)

# Init oled display
WIDTH  = 128 # oled display width in pixels
HEIGHT = 64  # oled display height in pixels
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

# Left and right push buttons connected to GP4 and GP5
left = Pin(4, Pin.IN, Pin.PULL_UP)
right = Pin(5, Pin.IN, Pin.PULL_UP)

# coordinates of the paddle on the screen in pixels
# the screen is 128 pixels wide by 64 pixel high
xp = 60 
yp = 60

# Simple Pong
x = 64 # ball coordinates on the screen in pixels
y = 0
vx = 2 # ball velocity along x and y in pixels per frame
vy = 2
    
while True:
    # Clear the screen
    oled.fill(0)
    
    # Draw a 4x4 pixels ball at (x,y) in white
    oled.fill_rect(x, y, 4, 4, 1)
    oled.show()
    
    # Move the ball by adding the velocity vector
    x += vx
    y += vy
    
    # Make the ball rebound on the edges of the screen
    if x < 0:
        x = 0
        vx = -vx
    if y < 0:
        y = 0
        vy = -vy
    if x + 4 > 128:
        x = 128 - 4
        vx = -vx
    if y + 4 > 64:
        y = 64 - 4
        vy = -vy

# draw a 16x4 pixels paddle at coordinates (xp,yp)
    oled.fill_rect(xp, yp, 16, 4, 1)
    oled.show()
    
    if left.value() == 0:
        print("LEFT Button Pressed")
        xp = xp - 5 # Move the paddle to the left by 1 pixel
    elif right.value() == 0:
        print("RIGHT Button Pressed")
        xp = xp + 5 # Move the paddle to the right by 1 pixel
    
    time.sleep(0.001)