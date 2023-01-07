# TODO:
#  OFF.LOG.1 zrob mozliwosc wywołania operacji systemowej grep
#  na wskazanych plikach tekstowych. Argumentem przekazywanym do operacji
#  jest właściwe wyrażenie regularne.
#  OFF.LOG.2 zrob możliwość wywołania działania wyrażenia regularnego z modułu Python
#  re na wskazanych plikach tekstowych lub EVTX przetworzonych do formatu JSON/XML/inny tekstowy.
#  Argumentem przekazywanym do operacji jest właściwe wyrażenie regularne.
#  pomocne linki:
#  https://appdividend.com/2021/05/03/python-grep/
#  https://stackoverflow.com/questions/1921894/grep-and-python
#  https://stackoverflow.com/questions/15026357/use-grep-on-file-in-python

import json
import click
from datetime import datetime
import sqlite3
import os
import pandas as pd
import re
import pyshark
import subprocess
import requests
import shutil

    #f = file_path
    #grep = grep_pattern
    #rep = re_pattern
    #bpf = bpf_filter)
def file_version_manager(f, rep, grep, bpf):
    output = ""


    if f.endswith('.txt') or f.endswith('.json') or f.endswith('.xml'):
        if rep != "" and grep != "":
            output = "Zbyt wiele operacji, wybierz jedna."

        elif grep != "":
            output = str(subprocess.check_output("grep " + grep + " " + f, shell=True).decode("utf-8"))

        elif rep != "":
            with open(f, "r") as file:
                for line in file:
                    if re.search(rep, line):
                        output += line

        else:
            with open(f, "r") as file:
                for line in file:
                    output = output + line

        return output

    elif f.endswith('.pcap') or f.endswith('.pcapng'):
        shark_cap = pyshark.FileCapture(f, display_filter=bpf)
        for packet in shark_cap:
            output += str(packet)

        return output

    else:
        output = "Zle rozszerzenie pliku. Uzyj jednego z rozszerzen: .txt, .xml, .json, .pcap "
        return output


def scanning_file(f, rule):
    detection_rules = __import__('detection-rules')
    method = getattr(detection_rules, rule)
    result = method(f)
    return result
