from machine import Pin
from time import sleep
import RTDSettings as RTD

RTD.GPIO_Init()                 #Initializes the channels  
sleep(5.0)
print("Finish RTD.GPIO_Init()")   
while True:
    RTD.ADC_Init() #Initializes the ADC
    sleep(1.0)
    x=0
    for x in range(5):
        print("RTD no. ", x)
        RTD.Sel_Channel(x)  #sequences the channel and current activation
        sleep(1.0)
        print(RTD.Resistance_Convertion(RTD.Read_ADC())) #begins ADC conversion and its convention into resistance value
    print("Finish ADC x 5 Channels Reading")    
    sleep(5.0)