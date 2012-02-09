import socket
import os

host = ''
port = 8080

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind((host, port))
sock.listen(1)
conn, addr = sock.accept()
print 'Connected by', addr
while 1:
    data = conn.recv(1024)
    if not data: break
    conn.send("Shu Wang's Web Server M1")
conn.close()

