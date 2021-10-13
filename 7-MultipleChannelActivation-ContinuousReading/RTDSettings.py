
from machine import Pin, SoftSPI
spi = SoftSPI(baudrate=1_000_000, polarity=0, phase=0, sck=Pin(0), mosi=Pin(2), miso=Pin(1))#configurations for Raspberry Pi Pico 

def GPIO_Init(): 
    #RESET
    #disable all channels 
    #Channel_0 Register
    x=spi.read(1, 0x09)
    x=spi.read(1, 0x00)
    x=spi.read(1, 0x00)    
    #Channel_1 Register
    x=spi.read(1, 0x0A)
    x=spi.read(1, 0x00)
    x=spi.read(1, 0x00)  
    #Channel_2 Register
    x=spi.read(1, 0x0B)
    x=spi.read(1, 0x00)
    x=spi.read(1, 0x00)  
    #Channel_3 Register
    x=spi.read(1, 0x0C)
    x=spi.read(1, 0x00)
    x=spi.read(1, 0x00)  
    #Channel_4 Register
    x=spi.read(1, 0x0D)
    x=spi.read(1, 0x00)
    x=spi.read(1, 0x00)  
    
    #IO_Control_1 Register 
    #disable current
    x=spi.read(1, 0x03)
    x=spi.read(1, 0x00)
    x=spi.read(1, 0x00)
    x=spi.read(1, 0x00)
   
    #Config_0 Register
    #bipolar
    #gain=16
    #ref(+), ref(-)  
    #full power mode 
    #single convertion
    x=spi.read(1, 0x19)
    x=spi.read(1, 0x08)
    x=spi.read(1, 0x04)
    
def CH_0(): 
    GPIO_Init()     
    #Channel_0 Register 
    #enable 
    #AINP=AIN2
    #AINM=AIN3
    #setup = Config_0
    x=spi.read(1, 0x09)
    x=spi.read(1, 0x80)
    x=spi.read(1, 0x43)
    #IO_Control_1 Register 
    #Iout0 = 500 uA
    #Iout_CH = AIN0
    x=spi.read(1, 0x03)
    x=spi.read(1, 0x00)
    x=spi.read(1, 0x04)
    x=spi.read(1, 0x00)

def CH_1():       
    GPIO_Init()
    #Channel_1 Register 
    #enable 
    #AINP=AIN4
    #AINM=AIN5
    #setup = Config_0
    x=spi.read(1, 0x0A)
    x=spi.read(1, 0x80)
    x=spi.read(1, 0x85)
    #IO_Control_1 Register 
    #Iout0 = 500 uA
    #Iout_CH = AIN1
    x=spi.read(1, 0x03)
    x=spi.read(1, 0x00)
    x=spi.read(1, 0x04)
    x=spi.read(1, 0x01)
    
def CH_2():       
    GPIO_Init()
    #Channel_2 Register 
    #enable 
    #AINP=AIN6
    #AINM=AIN7
    #setup = Config_0
    x=spi.read(1, 0x0B)
    x=spi.read(1, 0x80)
    x=spi.read(1, 0xCE)
    #IO_Control_1 Register 
    #Iout0 = 500 uA
    #Iout_CH = AIN8
    x=spi.read(1, 0x03)
    x=spi.read(1, 0x00)
    x=spi.read(1, 0x04)
    x=spi.read(1, 0x08)
    
def CH_3():      
    GPIO_Init()
    #Channel_3 Register 
    #enable 
    #AINP=AIN9
    #AINM=AIN10
    #setup = Config_0
    x=spi.read(1, 0x0C)
    x=spi.read(1, 0x81)
    x=spi.read(1, 0x2A)
    #IO_Control_1 Register 
    #Iout0 = 500 uA
    #Iout_CH = AIN11
    x=spi.read(1, 0x03)
    x=spi.read(1, 0x00)
    x=spi.read(1, 0x04)
    x=spi.read(1, 0x0B)

def CH_4():       
    GPIO_Init()
    #Channel_4 Register 
    #enable 
    #AINP=AIN12
    #AINM=AIN13
    #setup = Config_0
    x=spi.read(1, 0x0D)
    x=spi.read(1, 0x81)
    x=spi.read(1, 0x8D)
    #IO_Control_1 Register 
    #Iout0 = 500 uA
    #Iout_CH = AIN14
    x=spi.read(1, 0x03)
    x=spi.read(1, 0x00)
    x=spi.read(1, 0x04)
    x=spi.read(1, 0x0E)

def ADC_Init():
    #ADC_control Register
    #Internal CLK
    #continuos convertion mode
    #-----------------------------
    #   Power mode   |    code
    # F(full)/L(low) |
    #-----------------------------
    #      F         |   0x00C0
    #      F         |   0x0080
    #      L         |   0x0000
    x=spi.read(1, 0x01)
    x=spi.read(1, 0x00) #this byte is always 0x00
    x=spi.read(1, 0xc0) #this bythe defines the power mode 
    x=spi.read(3, 0x41)
    print("ADC_Init(): ", x)

def Sel_Channel(CH_id):#CH_id is an integer and the number of the RTD to activate {0,...,4}
    channels = [CH_0, CH_1, CH_2, CH_3, CH_4]
    channel_sel=channels[CH_id]()
    print ("Channel ", CH_id, "selected")
    
def Read_ADC():
    x=spi.read(1, 0x42) #ignore first byte "adress instruction"
    x=spi.read(3, 0x42)
    x=int.from_bytes(x,"big")
    return x 

def Resistance_Convertion(dataadc):
    Rref = 5110 #reference resistance
    G = 16.0 # Gain
    r = (dataadc - 2**23) * Rref / (G * 2**23)
    return r