import asyncio

from chainlist import ChainList


chain = ChainList()
async def main():
	# await chain.get_chains_names() # генерирует файл json с корректными названиями сетей (как нужно для апи)
	a = await chain.get_rpcs_list(chain_name='Base') # возвращает список рабочих  rpc с отсутствующим либо низким уровней слежки за пользователем
	print(a)

if __name__ == '__main__':
	asyncio.run(main())