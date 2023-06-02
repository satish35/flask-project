import requests
from flask import make_response,jsonify

def user(username):
    try:
        json_data={
            'user': username
        }
        res=requests.get(
            'http://127.0.0.1:8081',
            json= json_data
        )
        result=res.json()
        print(result)
        return result
    except Exception as err:
        print(err)