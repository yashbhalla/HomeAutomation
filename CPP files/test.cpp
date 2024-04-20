#include <iostream>
#include <cstring>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

#define PORT 12345
#define BUFFER_SIZE 1024

void receiveBroadcastMessage()
{
    int sockfd;
    struct sockaddr_in addr;
    char buffer[BUFFER_SIZE];
    int broadcast = 1;
    socklen_t addrlen = sizeof(addr);

    // Create a UDP socket
    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0)
    {
        std::cerr << "Failed to create socket" << std::endl;
        return;
    }

    // Enable broadcast
    if (setsockopt(sockfd, SOL_SOCKET, SO_BROADCAST, &broadcast, sizeof(broadcast)) < 0)
    {
        std::cerr << "Failed to set broadcast option" << std::endl;
        close(sockfd);
        return;
    }

    // Set up the address structure to bind to any address and the specified port
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(PORT);
    addr.sin_addr.s_addr = htonl(INADDR_ANY);

    // Bind the socket
    if (bind(sockfd, (struct sockaddr *)&addr, sizeof(addr)) < 0)
    {
        std::cerr << "Bind failed" << std::endl;
        close(sockfd);
        return;
    }

    std::cout << "Waiting for broadcast messages..." << std::endl;

    while (true)
    {
        int nbytes = recvfrom(sockfd, buffer, BUFFER_SIZE - 1, 0, (struct sockaddr *)&addr, &addrlen);
        if (nbytes < 0)
        {
            std::cerr << "Receive failed" << std::endl;
            continue;
        }

        buffer[nbytes] = '\0';
        std::cout << "Received broadcast message: " << buffer << std::endl;
    }

    // Close the socket (this will never be reached in this example)
    close(sockfd);
}

int main()
{
    receiveBroadcastMessage();

    return 0;
}