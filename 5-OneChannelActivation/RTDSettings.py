
from machine import Pin, SoftSPI
spi = SoftSPI(baudrate=1_000_000, polarity=0, phase=0, sck=Pin(0), mosi=Pin(2), miso=Pin(1))

def GPIO_Init():
    #Channel_0 Register
    #enable 
    #AINP=AIN2
    #AINM=AIN3
    #setup = Config_0
    x=spi.read(1, 0x09)
    x=spi.read(1, 0x80)
    x=spi.read(1, 0x43)
    
    #Config_0 Register
    #bipolar
    #gain=16
    #ref(+), ref(-)    
    x=spi.read(1, 0x19)
    x=spi.read(1, 0x08)
    x=spi.read(1, 0x04)
    
    #IO_Control Register 
    #Iout0 = 500 uA
    #Iout_CH = AIN0
    x=spi.read(1, 0x03)
    x=spi.read(1, 0x00)
    x=spi.read(1, 0x04)
    x=spi.read(1, 0x00)
    
    #ADC_control Register
    #Internal CLK
    #low power mode
    #continuos convertion
    x=spi.read(1, 0x01)
    x=spi.read(1, 0x00)
    x=spi.read(1, 0x00)

def read_ADC():
    x=spi.read(1, 0x42) #ignore first byte "adress instruction"
    x=spi.read(3, 0x42)
    x=int.from_bytes(x,"big")
    return x 

def RTD_ResistanceConvertion(dataadc):
    Rref = 5110 #reference resistance
    G = 16.0 # Gain
    r = (dataadc - 2**23) * Rref / (G * 2**23)
    return r

