
import network
from time import sleep
import socket
import urequests as req
from machine import Pin
#from random import getrandbits as rndb

led = Pin(2, Pin.OUT) # set pin2 output for (board led) to show request proccess
led.value(1)          # set led off


station = network.WLAN(network.STA_IF)
print('\nStart  ###')
def conect_to_wifi(): # connect to wifi or local network 
    print("\n---------- Connect to WiFi --------------------\n")
    num=0
    ssid = "BHMN"
    password =  "BHMNBHMN"
    if station.isconnected() == True:
        print("connected to WiFi")
        print('WiFi Conection Info:',station.ifconfig())        
    else:
        station.active(True)
        station.connect(ssid, password)
        while station.isconnected() == False:
            num+=1
            if num>=5:
                print("Can't connect to WiFi")
                break 
            print('Reconnect to WiFi...')
            sleep(5)
        if station.isconnected() == True:
            print("Connection successful")    
            print('WiFi Conection Info:',station.ifconfig())
    print("-----------------------------------------------")


def direct_conect(): # config access point mode for direct connection
    print("\n---------- Access Point Configuration ---------------\n")    
    ssid = 'ESP Server'
    password = '88888888'
    ipinfo = ('5.5.5.5', '255.255.255.0', '5.5.5.1', '8.8.8.8')
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, authmode=network.AUTH_OPEN, password=password)
    ap. ifconfig(ipinfo)
    while ap.active() == False:
      pass
    print('Direct Conection Info:',ap.ifconfig())
    print("-----------------------------------------------------")
    
# call to functions for config wifi
conect_to_wifi()
direct_conect()

# make a socket to listen to the client request
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port=80
s.bind(('', port))
s.listen(5)
s.settimeout(0.5)

# function for handle requests
def req_check():
    try:
        conn, addr = s.accept()
        led.value(0)
        data=conn.recv(3000)
        data=str(data)
        print("\n---------- This request came from client ----------\n")
        print(data,'\n')
        
        try:
            if data.find(' / HTTP/1.1')>-1:
                print('\n!!!  We define request for main page and response to client  !!!\n')
                t=open('main_html.txt', 'rb')
                html = t.read()
                t.close()
                response = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + html
                conn.sendall(response)
                
            elif data.find(' /secondaryHTML')>-1:
                print('\n!!!  We define request for second page and response to client  !!!\n')
                t=open('secondary_html.txt', 'rb')
                html = t.read()
                t.close()
                response = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + html
                conn.sendall(response)
                
            elif data.find('main_pic.png')>-1:                
                print('\n!!!  We define request for main pic and response to client  !!!\n')
                p=open('mainpic.png', 'rb')
                pic = p.read()
                p.close()
                response = b'HTTP/1.1 200 OK\r\nContent-Type: image/png\r\n\r\n' + pic
                conn.sendall(response)                
                
            elif data.find('secondary_pic.png')>-1:                
                print('\n!!!  We define request for main pic and response to client  !!!\n')
                p=open('secondarypic.png', 'rb')
                pic = p.read()
                p.close()
                response = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n\r\n' + pic
                conn.sendall(response)                
                
            conn.close()
            led.value(1)
        except :
            conn.close()
            led.value(1)
    except :
        pass
        led.value(1)        

while 1:
    
    req_check() # check for request
    
    sleep(.5)