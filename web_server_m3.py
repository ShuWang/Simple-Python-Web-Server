import socket
import os

host = ''
port = 8080

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sock.bind((host,port))
sock.listen(1)

while 1:
        csock,caddr = sock.accept()
        cfile = csock.makefile('rw',0)

        # Protocol exchange - read request

        while 1:
                line = cfile.readline().strip()
                if line == '':
                        cfile.write("HTTP/1.0 200 OK\n\n")
                        cfile.write("<head><title>Shu Wang's Python Test Web Server</title></head>")
                        cfile.write("<h1>Shu Wang's Python Test Web Server</h1>")

                        path = '.'
                        listing = os.listdir(path)
                        for infile in listing:
                            if os.path.isdir(infile):
                                cfile.write("<h2>d&nbsp;&nbsp;" + infile + "</h1>")
                            else:
                                cfile.write("<h2>f&nbsp;&nbsp;" + infile + "</h2>")

                        cfile.close()
                        csock.close()
                        break

