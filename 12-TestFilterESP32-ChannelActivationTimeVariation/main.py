from machine import Pin
from time import sleep
import RTDSettings as RTD

RTD.GPIO_Init()
RTD.Set_Init()
RTD.ADC_Init() 
sleep(5.0)
print("Finish RTD.GPIO_Init()")  
while True:
    # RTD.ADC_Init()
    # sleep(1.0)
    x=0
    a=0
    i=0
    for a in range(11):
        wait=0.0+a/10
        print("*******************Time= ",wait,"***********************")
        for i in range(10):   
            for x in range(5):
                print("RTD no. ", x)
                RTD.Sel_Channel(x)
                sleep(wait)
                print(RTD.Resistance_Convertion(RTD.Read_ADC()))
            print("Finish ADC x 4 Channels Reading. Reading : #",i)  
    print("-----------------------------FINAL DE PRUEBA--------------------------------------")         
    sleep(5.0)