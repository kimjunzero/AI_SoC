#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wiringPi.h>
#include <linux/socket.h>
#include <linux/types.h>
#include <unistd.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <pthread.h>

#define PORT 9000
int s_sock, c_sock;

void ReadThread()
{
	char buf[500];
	while(1)
	{
		int r = read(c_sock, buf, 500); buf[r] = 0;
		if(r > 0)
		{
			printf("> %s(%d)\n", buf, r);
			if(!strncmp(buf, "exit", 4)) exit(0);
		}
	}
	
}
int main()
{
	struct sockaddr_in saddr, caddr;  // address define
	memset(&saddr, 0, sizeof(saddr)); // server address
	memset(&caddr, 0, sizeof(caddr)); // client
	saddr.sin_family = AF_INET;
	saddr.sin_port = htons(PORT);
	saddr.sin_addr.s_addr = 0; // inet_addr("0.0.0.0"); // htonl(INADDR_ANY); // 0 0 0 0
	
	s_sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP); // socket open
	int ret_bind = bind(s_sock, (struct sockaddr *)&saddr, sizeof(saddr));
	
	printf("\nServer socket information (s_sock:%d),(bind:%d)\n", s_sock, ret_bind);
	printf("Server thread running....\n");
	
	listen(s_sock, 2);
	int len = sizeof(caddr);
	c_sock = accept(s_sock, (struct sockaddr *)&caddr, &len);
	
	int ip = caddr.sin_addr.s_addr;
	int pt = caddr.sin_port;
	
	printf("    RemoteEP_ADDR : %d.%d.%d.%d\n", ip&0xFF, (ip&0xff00)>>8, (ip&0xff0000)>>16, (ip&0xff000000)>>24);
	printf("    RemoteEP_PROT : %d\n",((pt&0xff)<<8) + ((pt&0xff00)>>8));
	
	
	pthread_t th;
	pthread_create(&th, NULL, ReadThread, NULL);
	
	char sbuf[500];
	while(1)
	{
		printf(">"); gets(sbuf); // scanf("%s", sbuf);
		write(c_sock, sbuf, strlen(sbuf));
		if(!strncmp(sbuf, "exit", 4)) exit(0);
	}
	
	return 0;
}
