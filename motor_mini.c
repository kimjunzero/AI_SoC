#include <stdio.h>
#include <stdlib.h>
#include <wiringPi.h>
#include <pthread.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <sys/stat.h>

#define A	21
#define B	22
#define C	23
#define D	24
#define BUZZER	25

#define FIFO_PATH "/tmp/py2c_fifo"

int target_motor_cnt = 1;
int buzzer_flag = 0;
int state = 0;

void *read_pipe_thread(void *arg)
{
    char buffer[16];
    int fd;

    mkfifo(FIFO_PATH, 0666);

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
		if(input >= 6 && !buzzer_flag) buzzer_flag = 1;
            }
        }
    }

    close(fd);
    pthread_exit(NULL);
}

void *play_buzzer_thread(void* arg)
{
	static int start_time;
	static int first_call = 1;
	while(1)
	{		
		if(buzzer_flag)
		{
			if(first_call) {
				start_time = millis();
				first_call = 0;
			}
		
			digitalWrite(BUZZER, HIGH);
			if((millis() - start_time) >= 500)
			{
				buzzer_flag = 0;
				first_call = 1;
				digitalWrite(BUZZER, LOW);
			}
		}
	}

}

void init()
{
    wiringPiSetup();
	
	pinMode(A, OUTPUT);
	pinMode(B, OUTPUT);
	pinMode(C, OUTPUT);
	pinMode(D, OUTPUT);
	pinMode(BUZZER, OUTPUT);

	digitalWrite(BUZZER, LOW);
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

int main()
{
    init();
	unsigned int curr_motor_cnt = 1;
    
    
    pthread_t th1, th2;
    pthread_create(&th1, NULL, read_pipe_thread, NULL);
    pthread_create(&th2, NULL, play_buzzer_thread, NULL);
    
    while(1)
    {
        if(curr_motor_cnt > target_motor_cnt) curr_motor_cnt--;
        else if(curr_motor_cnt < target_motor_cnt) curr_motor_cnt++;
        else if(curr_motor_cnt == target_motor_cnt)
        {
            delay(5);
            continue;
        }
        motor_step(curr_motor_cnt % 4);
        delay(5);
    }
	
	return 0;
}
