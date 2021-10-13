from machine import Pin
from time import sleep
import RTDSettings as RTD

RTD.GPIO_Init()

while True:
    print(RTD.RTD_ResistanceConvertion(RTD.read_ADC()))
    sleep(10.0)