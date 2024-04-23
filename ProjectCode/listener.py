import socket
import struct
import json



things_services = {}
services = []

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Define the multicast group and port
multicast_group = '232.1.1.1'
server_address = ('', 1235)

# Bind to the server address
s.bind(server_address)

# Tell the operating system to add the socket to the multicast group
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
    print("\nwaiting to receive message")
    data, address = s.recvfrom(1024)
    # Decode the data to a string
    data_string = data.decode()

    # Parse the JSON string into a Python dictionary
    data_dict = json.loads(data_string)

    # Print the keys
    if(data_dict['Tweet Type'] == "Service"):
        print('Received service: ', data_dict['Tweet Type'])
        if data_dict['Name'] not in services:
            services.append(data_dict['Name'])
            if data_dict['Thing ID'] not in things_services:
                things_services[data_dict['Thing ID']] = [data_dict['Name']]
            else:
                things_services[data_dict['Thing ID']].append(data_dict['Name'])
            things_services[data_dict['Thing ID']].sort()
        print('Services: ', services)
        print('Things Services: ', things_services)