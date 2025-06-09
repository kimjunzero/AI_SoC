#include <stdio.h>
#include <stdlib.h>
#include <wiringPi.h>
#include <pthread.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <sys/stat.h>

#define A   21
#define B   22
#define C   23
#define D   24
#define BUZZER  25

#define BUZZER_DELAY    500
#define BUZZER_CYCLE    600

#define FIFO_PATH "/tmp/py2c_fifo"

int target_motor_cnt = 1;
int state = 0;
int buzzer_flag = 0;

void *read_pipe_thread(void *arg)
{
    char buffer[16];
    int fd;

    // FIFO가 없다면 생성
    mkfifo(FIFO_PATH, 0666);

    // FIFO 열기 (읽기 전용)
    fd = open(FIFO_PATH, O_RDONLY);

    if (fd == -1) {
        perror("open");
        pthread_exit(NULL);
    }

    while (1)
    {
        memset(buffer, 0, sizeof(buffer));
        int n = read(fd, buffer, sizeof(buffer) - 1);
        if (n > 0)
        {
            int input = atoi(buffer);
            if (input >= 0 && input <= 9 && state != input)
            {
                state = input;
                if(!state) target_motor_cnt = 1;
                else target_motor_cnt = state*300 + 1000;
                if(input >= 3 && !buzzer_flag) buzzer_flag = 1;
            }
        }
    }

    close(fd);
    pthread_exit(NULL);
}

void init()
{
    wiringPiSetup();
    
    pinMode(A, OUTPUT);
    pinMode(B, OUTPUT);
    pinMode(C, OUTPUT);
    pinMode(D, OUTPUT);
    pinMode(BUZZER, OUTPUT);
    digitalWrite(BUZZER, 0);
    delay(10);
}

void motor_step(int step)
{
    switch(step)
    {
        case 0:
            digitalWrite(A, HIGH);
            digitalWrite(B, HIGH);
            digitalWrite(C, LOW);
            digitalWrite(D, LOW);
            break;
        case 1:
            digitalWrite(A, LOW);
            digitalWrite(B, HIGH);
            digitalWrite(C, HIGH);
            digitalWrite(D, LOW);
            break;
        case 2:
            digitalWrite(A, LOW);
            digitalWrite(B, LOW);
            digitalWrite(C, HIGH);
            digitalWrite(D, HIGH);
            break;
        case 3:
            digitalWrite(A, HIGH);
            digitalWrite(B, LOW);
            digitalWrite(C, LOW);
            digitalWrite(D, HIGH);
            break;
        default:
            break;
    }
}

void playTone() {
    
    static int value = 0;
    static int i = 0;
    
    value = !value;
    i++;
    if(i >= BUZZER_CYCLE)
    {
        value = 0;
        i = 0;
        buzzer_flag = 0;
        digitalWrite(BUZZER, 0);
    }

    digitalWrite(BUZZER, value);

}

int main()
{
    init();
    unsigned int curr_motor_cnt = 1;
    
    unsigned int prev_motor_time = 0;
    unsigned int prev_buzzer_time = 0;

    pthread_t th;
    pthread_create(&th, NULL, read_pipe_thread, NULL);
    
    while(1)
    {
        unsigned int now = millis();
        if (now - prev_motor_time >= 5)
        {
            prev_motor_time = now;
            if(curr_motor_cnt > target_motor_cnt) curr_motor_cnt--;
            else if(curr_motor_cnt < target_motor_cnt) curr_motor_cnt++;
            else
            motor_step(curr_motor_cnt % 4);
        }
        if (buzzer_flag)
        {
            unsigned int now_us = micros();
            if (now_us - prev_buzzer_time >= BUZZER_DELAY)
            {
                prev_buzzer_time = now_us;
                playTone();
            }
        }
    }
    
    return 0;
}
