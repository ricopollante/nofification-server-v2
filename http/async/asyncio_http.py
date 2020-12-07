from aiohttp import web
import asyncio
import random
import requests
from model import * 
from auth.token_auth import token_encode, token_verify


async def saveData(description, date, time, app_id, user_id):
   #await asyncio.sleep(random.randint(0, 1))
   add_notif = Notifications(description, date, time, app_id, user_id)

   try:
       db.session.add(add_notif)
       db.session.commit()
   except Exception as error:
       print(error)
       db.session.rollback()

#Login & Get Token
#http://127.0.0.1:8003/login?username=admin&password=root
async def login(request):
    username = request.rel_url.query['username']
    password = request.rel_url.query['password']
    try:
        query_admin = SuperAdmin.query.filter_by(username=username)
        dump_pass = superadmin_all_schema.dump(query_admin)[0]
        if dump_pass['password'] == password:
            result = token_encode(username)

        else: 
            result = "INVALID LOGIN" 
    except:
        result = "INVALID LOGIN" 
    return web.json_response({"token" :result}) 
#INPUT DATA
##http://127.0.0.1:8003/add?app=buzz&date=12/09/2020&time=12:30&description=uqweogg123ed_oqweut&user_id=2&app_id=1&token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.ofQ81GPMNtuljSEFcWvFEp6MwpfRTCiZPzkIhXiNx68

async def handle(request):
    await asyncio.sleep(random.randint(0, 1))

    try:
        token = request.rel_url.query['token']
        if token_verify(token) == "True":
            user_id = request.rel_url.query['user_id']
            app_id = request.rel_url.query['app_id']
            date = request.rel_url.query['date']
            time_data = request.rel_url.query['time']
            description = request.rel_url.query['description']
            await saveData(description, date, time_data, app_id, user_id)
            print( date, time_data, app, description)
            result = "DATA RECIEVED"
        else:
            result = "INVALID TOKEN"

    except Exception as error:
        print(error) 
        result = "INVALID TOKEN"

    
    
    return web.Response(text=result)

async def init(port):
    app = web.Application()
    app.router.add_route('GET', '/add', handle)
    app.router.add_route('GET', '/login', login)
    print("Started at", port)
    return await loop.create_server(
        app.make_handler(), '127.0.0.1', port)
    
        

loop = asyncio.get_event_loop()
# loop.run_until_complete(asyncio.gather(init()))
# loop.run_forever()
