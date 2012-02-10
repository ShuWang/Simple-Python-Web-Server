import socket
import os


# Translate http request path to local OS path
def translate_path(path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        # abandon query parameters
        print "Original path from GET is" + path
        # path = urlparse.urlparse(path)[2]
        # path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path



host = ''
port = 50009

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sock.bind((host,port))
sock.listen(1)

while 1:
        csock,caddr = sock.accept()
        cfile = csock.makefile('rw',0)

        # Protocol exchange - read request

        # Extract request path
        line = cfile.readline().strip()
        words = line.split()
        [command, path, version] = words
        print "Extracted path is" + path
        path = translate_path(path)
        print "Translated local path is" + path
        while 1:
                
             line = cfile.readline().strip()
             # print line
             if line == '':

                cfile.write("HTTP/1.0 200 OK\n\n")
                cfile.write("<head><title>Shu Wang's Python Test Web Server</title></head>")
                cfile.write("<h1>Shu Wang's Python Test Web Server</h1>")

                # list directory
                list = os.listdir(path)
                for name in list:
                     fullname = os.path.join(path, name)
                     displayname = linkname = name
                     # Append / for directories or @ for symbolic links
                     if os.path.isdir(fullname):
                         displayname = name + "/"
                         linkname = name + "/"
                     if os.path.islink(fullname):
                         displayname = name + "@"
                     cfile.write('<li><a href="%s">%s</a>\n'
                             % (linkname, displayname))
                      


                cfile.close()
                csock.close()
                break

