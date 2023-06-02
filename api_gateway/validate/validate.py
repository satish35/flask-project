import requests

def jvalidate(token):
    #if "Authorization" not in request.headers:
    #    return "no authorization in header"
    #token=request.headers.get("Authorization")
    #token=ls.getItem('token')
    print(token)

    data={'Authorization' : 'Bearer {}'.format(token)}
    res=requests.get(
        'http://127.0.0.1:5000/jvalidation',
        headers= data
    )
    print(res)
    return res.content   

def validate(token):
    #if "Authorization" not in request.headers:
    #    return "no authorization in header"
    #token=request.headers.get("Authorization")
    print(token)
    data={'Authorization' : 'Bearer {}'.format(token)}
    res=requests.get(
        'http://127.0.0.1:5000/validation',
        headers= data
    )
    print(res)
    return res.content 