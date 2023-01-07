import re
import pyshark
import subprocess

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

            try:
                output = subprocess.check_output("grep " + grep_pattern + " " + file_path, shell=True).decode("utf-8")
            except:
                output = ""
            else:
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

    else:
        output = "Bad file extension. Try one of (.txt, .xml, .json, .pcap, .evtx) "
        return output


def scan_file(file_path, rule):
    detection_rules = __import__('detection-rules')
    method = getattr(detection_rules, rule)
    result = method(file_path)
    return result

