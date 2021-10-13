from machine import Pin
from time import sleep
import MultipleRTDSettings as RTD

RTD.GPIO_Init()

while True:
    print('''Select RTD: 
    0: RTD_0 
    1: RTD_1
    2: RTD_2 
    3: RTD_3 
    4: RTD_4 
    ''')
    RTD_id=(int(input("RTD: ")))
    RTD.sel_channel(RTD_id)
    
    print(RTD.ResistanceConvertion(RTD.read_ADC()))
    sleep(10.0)
    