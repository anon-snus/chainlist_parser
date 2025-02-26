import asyncio
from libs.eth_async.utils.utils import async_get, async_post
from bs4 import BeautifulSoup
import json
import random
class ChainList:
	def __init__(
			self,
			proxy:str|None = None
	):
		self.proxy=proxy
		

	async def get_chains_names(self):
		'''
		:return: json file with chain names supported by chainlist
		'''
		url = 'https://chainlist.org/'
		for i in range(5):
			try:
				resp = await async_get(url, response_type='text', proxy=self.proxy)
				soup = BeautifulSoup(resp, 'html.parser')
				script_tag = soup.find("script", {"id": "__NEXT_DATA__", "type": "application/json"})
				data = json.loads(script_tag.string)
				chain_names = []
				for i in data['props']['pageProps']['chains']:
					chain_names.append({'name': i['name'], 'chain': i['chain']})
				with open("chains.json", "w", encoding="utf-8") as json_file:
					json.dump(chain_names, json_file, ensure_ascii=False, indent=4)
				print("Результат сохранён в 'chains.json'.")
				return chain_names
			except Exception as e:
				print(e)
				await asyncio.sleep(1)
		print('Не получилось получить названия сетей')

	async def get_rpcs_list(self, chain_name:str, connection_type:str='htt', current_rpc:str|None=None):
		'''
		finds list of public working https rpcs with no or small tracking
		:param connection_type: type of connection put 'htt' for https or 'wss' for wss
		:param chain_name: get chain name from chains.json for correct work
		:return: list of good rpcs
		'''
		url = 'https://chainlist.org/'
		print(f'Looking for {chain_name} rpcs...')
		for i in range(5):
			try:
				resp = await async_get(url, response_type='text', proxy=self.proxy)
				soup = BeautifulSoup(resp, 'html.parser')
				script_tag = soup.find("script", {"id": "__NEXT_DATA__", "type": "application/json"})
				data = json.loads(script_tag.string)
				rpcs_list = []
				json_data = {
					'jsonrpc': '2.0', 'method': 'eth_getBlockByNumber', 'params': ['latest', False, ], 'id': 1,
				}
				for i in data['props']['pageProps']['chains']:
					if i['name'].lower() == chain_name.lower():
						for n in i['rpc']:
							if 'tracking' in n:
								if n['tracking'] == 'none' or n['tracking'] == 'limited':
									if n['url'][:3] == connection_type:
										try:
											a = await async_post(url=n['url'], json=json_data, timeout=1, proxy=self.proxy)
											if a:
												if n['url'] != current_rpc:
													return n['url']
												# rpcs_list.append(n['url'])
												# return n['url']
										except Exception as e:
											pass
				# return random.choice(rpcs_list)
			except Exception as e:
				print(e)
				await asyncio.sleep(1)
		print('Не получилось получить список rpc')
