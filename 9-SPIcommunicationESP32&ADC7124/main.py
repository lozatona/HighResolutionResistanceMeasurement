from machine import Pin, SoftSPI
from time import sleep
spi = SoftSPI(baudrate=1000000, polarity=1, phase=1, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
# print("status")
# x=spi.read(1, 0x40)
while True: 
    #id 0x14 
    print("id")
    x=spi.read(2, 0x45)
    print(x)
    
	#config register 0x0860 offset
    x=spi.read(1, 0x19)
    x=spi.read(1, 0x08)
    x=spi.read(1, 0x04)
    print("config")
    x=spi.read(3, 0x59)
    print(x)
    x=spi.read(3, 0x5a)
    print(x)
    
	#filter 0x060180 offset   
    x=spi.read(1, 0x21)
    x=spi.read(1, 0xf6)
    x=spi.read(1, 0x03)
    x=spi.read(1, 0xc0)
    print("filter")
    x=spi.read(4, 0x61) 
    print(x)    
    x=spi.read(4, 0x62)    
    print(x)
    
    #Channel 0x8001 offset    
    x=spi.read(1, 0x09)
    x=spi.read(1, 0x80)
    x=spi.read(1, 0x43)
    print("Channel")
    x=spi.read(3, 0x49)
    print(x)
    x=spi.read(3, 0x4a)
    print(x)
    sleep(5)