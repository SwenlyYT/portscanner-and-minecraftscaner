import requests
from time import sleep
import json
import os

ip = input('Введите айпи: ')

start_port = int(input('Введите порт с которого будет начинаться скан: '))
if start_port < 1:
    start_port = 1

end_port = int(input('Введите порт на который будет заканчиваться скан: '))
if end_port > 65535:
    end_port = 65535

_format = input('Сохранять в формате ip:port? (y/n) ')
if _format.lower() == 'y' or _format.lower() == 'yes' or _format.lower() == 'да' or _format.lower() == 'пизда':
    _format = 'y'
else:
    _format = 'n'

with open(f'saves/{ip} {start_port} - {end_port}.txt', 'w') as f:
    f.write('')

print()

def portscan(ip):
    HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'}


    data = {
	"remoteHost": ip,
	"start_port": start_port,
	"end_port": end_port,
	"normalScan": "Yes",
	"scan_type": "connect",
	"ping_type": "none"
}

    r = requests.post(f'https://www.ipfingerprints.com/scripts/getPortsInfo.php', data=data, headers=HEADERS)

    json_object = json.loads(r.text)
    otvet = json_object['portScanInfo']
    all_opens = str(otvet).split('/tcp')
    count_ports = 0

    for port in all_opens:
        try:
            aboba = port.split('\n')
            count = len(aboba) - 1
            msg = aboba[count]
            if '<' in msg or '>' in msg:
                continue
            print(msg, 'is open')
            with open(f'saves/{ip} {start_port} - {end_port}.txt', 'a') as f:
                if _format == 'n':
                    f.write(msg + '\n')
                else:
                    f.write(ip + ':' + msg + '\n')
            count_ports += 1
        except:
            continue
        # op = str(otvet).split(str(port))[0]
        # op = op.split('\n')
        # count = len(op) - 1
        # op = op[count]
        # print('Port open - ' + op)
    
    print(f'В итоге открытых портов нашлось ровно {count_ports}')

portscan(ip)

vopros = input('Сохранить результат? (y/n) ')
if vopros.lower() != 'y' and vopros.lower() != 'yes' and vopros.lower() != 'да':
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), f'saves/{ip} {start_port} - {end_port}.txt')
    os.remove(path)

input()