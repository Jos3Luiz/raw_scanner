import socket
import struct
def parsePckt(p):
  d={8:"Echo Request",0:"Echo Reply",3:"Destination Unreachable",11:"Time Exceeded Message",12:"Parameter Problem Message",4:"Source Quench Message",
  5:"Redirect Message",13:"Timestamp or Timestamp Message",14:"Timestamp Reply Message",15:"information request message",16:"information reply message"}
  icmpHeader=p[20:28]
  typed,code,checksum,packetID,sequence=struct.unpack("bbHHh",icmpHeader) 
  print(f"""[type={typed}] -> {d[typed] if typed in d else "Unkown"} - code = {code} / sequence={sequence}""")


def listen():
  s = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP)
  s.setsockopt(socket.SOL_IP, socket.IP_HDRINCL, 1)
  while 1:
    data, addr = s.recvfrom(1508)
    print(f"Recived ICMP from [{addr}]")
    parsePckt(data)

listen()
