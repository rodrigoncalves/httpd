import sys, os
import string, cgi, time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class http(BaseHTTPRequestHandler): 

    def do_GET(self):
        try:
            if self.path.endswith(".html"):
                f = open(DocumentRoot + self.path)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
                return

            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    def do_POST(self):
        global rootnode
        try:
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                query = cgi.parse_multipart(self.rfile, pdict)
            self.send_response(301)

            self.end_headers()
            upfilecontent = query.get('upfile')
            print "filecontent", upfilecontent[0]
            self.wfile.write("<html>Post OK. <br /><br />");
            self.wfile.write(upfilecontent[0]);
            self.wfile.write("</html>")

        except:
            pass

def main(NameVirtualHost):
    try:
        virtualhost = string.split(NameVirtualHost, ":")

        if virtualhost[0] == "*":
            virtualhost[0] = ""
         
        server = HTTPServer((virtualhost[0], int(virtualhost[1])), http)
        print 'Start server HTTP in %s' % NameVirtualHost
        server.serve_forever()

    except KeyboardInterrupt:
        print 'Shutting down server HTTP'
        server.socket.close()

if __name__ == '__main__':
    DocumentRoot = "%s/htdocs/" % os.path.realpath(os.path.dirname(__file__))

    PORT = "8000"
    HOST = "localhost"

    if len(sys.argv) >= 2:
        main(sys.argv[1])
    else:
        main("%s:%s" % (HOST, PORT))
