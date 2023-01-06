import click
import requests
from datetime import datetime
import json
import sqlite3
import os
import pandas as pd
import re
import pyshark
import subprocess
import evtx
import requests
import shutil

#requesty fastAPI

#log_file = open('Databases/'''tutaj log jaki chcemy analizować''', 'a')
#con = sqlite3.connect('Databases/)
#cur = con.cursor()
'''cur.execute(
    CREATE TABLE IF NOT EXISTS app_events (date_time DATETIME, command Varchar(255), user_id Varchar(10), path Varchar(255)))
'''

'''
@click.command()
@click.option('-f' , '--file', help='File to analyse', type=str)
def filename(file):
    extension = file.split('.')[-1]
    if (extension in ['txt', 'pcap', 'evtx', 'json', 'xml']):
        print('Supported extension')
    else:
        print('Unsupported extension')


'''
def file_handling(file_path, re_pattern, grep_pattern, bpf_filter):
    output = ""

    if file_path.endswith('.txt') or file_path.endswith('.xml') or file_path.endswith('.json'):
        if re_pattern != "" and grep_pattern != "":
            output = "Two patterns instead of one."
        elif re_pattern != "":
            with open(file_path, "r") as file:
                for line in file:
                    if re.search(re_pattern, line):
                        output += line

        elif grep_pattern != "":

            output = subprocess.check_output("grep " + grep_pattern + " " + file_path, shell=True).decode("utf-8")
            output = str(output)

        else:
            with open(file_path, "r") as file:
                for line in file:
                    output += line

        return output

    elif file_path.endswith('.pcap') or file_path.endswith('.pcapng'):
        shark_cap = pyshark.FileCapture(file_path, display_filter=bpf_filter)
        for packet in shark_cap:
            output += str(packet)

        return output

    elif file_path.endswith('.evtx'):
        with evtx.Evtx(file_path) as log:
            for record in log.records():
                payload = str(record.xml())
                output += payload
        return output

    else:
        output = "Bad file extension. Try one of (.txt, .xml, .json, .pcap, .evtx) "
        return output

def scan_file(file_path, rule):
    detection_rules = __import__('detection-rules')
    method = getattr(detection_rules, rule)
    result = method(file_path)
    return result

def process_output(output, firewall, console):
    if output[0] == "remote" and console != "":
        pload = {'action_alert': str(output[0]), 'action_block': str(output[1]), 'description': str(output[2])}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(f'http://{console}/', data=json.dumps(pload), headers=headers)

    if output[1] and firewall != "":
        if output[2].find("suspicious ip") > -1 or output[2].find("suspicious number of ips") > -1 or output[2].find("untrusted ports") > -1:
            pload = {'rule': "BLOCK", 'value': str(output[3])}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(f'http://{firewall}/', data=json.dumps(pload), headers=headers)

@click.group()
def application():
    pass
@application.command()
@click.option('--file_path', multiple=True, type=click.Path(exists=True))
@click.option('--re_pattern', default="")
@click.option('--grep_pattern', default="")
@click.option('--bpf_filter', default="")
def read_file(file_path, re_pattern, grep_pattern, bpf_filter):
    now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    #log_file.write(now + ':   ')

    user_id = os.getuid()
    events = (now, "read_file", user_id, str(file_path))
    #cur.execute("insert into app_events values (?, ?, ?, ?)", events)
    #con.commit()
    output = ""
    for pth in file_path:
        if os.path.isfile(pth):
            output = file_handling(pth, re_pattern, grep_pattern, bpf_filter)
            click.echo(output)
        elif os.path.isdir(pth):
            for root, directories, files in os.walk(pth, topdown=False):
                for name in files:
                    output = file_handling(os.path.join(root, name), re_pattern, grep_pattern, bpf_filter)
                    click.echo(output)

    #con.close()
    #log_file.write("\n" + " read_file: " + str(output) + "\n\n")
    #log_file.close()

if __name__ == '__main__':
    print('CLI Application Started...')