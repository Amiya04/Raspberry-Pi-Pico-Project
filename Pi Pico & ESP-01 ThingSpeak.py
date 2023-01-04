import uos
import machine
import utime
from machine import Pin, I2C        #importing relevant modules & classes
import bme280       #importing BME280 library

myHOST = 'api.thingspeak.com'
myPORT = '80'
myAPI = '*****************'

print()
print("Machine: \t" + uos.uname()[4])
print("MicroPython: \t" + uos.uname()[3])

i2c=I2C(1,sda=Pin(2), scl=Pin(3), freq=400000)   #initializing the I2C method 

uart0 = machine.UART(0, baudrate=115200)
print(uart0)

def Rx_ESP_Data():
    recv=bytes()
    while uart0.any()>0:
        recv+=uart0.read(1)
    res=recv.decode('utf-8')
    return res
def Connect_WiFi(cmd, uart=uart0, timeout=3000):
    print("CMD: " + cmd)
    uart.write(cmd)
    utime.sleep(7.0)
    Wait_ESP_Rsp(uart, timeout)
    print()

def Send_AT_Cmd(cmd, uart=uart0, timeout=3000):
    print("CMD: " + cmd)
    uart.write(cmd)
    Wait_ESP_Rsp(uart, timeout)
    print()
    
def Wait_ESP_Rsp(uart=uart0, timeout=3000):
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms()-prvMills)<timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    print("resp:")
    try:
        print(resp.decode())
    except UnicodeError:
        print(resp)
    
Send_AT_Cmd('AT\r\n')          #Test AT startup
Send_AT_Cmd('AT+GMR\r\n')      #Check version information
Send_AT_Cmd('AT+CIPSERVER=0\r\n')      #Check version information
Send_AT_Cmd('AT+RST\r\n')      #Check version information
Send_AT_Cmd('AT+RESTORE\r\n')  #Restore Factory Default Settings
Send_AT_Cmd('AT+CWMODE?\r\n')  #Query the Wi-Fi mode
Send_AT_Cmd('AT+CWMODE=1\r\n') #Set the Wi-Fi mode = Station mode
Send_AT_Cmd('AT+CWMODE?\r\n')  #Query the Wi-Fi mode again
Connect_WiFi('AT+CWJAP="Redmi Note 7 Pro","abcd1234"\r\n', timeout=5000) #Connect to AP
Send_AT_Cmd('AT+CIFSR\r\n',timeout=5000)    #Obtain the Local IP Address
Send_AT_Cmd('AT+CIPMUX=1\r\n')    #Obtain the Local IP Address
utime.sleep(1.0)
print ('Starting connection to ESP8266...')
while True:
    bme = bme280.BME280(i2c=i2c)        #BME280 object created
    temperature = bme.values[0]         #reading the value of temperature
    pressure = bme.values[1]            #reading the value of pressure
    humidity = bme.values[2]            #reading the value of humidity
    print('Temperature: ', temperature[:-1])    #printing BME280 values
    print('Humidity: ', humidity[:-1])
    print('Pressure: ', pressure[:-3])
    print ('!About to send data to thingspeak')
    sendData = 'GET /update?api_key='+ myAPI +'&field1='+str(temperature[:-1]) +'&field2='+str(pressure[:-3]) +'&field3='+str(humidity[:-1])
    Send_AT_Cmd('AT+CIPSTART=0,\"TCP\",\"'+ myHOST +'\",'+ myPORT+'\r\n')
    utime.sleep(1.0)
    Send_AT_Cmd('AT+CIPSEND=0,' +str(len(sendData)+4) +'\r\n')
    utime.sleep(1.0)
    Send_AT_Cmd(sendData +'\r\n')
    utime.sleep(4.0)
    Send_AT_Cmd('AT+CIPCLOSE=0'+'\r\n') # once file sent, close connection
    utime.sleep(4.0)
    print ('Data send to thing speak')
