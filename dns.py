import json
import socket
import dnslib

PORT = 53
IP = '127.0.0.1'

# ns1.e1.ru
FORWARDER = '212.193.163.6'


def save_cache(cache):
    file = open('cache.json', 'w')
    json.dump(cache, file)
    file.close()


try:
    file = open('cache.json', 'r')
    cache = json.load(file)
    file.close()
except:
    cache = {}

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('127.0.0.1', PORT))


def create_response(data):
    id = data[:2]
    str_id = ''
    for byte in id:
        str_id += str(byte)
    print(str_id)
    return b'dfs'


while True:
    request, addr = server.recvfrom(1024)
    print(request)
    print(dnslib.DNSRecord.parse(request))

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto(request, (FORWARDER, PORT))
    response, addr2 = client.recvfrom(1024)
    print()
    create_response(request)
    print(response)
    print(dnslib.DNSRecord.parse(response))
    #response = create_response(request)
    server.sendto(response, addr)
