import socket
import os
import mimetypes

def translate_path(path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        words = path.split('/')
        words = filter(None, words)
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path

def copyfileobj(fsrc, fdst, length=16*1024):
        """copy data from file-like object fsrc to file-like object fdst"""
        while 1:
                buf = fsrc.read(length)
                if not buf:
                        break
                fdst.write(buf)

def splitext(p):
        """Split the file name into base and extention """
        i = p.rfind('.')
        if i<=p.rfind('/'):
           return p, ''
        else:
         return p[:i], p[i:]

def guess_type(path):
  """Try to guess the internet resource type"""
  if not mimetypes.inited:
        mimetypes.init() # try to read system mime.types
  extensions_map = mimetypes.types_map.copy()
  extensions_map.update({
        '': 'application/octet-stream', # Default
        '.py': 'text/plain',
        '.c': 'text/plain',
        '.h': 'text/plain',
        '.gif': 'image/gif',
        '.jpg': 'image/jpeg',
        })
  base, ext = splitext(path)
  if ext in extensions_map:
            return extensions_map[ext]
  ext = ext.lower()
  if ext in extensions_map:
            return extensions_map[ext]
  else:
            return extensions_map['']



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
        path = translate_path(path)
        while 1:
                
             line = cfile.readline().strip()
             if line == '':

                # If the request path is a directory then list its content
                if os.path.isdir(path):
                  cfile.write("HTTP/1.0 200 OK\n\n")
                  cfile.write("<head><title>Shu Wang's Python Test Web Server</title></head>")
                  cfile.write("<h1>Shu Wang's Python Test Web Server</h1>")

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
                # If the request path is a file then serve the file
                else:
                     f = open(path, 'rb')      
                     ctype = guess_type(path)
                     cfile.write("HTTP/1.0 200 OK\n")
                     cfile.write("Content-type: " + ctype + "\n")
                     cfile.write("Content-Length: " + str(os.fstat(f.fileno())[6]) + "\n\n")
                     copyfileobj(f, cfile)  
                    
                cfile.close()
                csock.close()
                break

