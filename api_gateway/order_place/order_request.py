import requests
from flask import make_response, jsonify

def order_request(_sid, _uid):
    try:
        if _sid == None:
            raise ValueError
        json_data={
            '_sid': _sid,
            '_uid': _uid
        }
        resp=requests.get(
            'http://127.0.0.1:8081/placerequest',
            json= json_data
        )
        data=resp.json()
        print(data)
        return data
    except Exception as err:
        return make_response(jsonify({
            'status': 'error',
            'message': 'something went wrong'
        }))
