import kivy
import socket
import time

UDP_IP = "192.168.1.65"
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.bind((UDP_IP, UDP_PORT))

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty



class GG(Widget):
    def on_touch_move(self, touch):
        print("Mouse Move", touch.x)
        XX = str(touch.x).encode('utf-8')
        YY = str(touch.y).encode('utf-8')
        #time.sleep(1)
        sock.sendto(XX, (UDP_IP, UDP_PORT))
        sock.sendto(YY, (UDP_IP, UDP_PORT))
class MyApp(App):
    def build(self):
        return GG()

if __name__ == '__main__':
    MyApp().run()