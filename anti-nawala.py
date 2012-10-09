import socket
import simplejson as json
from python_rest_client.restful_lib import Connection

class DNSQuery:
  def __init__(self, data):
    self.data=data
    self.domain=''

    tipo = (ord(data[2]) >> 3) & 15   # Opcode bits
    if tipo == 0:                     # Standard query
      ini=12
      lon=ord(data[ini])
      while lon != 0:
        self.domain+=data[ini+1:ini+lon+1]+'.'
        ini+=lon+1
        lon=ord(data[ini])

  def request(self, ip):
    packet=''
    if self.domain:
      packet+=self.data[:2] + "\x81\x80"
      packet+=self.data[4:6] + self.data[4:6] + '\x00\x00\x00\x00'   # Questions and Answers Counts
      packet+=self.data[12:]                                         # Original Domain Name Question
      packet+='\xc0\x0c'                                             # Pointer to domain name
      packet+='\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'             # Response type, ttl and resource data length -> 4 bytes
      packet+=str.join('',map(lambda x: chr(int(x)), ip.split('.'))) # 4bytes of IP
    return packet

if __name__ == '__main__':
  ip='127.0.0.1'
  print 'pyminifakeDNS:: dom.query. 60 IN A %s' % ip
  
  udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  udps.bind(('127.0.0.1',53))
  
  try:
    while 1:

      data, addr = udps.recvfrom(1024)
      p=DNSQuery(data)

      base_url = "http://dig.jsondns.org/IN/" + p.domain
      conn = Connection(base_url)
      qr = conn.request_get("/A", args={})
      qr2 = qr['body']
      obj = json.loads(qr2)
      obj2 = obj['answer']
      ip = obj2[0][u'rdata']

      udps.sendto(p.request(ip), addr)

      # Write to HOSTS file
      f = open('/etc/hosts', 'a')
      f.write(ip + ' ' + p.domain[:-1] + '\n')
      f.close()

      print 'Request: %s -> %s' % (p.domain, ip)
  except KeyboardInterrupt:
    print 'Keyboard Interrupt'
    udps.close()
