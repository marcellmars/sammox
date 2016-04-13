from PyQt4 import QtCore
from PyQt4 import QtGui

import sys
import SimpleHTTPServer
import SocketServer

'''
SimpleHTTPServer threaded daemon listening on PORT which sets text in
QLineEdit after getting GET request. It passes whatever is sent after
http://127.0.0.1:PORT/

Test it from any HTML page on internet having jQuery:

$.get('http://127.0.0.1:8001/?fooarg=tralala,'+ Math.round(Math.random()*100),
      function(r) {
        console.log(r)
      }
)
'''
PORT = 8001

class HTTPHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200, 'OK')
        self.send_header('Allow', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With')
        self.send_header('Content-Length', '0')
        self.end_headers()

    def do_GET(self):
        self.send_response(200, 'OK')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.server.qobject.my_signal.emit(self.path)
        self.wfile.write('You sent: {}'.format(self.path))

class ThreadedServer(QtCore.QThread):
    my_signal = QtCore.pyqtSignal(str, name="my_signal")
    def __init__(self):
        QtCore.QThread.__init__(self)
        SocketServer.TCPServer.allow_reuse_address = True
        self.httpd = SocketServer.TCPServer(("", PORT), HTTPHandler)
        self.httpd.qobject = self
    def run(self):
        self.httpd.serve_forever()


class MyGui(QtGui.QLineEdit):
    def __init__(self):
        QtGui.QLineEdit.__init__(self)
    def after_signal(self, arg):
        self.setText(arg)

app = QtGui.QApplication(sys.argv)
app.setApplicationName("tcpserver")

my_gui = MyGui()
my_gui.show()
my_gui.resize(400,40)

server = ThreadedServer()
server.httpd.qobject.my_signal.connect(my_gui.after_signal)
server.start()

app.exec_()
