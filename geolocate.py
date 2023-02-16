import argparse
import requests
from pathlib import Path
import re
import sys
import ipaddress


def ip_iter(ip):
    if args.file or args.cidr != None:
        if args.file:
         
            ips = open(ip,'r').readlines()
            
        else:
            ips = list(ipaddress.ip_network(ip))
        for ip in ips:
            ip = str(ip).strip()
            geo_locate_html(ip)
    else:
        geo_locate_html(ip)

def geo_locate_html(ip):
    
    url = 'https://ipgeolocation.io/ip-location/'
    print(url+ip)
    ip_info = requests.get(url+ip).text
    
    get_ip = re.search(r'<td>(IP)</td>\n<td id="ipaddrs">(.+)</td>\n',ip_info)
    get_org = re.search(r'<td>(Organization)</td>\n<td>(.*)</td>\n',ip_info)
    get_location = re.search(r'<td>(State/Province)</td>\n<td>(.+)</td>\n</tr>\n<tr>\n<td>District/County</td>\n<td></td>\n</tr>\n<tr>\n<td>(City)</td>\n<td>(.+)</td>\n</tr>\n<tr>\n<td>(Zip Code)</td>\n<td>(.*)</td>\n</tr>\n<tr>\n<td>(Latitude & Longitude of City)</td>\n<td>(.+)</td>',ip_info)
    
    ip_addr = [get_ip.groups()[0],get_ip.groups()[1]]
    org = [get_org.groups()[0],get_org.groups()[1]]
    state = [get_location.groups()[0],get_location.groups()[1]]
    city = [get_location.groups()[2],get_location.groups()[3]]
    zipcode = [get_location.groups()[4],get_location.groups()[5]]
    coords = [get_location.groups()[6],get_location.groups()[7]]
    
    print(": ".join(ip_addr))
    if org[1] != "":
        print(": ".join(org))
    print(": ".join(state))
    print(": ".join(city))
    if zipcode[1] != "":
        print(": ".join(zipcode))
    print(": ".join(coords))
    print("\n")

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-i','--ip-addr',help='Single IPv4 Address to perform geolocate on',action='store')
    group.add_argument('-f','--file',help='A file containing IPv4 Addresses to perform geolocate on',action='store')
    group.add_argument('-c','--cidr',help='IPv4 CIDR range to perform geolocate on',action='store')
    args = parser.parse_args()

    if args.ip_addr != None:
        ip = args.ip_addr
        try:
            checkip = ipaddress.IPv4Address(ip)
        except Exception as e:
            print(e)
            print('Supplied string does not appear to be a valid IP Address...exing')
            sys.exit()
    elif args.file != None:
        ip = args.file
        checkfile = Path(ip).is_file
        if checkfile == False:
            print('Supplied argument is not a valid file name, please provide the correct path...exiting')
            sys.exit()
    else:
        ip = args.cidr
        try:
            confirm_net = ipaddress.ip_network(ip)
        except Exception as e:
            print(e)
            print('Argument supplied is not a valid CIDR, please provide the correct value...exiting')
            sys.exit()
    
    ip_iter(ip)
