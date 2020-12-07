import jwt as jwt_init
import sys

SECRET_KET = 'superadmin'
algorithm = 'HS256'

def token_encode(username, app_id):
    payload_encode = jwt_init.encode({'username' : username, 'app_id' : app_id}, SECRET_KET, algorithm=algorithm)
    token = payload_encode.decode('UTF')
    return token


def token_verify(token):
        try:
            payload_decode = jwt_init.decode(token, SECRET_KET, algorithm=algorithm)
            #print(payload_decode)
            return payload_decode 
        except:
            return "Token Invalid"

        

