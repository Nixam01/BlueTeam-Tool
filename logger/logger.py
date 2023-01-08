import os
import requests
import logging
from fastapi import FastAPI

from datetime import datetime



def log(data, function_name):
    file_name = function_name + '-' + datetime.now().strftime("%d-%m-%Y-%H:%M:%S")+'.txt'
    path = '/var/log/logs/'
    fp = path+file_name
    command = 'touch '+ fp
    os.system(command)
    with open(fp, 'w') as f:
        f.write(data)

app = FastAPI()

@app.route('/send', methods=['POST'])
def send_data():
    data = requests.data.decode('utf-8')
    print(data)
    return data

if __name__ == '__main__':
    app.run(host='localhost', port=5001, debug=False)