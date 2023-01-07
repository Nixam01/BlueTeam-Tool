import click
#from datetime import datetime
import json
import os
import requests


#requesty fastAPI



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

    for pth in file_path:
        if os.path.isfile(pth):
            output = file_handling(pth, re_pattern, grep_pattern, bpf_filter)
            click.echo(output)
        elif os.path.isdir(pth):
            for root, directories, files in os.walk(pth, topdown=False):
                for name in files:
                    output = file_handling(os.path.join(root, name), re_pattern, grep_pattern, bpf_filter)
                    click.echo(output)

@application.command()
@click.option('--action', multiple=False, help="Action you want to perform (one of netconfig)")
@click.option('--agent_host', multiple=False, help="ip:port")
@click.option('--interface', multiple=False, help="Interface to capture traffic on")
@click.option('--capture_filter', default="", multiple=False, help="Capture filter")
@click.option('--timeout', multiple=False, help="Time of capturing")
@click.option('--file_number', multiple=True, help="Number of file to download")
@click.option('--command', multiple=False, help="Command to execute")

def agent(action, agent_host, interface, capture_filter, timeout, file_number, command):
    if action == 'netconfig':
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.get(f'http://{agent_host}/netconfig', headers=headers)
        result = str(r.content).replace('\\n', '\n').replace('\\t', '\t')
        click.echo(result)

    elif action == 'capture':
        pload = {"interface": interface, "filter": capture_filter, "timeout": str(timeout)}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        response = requests.post(f'http://{agent_host}/capture', data=json.dumps(pload), headers=headers, stream=True)
        file_name = "Files_application/pcaps/" + str(datetime.now().strftime("%d-%m-%Y_%H-%M-%S")) + ".pcap"
        if response.status_code == 200:
            with open(file_name, 'wb') as f:
                f.write(response.content)

    elif action == 'list_pcaps':
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.get(f'http://{agent_host}/list-pcaps', headers=headers)
        click.echo(r.content)

    elif action == 'list_logs':
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.get(f'http://{agent_host}/list-logs', headers=headers)
        click.echo(r.content)

    elif action == 'download_pcap':
        for file in file_number:
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.get(f'http://{agent_host}/list-pcaps', headers=headers)
            json_str = str(r.content)
            json_str = json_str[3:-2]
            list = json_str.split(',')
            file_name = "Files_application/pcaps/" + list[int(file)-1][4:-1]

            parameters = {"nr": file}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            response = requests.get(f'http://{agent_host}/download-pcap', params=parameters, headers=headers, stream=True)
            if response.status_code == 200:
                with open(file_name, 'wb') as f:
                    f.write(response.content)

    elif action == 'download_log':
        for file in file_number:
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.get(f'http://{agent_host}/list-logs', headers=headers)
            json_str = str(r.content)
            json_str = json_str[3:-2]
            list = json_str.split(',')
            file_name = "../database/downloads/logs/" + list[int(file)-1][4:-1]

            parameters = {"nr": file}
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            response = requests.get(f'http://{agent_host}/download-log', params=parameters, headers=headers, stream=True)
            if response.status_code == 200:
                with open(file_name, 'wb') as f:
                    f.write(response.content)
    elif action == 'command':
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        payload = {"command": command}
        r = requests.post(f'http://{agent_host}/command', headers=headers, data=json.dumps(payload))
        result = str(r.content).replace('\\n', '\n').replace('\\t', '\t')
        click.echo(result)

    else:
        click.echo("Invalid action")


if __name__ == '__main__':
    application()
    print('CLI Application Started...')