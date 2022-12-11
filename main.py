from scapy.all import *
import requests
import time
import os
import threading

localip = requests.get("https://httpbin.org/ip").json()["origin"]

ip2geolocate = {}

def GetLocation(ip):
    response = requests.get(f'http://ip-api.com/json/{ip}')
    response = response.json()
    location_data = {
        "ip": ip,
        "city": response.get("city"),
        # "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data

def udp_filter(pkt):
    if pkt.haslayer(IP) and pkt.haslayer(UDP):
        ip = pkt[IP].src
        if ip not in ip2geolocate or ip == localip:
            ip2geolocate[ip] = GetLocation(ip)
   
def ThreadFunc():
    sniff(filter="udp", prn=udp_filter)
        
threading.Thread(target=ThreadFunc).start()

time.sleep(3)
for ip in ip2geolocate:
    if ip2geolocate[ip]["city"] != None:
        print(ip2geolocate[ip]["ip"] + ": " + ip2geolocate[ip]["city"])
os._exit(0)
