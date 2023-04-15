#!/usr/bin/env python3

import socket

#target_host = "www.google.com"
#target_port = 80

target_host = "127.0.0.1"
target_port = 9998


# socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect client
client.connect((target_host, target_port))

# send request
client.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

# receive some data
responce = client.recv(4096)

print(responce.decode())

client.close()


