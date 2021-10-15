from machine import Pin
from time import sleep
import RTDSettings as RTD

RTD.GPIO_Init()
RTD.Set_Init()
sleep(5.0)
print("Finish RTD.GPIO_Init()")

suma=[]
meas_RTD0=[]
meas_RTD1=[]
meas_RTD2=[]
meas_RTD3=[]
meas_RTD4=[]
average=[]
error=[]
std=[]
theo_val=[100,10,50,250,150]
n=50
while True:
    RTD.ADC_Init()
    for i in range(n):   
        for x in range(5):
            print("RTD no. ", x)
            RTD.Sel_Channel(x)
            sleep(1.0)
            tempo=RTD.Resistance_Convertion(RTD.Read_ADC())
            print(tempo)
            if (x==0):
                meas_RTD0.append(tempo)
            elif (x==1):
                meas_RTD1.append(tempo)
            elif (x==2):
                meas_RTD2.append(tempo)
            elif (x==3):
                meas_RTD3.append(tempo)
            elif (x==4):
                meas_RTD4.append(tempo)
        print("Finish ADC x 4 Channels Reading. Reading : #",i)

    suma.append(sum(meas_RTD0))
    suma.append(sum(meas_RTD1))
    suma.append(sum(meas_RTD2))
    suma.append(sum(meas_RTD3))
    suma.append(sum(meas_RTD4))
    meas_RTD=[meas_RTD0,meas_RTD1,meas_RTD2,meas_RTD3,meas_RTD4]
    print("-----------------------------------------------------------------------------------------")         
    for i in range (5):
        average.append(suma[i]/n)
        error.append(100*abs(theo_val[i]-average[i])/theo_val[i])
        tempo=[]
        for k in range (n):
            tempo.append((meas_RTD[i][k] - average[i])**2)
        std.append((sum(tempo)/n)**0.5)
    print("averages: ",average)
    print("errors: ",error)
    print("std: ",std)
    print("-----------------------------FINAL DE PRUEBA (",n,") mediciones)--------------------------------------")         
    sleep(5.0)
    
    
    
    