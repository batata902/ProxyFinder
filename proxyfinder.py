#!/usr/bin/python3
import requests
import argparse
import json

logo = '''\033[32m
::::::::: :::::::::  :::::::: :::    ::::::   ::::::::::::::::::::::::::::    :::::::::::: :::::::::::::::::::  
:+:    :+::+:    :+::+:    :+::+:    :+::+:   :+::+:           :+:    :+:+:   :+::+:    :+::+:       :+:    :+: 
+:+    +:++:+    +:++:+    +:+ +:+  +:+  +:+ +:+ +:+           +:+    :+:+:+  +:++:+    +:++:+       +:+    +:+ 
+#++:++#+ +#++:++#: +#+    +:+  +#++:+    +#++:  :#::+::#      +#+    +#+ +:+ +#++#+    +:++#++:++#  +#++:++#:  
+#+       +#+    +#++#+    +#+ +#+  +#+    +#+   +#+           +#+    +#+  +#+#+#+#+    +#++#+       +#+    +#+ 
#+#       #+#    #+##+#    #+##+#    #+#   #+#   #+#           #+#    #+#   #+#+##+#    #+##+#       #+#    #+# 
###       ###    ### ######## ###    ###   ###   ###       ##############    ############# #############    ### \033[m
v1.0

by \033[31mLazByte\033[m
\033[33mGithub\033[m: https://github.com/batata902/
'''

print (logo)
help = '''
Usage: python3 proxyfinder.py

args:
-pE		Filter by proxys with elite anonymity level
-s4		Filter by socks4 proxys
-s5		Filter by socks5 proxys
-http		Filter by http proxys
--restime	Set the maximum allowed response time for a proxy
-o		Save "protocol:ip:port" in a output file
-f		Filter proxies by specific words or characters

Usage examples:

~$ python3 proxyfinder.py -pE (Return only proxies that have an elite anonymity level)

~$ python3 proxyfinder.py -s4/s5/http (Return only socks4, socks5 or http proxy)

~$ python3 proxfinder.py -s5 --restime 500 -o proxies.txt (Return socks5 proxies with 500 as maximum response time and save it in a file.)
'''


parser = argparse.ArgumentParser(usage=help)
parser.add_argument('-pE', action='store_true', help='Filter by proxys with elite anonymity level')
parser.add_argument('-s4', action='store_true', help='Filter by socks4 proxys')
parser.add_argument('-s5', action='store_true', help='Filter by socks5 proxys')
parser.add_argument('-http', action='store_true', help='Filter by http proxys')
parser.add_argument('--restime', type=int, help='Set the max response time')
parser.add_argument('-f', type=str, help='Filter by words')
parser.add_argument('-o', type=str, help='Output file -> protocol:ip:port')
args = parser.parse_args()

argumentos = []
if args.s4:
	argumentos.append('socks4')
if args.s5:
	argumentos.append('socks5')
if args.http:
	argumentos.append('http')

proxys = {}
alreadyshow = []


def save_in_file(proxy):
	with open(args.o, 'a') as f:
		f.write(f'{proxy["protocols"][0]}:{proxy["ip"]}:{proxy["port"]}\n')
	print (f'Stored at -> {args.o}')


def get_proxy_list():
	global proxys
	headers = {'Content-Type': 'application/json'}
	s = requests.Session()
	for i in range(1, 19):
		req_proxys = s.get(f'https://proxylist.geonode.com/api/proxy-list?limit=500&page={i}&sort_by=lastChecked&sort_type=desc').text
	proxys = proxys | json.loads(req_proxys)
	return


def show_proxy_infos(proxy, mark):
	proxy_str = ''
	show = False

	for key, value in proxy.items():
		key_str = str(key)
		value_str = str(value)

		if mark is not None:
			if mark in  key_str or mark in value_str:
				show = True
				key_str = key_str.replace(mark, f'\033[32m{mark}\033[m')
				value_str = value_str.replace(mark, f'\033[32m{mark}\033[m')
		else:
			show = True

		proxy_str += f"{key_str}: {value_str}\n"

	if show:
		print ('[\033[32m+\033[m] Proxy found!')
		print (proxy_str)


def tratar_proxy(proxy, mark, save=False):
	show_proxy_infos(proxy, mark)
	alreadyshow.append(proxy['_id'])
	if save:
		save_in_file(proxy)
	return


def isfit(proxy, mark, save=False):
	if proxy['_id'] not in alreadyshow:
		if args.pE and proxy["anonymityLevel"] == 'elite':
			if len(argumentos) == 0:
				tratar_proxy(proxy, mark, save)
				return
			if proxy['protocols'][0] in argumentos:
				tratar_proxy(proxy, mark, save)
				return
		if len(argumentos) == 0:
			tratar_proxy(proxy, mark, save)
			return
		if proxy['protocols'][0] in argumentos:
			tratar_proxy(proxy, mark, save)
			return


'''
	        if args.pE:
	                if proxy["anonymityLevel"] == "elite":
	                        show_proxy_infos(proxy, mark)
	                        alreadyshow.append(proxy['_id'])
	                        if save:
	                        	save_in_file(proxy)
	                        return
	        if args.s4:
	                if 'socks4' in proxy['protocols']:
	                        show_proxy_infos(proxy, mark)
	                        alreadyshow.append(proxy['_id'])
	                        if save:
	                        	save_in_file(proxy)
	                        return
	        if args.s5:
	                if 'socks5' in proxy['protocols']:
	                        show_proxy_infos(proxy, mark)
	                        alreadyshow.append(proxy['_id'])
	                        if save:
	                        	save_in_file(proxy)
	                        return
	        if args.http:
	                if 'http' in proxy['protocols']:
	                        show_proxy_infos(proxy, mark)
	                        alreadyshow.append(proxy['_id'])
	                        if save:
	                        	save_in_file(proxy)
	                        return
	        if not (args.pE or args.s4 or args.s5 or args.http):
	                show_proxy_infos(proxy, mark)
	                alreadyshow.append(proxy['_id'])
	                return
	        return
'''

if __name__ == '__main__':
	print ('[\033[32mINFO\033[m] Looking for proxies...')
	get_proxy_list()
	save = False
	mark = None
	if args.o:
		save = True
	if args.f:
		mark = args.f
	for proxy in proxys['data']:
		if args.restime:
			if int(proxy['responseTime']) < args.restime:
				isfit(proxy, mark, save)
		else:
			isfit(proxy, mark, save)
	if args.o:
		print (f'[\033[32m+\033[m] Saved in -> {args.o}')


