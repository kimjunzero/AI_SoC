#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wiringPi.h>
#include <linux/socket.h>
#include <linux/types.h>
#include <linux/unistd.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <pthread.h>

#define PORT 9000
char *sip;
int s_sock, c_sock;

void ReadThread()
{
	char cbuf[500];
	while(1)
	{
		int r = read(c_sock, cbuf, 500); cbuf[r] = 0;
		if(r > 0)
		{
			printf("> %s(%d)\n", cbuf, r);
			if(!strncmp(cbuf, "exit", 4)) exit(0);
			
		}
	}
}

int main(int n, char **s)
{
	if(n == 1) // no argument
	{
		sip = "127.0.0.1";
	}
	else
	{
		sip = s[1];
		// sip = *(s+1);
	}
	
	struct sockaddr_in saddr, caddr;  // address define
	memset(&saddr, 0, sizeof(saddr)); // server address
	memset(&caddr, 0, sizeof(caddr)); // client
	saddr.sin_family = AF_INET;
	saddr.sin_family = AF_INET;
	saddr.sin_port = htons(PORT);
	saddr.sin_addr.s_addr = inet_addr(sip); // htonl(INADDR_ANY);  0 0 0 0
	
	c_sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP); // socket open
	int ret  = connect(c_sock, (struct sockaddr *)&saddr, sizeof(saddr));
	
	int ip = saddr.sin_addr.s_addr;
	int pt = saddr.sin_port;
	
	printf("connect result : %d\n\n", ret);
	printf("Server socket information:\n");
	printf("    SERVER_ADDR : %d.%d.%d.%d\n", ip&0xFF, (ip&0xff00)>>8, (ip&0xff0000)>>16, (ip&0xff000000)>>24);
	printf("    SERVER_PROT : %d\n",((pt&0xff)<<8) + ((pt&0xff00)>>8));
	
	
	if(ret == 0)  // connect OK!
	{
		printf("Server connected\n\n");
	}
	else
	{
		printf("\n\n원격 서버에 연결할 수 없습니다.\n\n", ret);
		return -1;
	}
	
	pthread_t th;
	pthread_create(&th, NULL, ReadThread, NULL);
	
	char rbuf[500];
	while(1)
	{
		fflush(stdin);
		fflush(stdout);
		fgets(rbuf, 500, stdin);
		write(c_sock, rbuf, strlen(rbuf));
		if(!strncmp(rbuf, "exit", 4)) exit(0);
	}
	
	return 0;
}
