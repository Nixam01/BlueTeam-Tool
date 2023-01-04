import pyshark
from fileHandler import *


def read_packet(file, bpf_filter):
    packets = pyshark.FileCapture(file, display_filter=bpf_filter)
    for packet in packets:
        print(packet)

# testing

# def main():
#     check_path('../../src')
#     read_packet('../../sample.pcap', 'arp')
#
#
# if __name__ == '__main__':
#     main()
