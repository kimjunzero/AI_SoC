#include <stdio.h>
#include <wiringPi.h>
#include "step.h"

#define TRIG  27
#define ECHO  28

void Trigger();
double Distance();

int main()
{
	wiringPiSetup();
	pinMode(TRIG, OUTPUT);
	pinMode(ECHO, INPUT);
	
	pinMode(ORANGE, OUTPUT);
	pinMode(YELLOW, OUTPUT);
	pinMode(PINK,   OUTPUT);
	pinMode(BLUE,   OUTPUT);
	pinMode(RED,    OUTPUT); // Power Line
	digitalWrite(RED, HIGH);
	
	digitalWrite(TRIG, LOW); delay(10); // 초기 PIN 상태 0(1)
	
	while(1)
	{
		
		// Trigger signal(2)
		Trigger();
	
		// Echo signal(3,4)
		double dist = Distance();
		
		delay(60); // enough time(5)
		printf("Distance : %.2lf\n", dist);
		
		if(dist <= 100)
		{
			// 4phase 4step(2가지)
			for(int i = 0; i < 2048; i++) // half or full(wave)
			{
				// step_wave(i % 4);
				step_full(i % 4);
				delay(2);
			}
		}
		else
		{
			// 4phase 4step(2가지)
			for(int i = 0; i < 2048; i++) // half or full(wave)
			{
				// step_wave(i % 4);
				step_full((2048 - i) % 4);
				delay(2);
			}
		}
	}
	
	return 0;
}

void Trigger()
{
	digitalWrite(TRIG, HIGH);
	delayMicroseconds(10);
	digitalWrite(TRIG, LOW);
	delayMicroseconds(200); // wait for Burst end : 25us(1/4k) * 8 =200us
}

double Distance()
{
	while(1) // Burst over, count start
	{
		int e = digitalRead(ECHO);
		if(e == 1) break; // high가 됬을 때
	}
	int t1 = micros();
	
	while(1) // wait until echo receive
	{
		int e = digitalRead(ECHO);
		if(e == 0) break; // low가 됬을 때
	}
	int t2 = micros();
	// 0.017
	
	double dist = (t2 - t1) * 0.017;
	
	return dist;
}

void step_full(int step) // 4phase 4setp full
{
	switch(step)
	{
		case 0:
			digitalWrite(ORANGE, 1);
			digitalWrite(YELLOW, 1);
			digitalWrite(PINK,   0);
			digitalWrite(BLUE,   0);
			break;
			
		case 1:
			digitalWrite(ORANGE, 0);
			digitalWrite(YELLOW, 1);
			digitalWrite(PINK,   1);
			digitalWrite(BLUE,   0);
			break;
			
		case 2:
			digitalWrite(ORANGE, 0);
			digitalWrite(YELLOW, 0);
			digitalWrite(PINK,   1);
			digitalWrite(BLUE,   1);
			break;
			
		case 3:
			digitalWrite(ORANGE, 1);
			digitalWrite(YELLOW, 0);
			digitalWrite(PINK,   0);
			digitalWrite(BLUE,   1);
			break;
			
		default:
			break;
	}
}
