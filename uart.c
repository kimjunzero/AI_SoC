#include <stdio.h>
#include <wiringPi.h>
#include <wiringSerial.h>
#include <pthread.h>
//#include <termios.h>

#define B_RATE    B9600

int fd;
void ReadProcess()
{
    char buf[1024];
    while(1)
    {
        int i;
        int n = serialDataAvail(fd);
        for(i=0;i<n;i++)
        {
            buf[i] = serialGetchar(fd);
        }
        buf[i] = 0;
        printf("%s",buf);
    }
}

int main()
{
    //struct termios op;
    fd = serialOpen("/dev/serial0", 9600);
    printf("serial Port handle : %d\n",fd);

    pthread_t rp;
    pthread_create(&rp, NULL, ReadProcess, NULL);

    serialPutchar(fd, 'a');
    printf("%c", serialGetchar(fd));

    char buf[500];
    while(1)
    {
        printf(">");
        fgets(buf, 500, stdin); // gets(buf); //
        serialPuts(fd, buf);
    }

    return 0;
}
