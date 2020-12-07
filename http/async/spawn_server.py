from asyncio_http import *

for port in range(8000,8001):
    try: 
        loop.run_until_complete(asyncio.gather(init(port)))
    except Exception as error: 
        print(error)
        pass
loop.run_forever()