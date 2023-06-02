import requests
import geocoder
from flask import make_response,jsonify
from werkzeug.datastructures import ImmutableMultiDict

def get_store(request):
    try:
        data=request.form.to_dict(flat=True)
        if data.get('range') == '':
            range=float(0.33333)
        else:
            range=float(data['range'])
        if data.get('price_fiter') == 'High':
            fil=-1
        else:
            fil=1
        g=geocoder.ip('me')
        print(g.latlng)
        json_data={
            'range': range,
            'lat': g.latlng[0],
            'long': g.latlng[1],
            'filter': fil
        }
        res=requests.get(
            'http://127.0.0.1:8080/search',
            json= json_data
        )
        data=res.json()
        print(data)
        return data
    except Exception as err:
        print(err)
        return make_response(jsonify({
            'status': 'error',
            'message': 'something went wrong'
        }),400)