import socket,struct

#https://datatracker.ietf.org/doc/html/rfc791#section-2.2
#https://datatracker.ietf.org/doc/html/rfc792

PROT_TCP=6
PROT_UDP=17
PROT_IP=4
PROT_ICMP=1


def make_ipv4_wrap(srcip, dstip, data,opt_prot=17,opt_ttl=64,opt_frgoff=0,opt_options=b""):
    srcip = socket.inet_aton(srcip)
    dstip = socket.inet_aton(dstip)

    padding = (len(opt_options) % 4) * b"\x00"
    ver = 4     #Version 4 for IPv4
    ihl = 5     #Header length in 32 bit words. 5 words == 20 bytes
    dscp_ecn = 0#Optional fields, don't feel like implementing. Let's keep it at 0
    tlen = len(data)+20 + len(opt_options + padding) #Length of data + 20 bytes for ipv4 header + 8 bytes for udp     header
    ident = socket.htons(54321) #ID of packet
    flg_frgoff = opt_frgoff #Flags and fragment offset
    ttl = opt_ttl #Time to live
    ptcl = opt_prot #Protocol, 17 (UDP)
    chksm = 0 #Will automatically fill in checksum    

    

    return struct.pack(
        "!"     #Network(Big endian)
        "2B"    #Version and IHL, DSCP and ECN
        "3H"    #Total Length, Identification, Flags and Fragment Offset
        "2B"    #Time to live, Protocol
        "H"     #Checksum
        "4s"    #Source ip
        "4s"    #Destination ip
        , (ver << 4) + ihl, dscp_ecn, tlen, ident, flg_frgoff, ttl, ptcl, chksm, srcip, dstip) +opt_options +data + padding


def make_udp(srcprt, dstprt, data):
    return struct.pack(
        "!4H"   #Source port, Destination port, Length, Checksum
        , srcprt, dstprt, len(data)+8, 0) + data




    



s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)

dstAddr="172.25.191.124"
srcAddr="172.25.191.124"
#srcAddr="1.1.1.1"
#packet = makepacket((srcAddr, 1000), (dstAddr, 10101), b"asdf")
packet = make_ipv4_wrap(srcAddr,dstAddr,make_udp(55000,10101,b"Ola Mundo!"))
#packet = make_ipv4_wrap(srcAddr,"192.168.0.1",packet,opt_prot=4)
s.sendto(packet, (dstAddr, 10101))