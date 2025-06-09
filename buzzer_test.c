#include <wiringPi.h>
#include <stdio.h>

#define BUZZER_PIN 25  // GPIO 18 (WiringPi 기준)

void beep() {
    int frequency = 1000;           // 1kHz
    int duration_ms = 300;          // 300ms
    int delay_us = 1000000 / frequency / 2;
    int cycles = frequency * duration_ms / 1000;

    for (int i = 0; i < cycles; i++) {
        digitalWrite(BUZZER_PIN, HIGH);
        delayMicroseconds(delay_us);
        digitalWrite(BUZZER_PIN, LOW);
        delayMicroseconds(delay_us);
    }
}

int main() {
    if (wiringPiSetup() == -1) {
        printf("WiringPi 초기화 실패\n");
        return 1;
    }

    pinMode(BUZZER_PIN, OUTPUT);
    while(1)
    {
	beep();
	delay(1000);
	}

    return 0;
}
