import pickle
import socket
import time

import dnslib

# ns1.e1.ru
FORWARDER = '212.193.163.6'


def get_forwarder():
    new_forwarder = input()
    if new_forwarder:
        return new_forwarder
    else:
        return FORWARDER


# forwarder = get_forwarder()
forwarder = FORWARDER


def save_cache(data):
    file = open('cache', 'wb')
    pickle.dump(data, file)
    file.close()


def load_cache():
    try:
        file = open('cache', 'rb')
        new_cache = pickle.load(file)
        file.close()
        return new_cache
    except:
        return {}


cache = load_cache()
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('127.0.0.1', 53))
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    request, address = server.recvfrom(2048)
    x = dnslib.DNSRecord.parse(request)
    # print(x)

    if cache.get((x.questions[0].qname, x.questions[0].qtype)):
        print('cache!')
        header = dnslib.DNSHeader(x.header.id, q=1, a=len(cache.get((x.questions[0].qname, x.questions[0].qtype))[0]))
        response = dnslib.DNSRecord(header, x.questions, cache.get((x.questions[0].qname, x.questions[0].qtype))[0])
        server.sendto(response.pack(), address)
    else:
        print(x)
        try:
            client.sendto(request, (forwarder, 53))
            response_from_dns, _ = client.recvfrom(2048)
            y = dnslib.DNSRecord.parse(response_from_dns)
            print(y)
            cache[(y.questions[0].qname, y.questions[0].qtype)] = y.rr, time.time()
            print()
            print(y.auth)
            print()
            if y.auth:
                cache[(y.auth[0].rname, y.auth[0].rtype)] = y.auth, time.time()
            save_cache(cache)
            header = dnslib.DNSHeader(x.header.id, q=1,
                                      a=len(cache.get((x.questions[0].qname, x.questions[0].qtype))[0]))
            response = dnslib.DNSRecord(header, x.questions, cache.get((x.questions[0].qname, x.questions[0].qtype))[0])
            server.sendto(response.pack(), address)
        except Exception as e:
            print(e)
