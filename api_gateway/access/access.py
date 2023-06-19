import requests,json
from werkzeug.datastructures import ImmutableMultiDict

def access(request):
    auth=request.form.to_dict(flat=True)
    #for key, value in auth:
       # print(key,value)
    #if auth['user'] is '' or auth['password'] is '':
    #    return 'none', ('missing credintials', 401)
    print(type(auth))
    res= requests.post(
        'http://127.0.0.1:5000/login',
        json= auth
    )
    data=json.loads(res.content)
    return data


def accessj(request):
    auth=request.form.to_dict(flat=True)
    #for key, value in auth:
       # print(key,value)
    #if auth['user'] is '' or auth['password'] is '':
    #    return 'none', ('missing credintials', 401)
    print(type(auth))
    res= requests.post(
        'http://127.0.0.1:5000/jlogin',
        json= auth
    )
    print(res.content)
    data=json.loads(res.content)
    return data