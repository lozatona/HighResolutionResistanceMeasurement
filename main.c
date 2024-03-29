//******************************************************************************
#include "msp.h"
float v_adc=0;
float Rx;
float val_adc,Vx;
//*****************GPIO Setup*****************
void GPIO_Init(void){
    P1->SEL0 = 0X00;
    P1->SEL1 = 0X00;
    P1->DIR = 0X01;    //set P1.0 output
    P1->OUT = 0X01;

    P3->SEL0 = 0X00;
    P3->SEL1 = 0X00;
    P3->DIR = 0X01;    //set P3.0 output
    P3->OUT = 0X01;

    P4->SEL0 = 0X00;
    P4->SEL1 = 0X00;
    P4->DIR = 0X01;     //SET P4.0 output
    P4->OUT = 0X00;

    P6->SEL1 |= BIT4;                       // Configure P6.1 A14 for ADC
    P6->SEL0 |= BIT4;
}//end GPIO_Init
//*****************SysTick Initialization*****************
void SysTick_Init(void){ //24MHz
    SysTick->LOAD = 0x00FFFFFF; // maximum reload value
    SysTick->CTRL = 0x00000005; // enable, no interrupts
}//end SysTick_Init
//*****************  SysTick_Wait *****************
void SysTick_Wait(uint32_t n){
    SysTick->LOAD = n-1;
    SysTick->VAL = 0;
    while((SysTick->CTRL&0x00010000)== 0){};
}//end SysTick_Wait
//********************ADC Setup *********************************************
void ADC_Init(void){
    // Enable global interrupt
    __enable_irq();
    // Enable ADC interrupt in NVIC module
    NVIC->ISER[0] = 1 << ((ADC14_IRQn) & 31);
    // Sampling time, S&H=16, ADC14 on
    //ADC14_CTL0_SHT0_0       numero de ciclos de reloj (4) necesarios para eltiempo de de muestreo de una muestra  MEM 0-7/ MEM 24-31
    //ADC14_CTL0_SHT1_0       numero de ciclos de reloj (4) necesarios para eltiempo de de muestreo de una muestra  MEM 8-23
    //ADC14_CTL0_SHP    ADC14 sample-and-hold pulse-mode select
    ADC14->CTL0 = ADC14_CTL0_SHT0_0 | ADC14_CTL0_SHT1_0 | ADC14_CTL0_SHP | ADC14_CTL0_ON;
    //ADC14_CTL1_RES__14BIT   14 bit (16 clock cycle conversion time)
    ADC14->CTL1 = ADC14_CTL1_RES__14BIT;         // Use sampling timer, 14-bit conversion results
    ADC14->MCTL[0] |= ADC14_MCTLN_INCH_14;   // A14 6.1 ADC input select; Vref=AVCC
    ADC14->IER0 |= ADC14_IER0_IE0;          // Enable ADC conv complete interrupt
    SCB->SCR &= ~SCB_SCR_SLEEPONEXIT_Msk;   // Wake up on exit from ISR
}//end Int_ADC
//********************INTERRUPCIONES**********************************************************
// ADC14 interrupt service routine
void ADC14_IRQHandler(void) {
    //float RG=498.89;
    //float G=1+49400/RG;
    float G=100;
    float R=101;
    float R2=7600;
    float R3=9030;
    float R4=63600;
    float VDD=3.295;
    float a,offset,VLIA,v_io1,v_io2;

    SysTick_Wait(900000);//T=n/3e+06
    val_adc=ADC14->MEM[0];
    offset = VDD*((R3*R4/(R3+R4))/(R2+(R3*R4/(R3+R4))));
    a=((R2*R4/(R2+R4))/(R3+(R2*R4/(R2+R4))));
    a=1/a;
    v_adc=val_adc*3.2/16384; //Vref 3.3V
    VLIA = a*(v_adc-offset);
    Vx= VLIA/G;

    if (v_adc > offset){ //caso 1
        v_io1=2.472; //ajustar segun sea necesario
        v_io2=0.817; //ajustar segun sea necesario
        Rx=2*R*Vx/(v_io1-v_io2-Vx);
    }
    else{    //caso 2
        v_io1=0.802; //ajustar segun sea necesario
        v_io2=2.464; //ajustar segun sea necesario
        Rx=-2*R*Vx/(v_io2-v_io1+Vx);
    }
    SysTick_Wait(900);
}//end ADC14_IRQHandler
//******************************MAIN***********************************************
int main(void) {
    volatile unsigned int i;
    WDT_A->CTL = WDT_A_CTL_PW |             // Stop WDT
                 WDT_A_CTL_HOLD;
    GPIO_Init();
    SysTick_Init();
    ADC_Init();
    // Ensures SLEEPONEXIT takes effect immediately
    __DSB();

    while (1)
    {
        P3->OUT = (P3->OUT&(0x01)) ^ 1;
        P4->OUT = (P4->OUT&(0x01)) ^ 1;
        P1->OUT = (P1->OUT&(0x01)) ^ 1;

        // Start sampling/conversion
        ADC14->CTL0 |= ADC14_CTL0_ENC | ADC14_CTL0_SC;
        SysTick_Wait(30000000);//T=n/3e+06   3s
        __sleep();
        __no_operation();                   // For debugger
    }
}//end MAIN


