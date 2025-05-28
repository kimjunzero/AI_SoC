#include <stdio.h>
#include <wiringPi.h>

#define ORANGE    21 // 29
#define YELLOW    22 // 31
#define PINK      23 // 33s
#define BLUE      24 // 35
#define RED       25 // 임시 전원용 : 사용 불가
// GND        6
// 5V         2

void step_wave(int step)
{
	switch(step)
	{
		case 0:
			digitalWrite(ORANGE, 1);
			digitalWrite(YELLOW, 0);
			digitalWrite(PINK,   0);
			digitalWrite(BLUE,   0);
			break;
			
		case 1:
			digitalWrite(ORANGE, 0);
			digitalWrite(YELLOW, 1);
			digitalWrite(PINK,   0);
			digitalWrite(BLUE,   0);
			break;
			
		case 2:
			digitalWrite(ORANGE, 0);
			digitalWrite(YELLOW, 0);
			digitalWrite(PINK,   1);
			digitalWrite(BLUE,   0);
			break;
			
		case 3:
			digitalWrite(ORANGE, 0);
			digitalWrite(YELLOW, 0);
			digitalWrite(PINK,   0);
			digitalWrite(BLUE,   1);
			break;
			
		default:
			break;
	}
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

void step_half(int step) // 4phase 8step full
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
			digitalWrite(PINK,   0);
			digitalWrite(BLUE,   0);
			break;
			
		case 2:
			digitalWrite(ORANGE, 0);
			digitalWrite(YELLOW, 1);
			digitalWrite(PINK,   1);
			digitalWrite(BLUE,   0);
			break;
			
		case 3:
			digitalWrite(ORANGE, 0);
			digitalWrite(YELLOW, 0);
			digitalWrite(PINK,   1);
			digitalWrite(BLUE,   0);
			break;
			
	    case 4:
			digitalWrite(ORANGE, 1);
			digitalWrite(YELLOW, 0);
			digitalWrite(PINK,   1);
			digitalWrite(BLUE,   1);
			break;
			
		case 5:
			digitalWrite(ORANGE, 0);
			digitalWrite(YELLOW, 0);
			digitalWrite(PINK,   0);
			digitalWrite(BLUE,   1);
			break;
			
		case 6:
			digitalWrite(ORANGE, 1);
			digitalWrite(YELLOW, 0);
			digitalWrite(PINK,   0);
			digitalWrite(BLUE,   1);
			break;
			
		case 7:
			digitalWrite(ORANGE, 1);
			digitalWrite(YELLOW, 0);
			digitalWrite(PINK,   0);
			digitalWrite(BLUE,   0);
			break;
			
		default:
			break;
	}
}

int main()
{
	wiringPiSetup();
	pinMode(ORANGE, OUTPUT);
	pinMode(YELLOW, OUTPUT);
	pinMode(PINK,   OUTPUT);
	pinMode(BLUE,   OUTPUT);
	pinMode(RED,    OUTPUT); // Power Line
	digitalWrite(RED, HIGH);
	
	// 4phase 4step(2가지)
	for(int i = 0; i < 2048; i++) // half or full(wave)
	{
		// step_wave(i % 4);
		step_full(i % 4);
		delay(2);
	}
	// 4phase 8step
	for(int i = 0; i < 4096; i++)
	{
		step_half((4096 - i) % 8);
		delay(1);
	}
	
	// digitalWrite(7, 1);
	
	return 0;
}
