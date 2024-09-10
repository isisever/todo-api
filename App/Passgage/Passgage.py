from dotenv import load_dotenv
import os
from PassgageAPI import PassgageAPI
from ..environment import *

load_dotenv()

def base_url ():
    return os.getenv('USER_ENDPOINT')

def user(data):
    passgage = PassgageAPI(api_url)
    passgage.headers = {'Authorization': 'Bearer ' + PassgageToken}
    return passgage.post(base_url(), headers=passgage.headers, data=data)