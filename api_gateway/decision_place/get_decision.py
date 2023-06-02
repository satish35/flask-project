import requests
from flask import make_response,jsonify

def accept(_id):
    try:
        json_data= {
            "_id": _id
        }
        res=requests.get(
            'http://127.0.0.1:8081/accept',
            json= json_data
        )
        data= res.json()
        return data
    except Exception as err:
        return make_response(jsonify({
            'status': 'error',
            'message': 'something went wrong'
        }))
    
def reject(_id):
    try:
        json_data= {
            "_id": _id
        }
        res=requests.get(
            'http://127.0.0.1:8081/reject',
            json= json_data
        )
        data= res.json()
        return data
    except Exception as err:
        return make_response(jsonify({
            'status': 'error',
            'message': 'something went wrong'
        }))
    
def done(_id):
    try:
        json_data= {
            "_id": _id
        }
        res= requests.get(
            'http://127.0.0.1:8081/done',
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