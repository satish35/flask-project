import requests
from flask import make_response, jsonify

def order_request_checku(username):
    try:
        json_data={
            'email': username
        }
        res=requests.get(
            'http://127.0.0.1:8081/uorder_check',
            json= json_data
        )
        data=res.json()
        print(data)
        return data
    except Exception as err:
        return make_response(jsonify({
            'status': 'error',
            'message': 'something went wrong'
        }))
    
def order_request_checkr(username):
    try:
        json_data={
            'user': username
        }
        res=requests.get(
            'http://127.0.0.1:8081/rorder_check',
            json= json_data
        )
        data=res.json()
        print(data)
        return data
    except Exception as err:
        return make_response(jsonify({
            'status': 'error',
            'message': 'something went wrong'
        }))
    
def accepted_orderu(username):
    try:
        json_data={
            'email': username
        }
        res=requests.get(
            'http://127.0.0.1:8081/uaccepted_order',
            json= json_data
        )
        data=res.json()
        print(data)
        return data
    except Exception as err:
        return make_response(jsonify({
            'status': 'error',
            'message': 'something went wrong'
        }))
    
def accepted_orderr(username):
    try:
        json_data={
            'user': username
        }
        res=requests.get(
            'http://127.0.0.1:8081/raccepted_order',
            json= json_data
        )
        data=res.json()
        print(data)
        return data
    except Exception as err:
        return make_response(jsonify({
            'status': 'error',
            'message': 'something went wrong'
        }))
    
