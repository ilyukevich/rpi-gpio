# TM1638 playground

import tm1638
import time

# These are the pins the display is connected to. Adjust accordingly.
# In addition to these you need to connect to 5V and ground.

DIO = 17
CLK = 27
STB = 22

display = tm1638.TM1638(DIO, CLK, STB)

display.enable(0)

#display.send_char(0, 0b11110110)
#display.send_char(0, '9')

display.set_text(u'привет_habr', 0.5)

for i in range(5):
  for i in range(8):
    display.set_led(i, display.RED) 
    time.sleep(0.1)
  for i in reversed(range(8)):
    display.set_led(i, 0) 
    time.sleep(0.1)

print(display.get_buttons())

#display.send_char(2, 0b11111011)
#display.send_char(3, 0b11010110)
#display.send_char(4, 0b01010100)
#display.send_char(5, 0b11010001)
#display.send_char(6, 0b11010111)
