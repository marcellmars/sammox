'''
run:
    curl https://textb.org/r/localdaemon/ | python

use in js:
    $.get('http://127.0.0.1:7788/?fooarg=value1,value2', function(r) { console.log(r) })


should print on server:
    fooarg
    value1
    value2
'''
import BaseHTTPServer
import SimpleHTTPServer
import ssl

PORT = 8001

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        print("options")
        self.send_response(200, 'OK')
        self.send_header('Allow', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With')
        self.send_header('Content-Length', '0')
        self.end_headers()

    def do_GET(self):
        print self.path

        self.send_response(200, 'OK')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write('{"alive":true}')


httpd = BaseHTTPServer.HTTPServer(("localhost.memoryoftheworld.org", PORT), Handler)
httpd.socket = ssl.wrap_socket(httpd.socket, keyfile='localmemory.key', certfile='localmemory.crt', server_side=True)

print "serving at port", PORT
httpd.serve_forever()
