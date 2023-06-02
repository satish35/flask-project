import requests, json
from werkzeug.datastructures import ImmutableMultiDict

def registeru(request):
    auth=request.form
    first_name=auth['first_name']
    last_name=auth['last_name']
    email=auth['email']
    contact_no=auth['contact_no']
    password=auth['password']

    data=auth.to_dict(flat=True)

    print(data)
    print(type(data))
    json_data=json.dumps(data)
    print(type(json_data))
    res= requests.post(
        'http://127.0.0.1:5000/register',
        json= data
    )
    return res.content

def registerj(request):
    auth=request.form
    first_name=auth['first_name']
    last_name=auth['last_name']
    email=auth['email']
    contact_no=auth['contact_no']
    password=auth['password']

    data=auth.to_dict(flat=True)

    print(data)
    print(type(data))
    json_data=json.dumps(data)
    print(type(json_data))
    res= requests.post(
        'http://127.0.0.1:5000/jregister',
        json= data
    )
    return res.content