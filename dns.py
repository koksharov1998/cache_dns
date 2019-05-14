import pickle
import socket

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
    file = open('cache', 'w')
    pickle.dump(data, file)
    file.close()


def load_cache():
    try:
        file = open('cache', 'r')
        new_cache = pickle.load(file)
        file.close()
        return new_cache
    except:
        return {}


cache = load_cache()
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('127.0.0.1', 53))
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def parse_data(data):
    id = ''
    for byte in data[:2]:
        id += str(byte)
    print('ID: ' + id)

    print(bin(ord(str(data[2]))))
    # qr = bin(ord(data[2]))
    # print(qr)

    questions_count = ''
    for byte in data[5:7]:
        questions_count += str(byte)
    print('Questions count: ' + questions_count)
    return b'dfs'


while True:
    request, address = server.recvfrom(2048)
    x = dnslib.DNSRecord.parse(request)

    if cache.get((x.questions[0].qname, x.questions[0].qtype)):
        print('cache!')
        header = dnslib.DNSHeader(x.header.id, q=1, a=len(cache.get((x.questions[0].qname, x.questions[0].qtype))))
        response = dnslib.DNSRecord(header, x.questions, cache.get((x.questions[0].qname, x.questions[0].qtype)))
        server.sendto(response.pack(), address)
    else:
        client.sendto(request, (forwarder, 53))
        response_from_dns, _ = client.recvfrom(2048)
        y = dnslib.DNSRecord.parse(response_from_dns)
        cache[(y.questions[0].qname, y.questions[0].qtype)] = y.rr
        # save_cache(cache)
        header = dnslib.DNSHeader(x.header.id, q=1, a=len(cache.get((x.questions[0].qname, x.questions[0].qtype))))
        response = dnslib.DNSRecord(header, x.questions, cache.get((x.questions[0].qname, x.questions[0].qtype)))
        server.sendto(response.pack(), address)

    '''
    print(x)
    print(x.questions[0])
    print(x.ar)
    print()
    '''
    #client.sendto(request, (forwarder, 53))
    #response, addr2 = client.recvfrom(2048)
    #y = dnslib.DNSRecord.parse(response)
    '''
    print(y)
    print(y.questions)
    print(y.ar)
    print(y.rr)
    print(y.auth)
    print()
    '''
    #server.sendto(response, address)
    #save_cache(cache)
