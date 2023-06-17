import requests, json
from werkzeug.datastructures import ImmutableMultiDict

def registeru(request):
    auth=request.form.to_dict(flat=True)
    json_data={
        'first_name': auth['first_name'],
        'last_name': auth['last_name'],
        'email': auth['email'],
        'contact_no': auth['contact_no'],
        'password': auth['password']
    }
    res= requests.post(
        'http://127.0.0.1:5000/register',
        json= json_data
    )
    data=res.json()
    return data

def registerj(request):
    auth=request.form.to_dict(flat=True)
    json_data={
        'first_name': auth['first_name'],
        'last_name': auth['last_name'],
        'email': auth['email'],
        'contact_no': auth['contact_no'],
        'password': auth['password']
    }
    res= requests.post(
        'http://127.0.0.1:5000/jregister',
        json= json_data
    )
    data= res.json()
    return data