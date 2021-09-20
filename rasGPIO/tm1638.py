import RPi.GPIO as GPIO
from time import sleep
import threading
import os
#from multiprocessing import Process


class TM1638(object):
    """info"""

    GREEN = 2
    RED = 1
    NONE = 0
    text_delay = 0.3
    pio = 0
    sw_callback = 0
    FONT = {
        '0': 0b111111,
        '1': 0b110,
        '2': 0b1011011,
        '3': 0b1001111,
        '4': 0b1100110,
        '5': 0b1101101,
        '6': 0b1111101,
        '7': 0b111,
        '8': 0b1111111,
        '9': 0b1101111,
        'a': 0b1110111,
        'b': 0b1111100,
        'c': 0b111001,
        'd': 0b1011110,
        'e': 0b1111001,
        'f': 0b1110001,
        'g': 0b111101,
        'h': 0b1110100,
        'i': 0b110000,
        'j': 0b1110,
        'k': 0b1110101,
        'l': 0b111000,
        'n': 0b1010100,
        'o': 0b111111,
        'p': 0b1110011,
        'q': 0b1100111,
        'r': 0b1010000,
        's': 0b1101101,
        't': 0b1111000,
        'u': 0b111110,
        'v': 0b111110,
        'y': 0b1101110,
        #rus
	    u'а': 0b1110111, 
        u'б': 0b1111101,
        u'в': 0b1111100,
        u'г': 0b110001, 
        u'е': 0b1111001,
        u'з': 0b1001111,
        u'и': 0b11100,
        u'й': 0b11101,
        u'к': 0b1110101,
        u'л': 0b110111,
        u'м': 0b101011,
        u'н': 0b111011,
        u'о': 0b111111,
        u'п': 0b1010100,
        u'р': 0b1110011,
        u'с': 0b1011000,
        u'т': 0b111,
        u'у': 0b1101110,
        u'ч': 0b1101010,
        u'ы': 0b1111110,
        u'ь': 0b1111100,
        u'э': 0b1001111,      
        u'я': 0b1100111,
        # 
         '!': 0b10000110,
         '-': 0b1000000,
         '=': 0b1001000,
         '?': 0b10000111,
         '_': 0b1000,
         "'": 0b10,
         ' ' : 0,        
    }

    def __init__(self, dio, clk, stb):
        self.dio = dio
        self.clk = clk
        self.stb = stb
    
    def __del__(self):
        GPIO.cleanup()
    #returns gpio object

    def enable(self, intensity=7):
        self.gpio = GPIO
        self.gpio.setmode(GPIO.BCM)
        self.gpio.setwarnings(0)
        self.gpio.setup(self.dio, GPIO.OUT)
        self.gpio.setup(self.clk, GPIO.OUT)
        self.gpio.setup(self.stb, GPIO.OUT)
        
        self.gpio.output(self.stb, 1)
        self.gpio.output(self.clk, 1)

        self.send_command(0x40)
        self.send_command(0x88 | 7&intensity)
        return self.gpio

    def send_command(self, cmd):
        GPIO.output(self.stb, 0)
        self.send_byte(cmd)
        GPIO.output(self.stb, 1)

    def send_data(self, addr, data):
        self.send_command(0x44)
        GPIO.output(self.stb, 0)
        self.send_byte(0xC0 | addr)
        self.send_byte(data)
        GPIO.output(self.stb, 1)

    def send_byte(self, data):
        for i in range(8):
            GPIO.output(self.clk, 0)
            GPIO.output(self.dio, (data & 1) == 1)
            data >>= 1
            GPIO.output(self.clk, 1)
    #color 1=red 2=green 0=off

    def set_led(self, n, color=RED):
        self.send_data((n << 1) + 1, color)

    def send_char(self, pos, data, dot=False):
        self.send_data(pos << 1, self.FONT.get(data, 0) | (0x80 if dot else 0))

    def set_digit(self, pos, digit, dot=False):
        for i in range(0, 6):
            self.send_char(i, self.get_bit_mask(pos, digit, i), dot)
    
    def get_bit_mask(self, pos, digit, bit):
        return ((self.FONT[digit] >> bit) & 1) << pos
    
    def clean(self):
        for i in range(8):
            self.send_char(i, ' ')

    def cleanall(self):
        self.clean()
        for i in range(8):
            self.set_led(i, 0)

    def set_text(self, text, delay=text_delay):
        self.clean()
        text = text.lower()
        length = len(text)
        # running string
        if length > 8:
            prev, curr = 0, 8
            while curr <= len(text):
                self.set_text(text[prev:curr], delay)
                sleep(delay)
                prev += 1
                curr += 1
        else:
            dot = False
            i = 0
            while i < len(text):
                if i+1 < len(text) and text[i+1] == '.':
                    text = text.replace('.', '', 1)
                    dot = True
                else:
                    dot = False
                self.send_char(i, text[i], dot)
                i += 1

    def receive(self):
        temp = 0
        GPIO.setup(self.dio, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        for i in range(8):
            temp >>= 1
            GPIO.output(self.clk, False)
            if GPIO.input(self.dio):
                temp |= 0x80
            GPIO.output(self.clk, True)
        GPIO.setup(self.dio, GPIO.OUT)
        return temp

    def get_buttons(self):
        keys = 0
        GPIO.output(self.stb, False)
        self.send_byte(0x42)
        for i in range(4):
            keys |= self.receive() << i
        GPIO.output(self.stb, True)
        return keys
    
    def check_btns(self):
        while 1:
          sleep(0.06)
          mask = self.get_buttons()
          if mask > 0:
            self.set_led(2, self.RED)
            self.sw_callback(mask)
          else: 
            self.set_led(2, 0)

    def listen(self):
        t = threading.Thread(target=self.check_btns)
        t.start()
