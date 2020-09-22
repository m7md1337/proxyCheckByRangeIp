import requests
import itertools


def ip_range(input_string):
    octets = input_string.split('.')
    chunks = [map(int, octet.split('-')) for octet in octets]
    ranges = [range(c[0], c[1] + 1) if len(c) == 2 else c for c in chunks]

    for address in itertools.product(*ranges):
        yield '.'.join(map(str, address))


timeouts= 3 # change if u want 
req  = requests.get("https://api.ipify.org/")
currnet_ip = req.content
ip_scan = '.'.join(currnet_ip.split('.')[0:2]) + ".0-255" + ".0-255"


for port8008 in ip_range(ip_scan):
	try:
		proxyDictionary = {
				"https": 'https://' + port8008+':8080'
		}
		res = requests.get("https://api.ipify.org/", proxies=proxyDictionary,timeout=timeouts)
		if res.status_code == 200:
			with open("proxylive.txt", 'a') as f:
				f.write("proxy:"+port8008+':8080'+"")
			print('proxy', port8008+':8080', 'is alive')
	except requests.exceptions.ConnectionError:
		print('[Proxy failed', port8008+':8080','reason:'+'error')
	except requests.exceptions.ConnectTimeout:
		print('[Proxy failed', port8008+':8080','reason:'+'Error,Timeout!')
	except requests.exceptions.HTTPError:
		print('[Proxy failed', port8008+':8080','reason:'+'HTTP ERROR!')
	except requests.exceptions.Timeout:
		print('[Proxy failed', port8008+':8080','reason:'+'Error! Connection Timeout!')
	except requests.exceptions.TooManyRedirects:
		print('[Proxy failed', port8008+':8080','reason:'+'ERROR! Too many redirects!')


f = open("proxylive.txt", "r")
print('[All         ] Working Proxies')
print(f.read())
