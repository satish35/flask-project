from flask import Flask,request,render_template,redirect,flash,make_response,jsonify,url_for,abort
from register import register
from validate import validate
from access import access
from store_access import get_store
from user_access import get_user
from order_place import order_request
from order_check import get_order_check
from decision_place import get_decision
from flask_pymongo import PyMongo
from werkzeug.datastructures import ImmutableMultiDict
import requests
import config
app=Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'
app.config["MONGO_URI"] = "mongodb://localhost:27017/file"
mongo=PyMongo(app)


allowed_extensions= { 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/gold')
def gold():
    URL= "https://api.metalpriceapi.com/v1/latest"
    PARAMS = {'api_key': config.API_KEY,
              'base': config.BASE,
              'currencies': config.CURRENCIES}
    res=requests.get(
        url= URL,
        params= PARAMS
    )
    data=res.json()
    print(data)
    value=data['rates']['XAU']
    rate=1/value
    updated_rate=float(rate/28.3495)
    print(updated_rate)
    print('hi')
    return jsonify({
        'gold_rate': updated_rate
    })

@app.route('/')
def home():
    return render_template('/index.html')

@app.route('/user')
def user():
    return render_template('/user.html')

@app.route('/userlogin', methods=['POST', 'GET'])
def ulogin():
    if request.method=='POST':
        res=access.access(request)
        if res['status']=='error':
            abort(401)
        else:
            resp=make_response(redirect(url_for('upload')))
            resp.set_cookie('token', res['token'])
            return resp
    else:
        return render_template('/login.html')
    
@app.route('/retailerlogin', methods=['POST', 'GET'])
def jlogin():
    if request.method=='POST':
        res=access.accessj(request)
        if res['status']=='error':
            abort(401)
        else:
            resp=make_response(redirect(url_for('supload')))
            resp.set_cookie('token', res['token'])
            return resp
    else:
        return render_template('/jlogin.html')
    
@app.route('/userlogout', methods=['GET', 'POST'])
def ulogout():
    res=validate.validate(request.cookies.get('token'))
    if res['status']=='error':
        return redirect(url_for('ulogin'))
    else:
        if request.method=='POST':
            pass
        else:
            resp=redirect(url_for('ulogin'))
            resp.delete_cookie('token')
            return resp
        
@app.route('/retailerlogout', methods=['GET', 'POST'])
def jlogout():
    res=validate.jvalidate(request.cookies.get('token'))
    if res['status']=='error':
        return redirect(url_for('jlogin'))
    else:
        if request.method=='POST':
            pass
        else:
            resp=redirect(url_for('jlogin'))
            resp.delete_cookie('token')
            return resp

@app.route('/register', methods=['POST', 'GET'])
def uregister():
    if request.method=='POST':
        res= register.registeru(request)
        if res['status']=='success':
            return redirect(url_for('ulogin'))
        else:
            abort(406)
    else:
        return render_template('/index.html')
    
@app.route('/jregister', methods=['POST', 'GET'])
def jregister():
    if request.method=='POST':
        res= register.registerj(request)
        if res['status']=='success':
            return redirect(url_for('jlogin'))
        else:
            abort(406)
    else:
        return render_template('/jregister.html')


@app.route('/store', methods=['POST', 'GET'])
def store():
    res=validate.validate(request.cookies.get('token'))
    if res['status']=='error':
        return redirect(url_for('ulogin'))
    else:
        if request.method=='POST':
            res=get_store.get_store(request)
            return render_template('/search.html', data=res['data'])
        else:
            return render_template('/search.html')

@app.route('/upload', methods=['POST','GET'])
def upload():
    res=validate.validate(request.cookies.get('token'))
    if res['status']=='error':
        return redirect(url_for('ulogin'))
    else:
        if request.method=='POST':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                name=mongo.save_file(file.filename,file)
                mongo.db.user.insert_one({
                    'email': res['message'],
                    'description': request.form['description'],
                    'photo': name
                })
                flash('file successfully added')
                return redirect(request.url)
        else:
            return render_template('upload.html')
    
@app.route('/placeorder', methods=['POST','GET'])
def place():
    res=validate.validate(request.cookies.get('token'))
    if res['status']=='error':
        return redirect(url_for('ulogin'))
    else:
        if request.method=='POST':
            data=request.form.to_dict(flat=True)
            _uid= data['button']
            print(_uid)
            res= order_request.order_request(request.cookies.get('id'), _uid)
            return res
        else:
            res= get_user.user(res['message'])
            return render_template('placeorder.html', data=res['data'])
    
    
@app.route('/order', methods=['POST', 'GET'])
def order():
    res=validate.validate(request.cookies.get('token'))
    if res['status']=='error':
        return redirect(url_for('ulogin'))
    else:
        if request.method=='POST':
            id=request.form['button']
            print(id)
            resp= jsonify(dict(redirect='placeorder'))
            resp.set_cookie('id', id)
            return resp
        else:
            pass
    

@app.route('/rorderrequest', methods=['POST', 'GET'])
def rorderrequest():
    res=validate.jvalidate(request.cookies.get('token'))
    if res['status']=='error':
        return redirect(url_for('jlogin'))
    else:
        if request.method=='POST':
            data=request.form.to_dict(flat=True)
            print(data)
            if data['status'] == 'accepted':
                res=get_decision.accept(data['button'])
                resp= jsonify(dict(redirect='rorderrequest'))
                return resp
            else:
                res= get_decision.reject(data['button'])
                resp= jsonify(dict(redirect='rorderrequest'))
                return resp
        else:
            res=get_order_check.order_request_checkr(res['user'])
            return render_template('rorderrequest.html', data=res['data'])
    
@app.route('/uorderrequest', methods=['POST', 'GET'])
def uorderrequest():
    res=validate.validate(request.cookies.get('token'))
    if res['status']=='error':
        return redirect(url_for('ulogin'))
    else:
        if request.method=='POST':
            pass
        else:
            res=get_order_check.order_request_checku(res['message'])
            print(res)
            return render_template('uorderrequest.html', data=res['data'])
    
@app.route('/raccepted_order', methods=['POST', 'GET'])
def raccepted_order():
    res=validate.jvalidate(request.cookies.get('token'))
    if res['status']=='error':
        return redirect(url_for('jlogin'))
    else:
        if request.method=='POST':
            data= request.form
            res=get_decision.done(data['button'])
            resp= jsonify(dict(redirect="raccepted_order"))
            return resp
        else:
            res=get_order_check.accepted_orderr(res['user'])
            return render_template('raccepted_order.html', data=res['data'])
    
@app.route('/uaccepted_order', methods=['POST', 'GET'])
def uaccepted_order():
    res=validate.validate(request.cookies.get('token'))
    if res['status']=='error':
        return redirect(url_for('ulogin'))
    else:
        if request.method=='POST':
            pass
        else:
            res=get_order_check.accepted_orderu(res['message'])
            return render_template('uaccepted_order.html', data=res['data'])
    
@app.route('/supload',methods=['POST','GET'])
def supload():
    res=validate.jvalidate(request.cookies.get('token'))
    if res['status']=='error':
        return redirect(url_for('jlogin'))
    else:
        if request.method=='POST':
            try:
                detail=request.form
                loc='{}%2C+{}%2C+{}%2C+{}'.format(detail['shop_address'],detail['city'],detail['state'],detail['pincode'])
                locd='{}, {}, {}, {}'.format(detail['shop_address'],detail['city'],detail['state'],detail['pincode'])
                print(loc)
                token= 'eyJhbGciOiJSUzUxMiIsImN0eSI6IkpXVCIsImlzcyI6IkhFUkUiLCJhaWQiOiJjQXltUHh6RlhuWWhUZmIybzNtOSIsImlhdCI6MTY4NzAyMDA1OCwiZXhwIjoxNjg3MTA2NDU4LCJraWQiOiJqMSJ9.ZXlKaGJHY2lPaUprYVhJaUxDSmxibU1pT2lKQk1qVTJRMEpETFVoVE5URXlJbjAuLko3dlRqdXUxTDFYSnZIWnpKSk05U1EubGNGUzFfTk5idFpUdjRvSHJDVFNWbkc0VXI3UlRTSlUzVFFxc2hKS0ZoMHlFc0Zaa3FBTHJ0MUdOT0NzMlJTNkkzRkZVRmpGQUI3ZUZpOV9fNUg1Q3dfb3c4VW44Yy1JM2VRbWs5a29YeFZfS1BGeEdtR3JyZVlGbmxEdzI5enAwUUVQSHVJMXl1UnJrT0locjBuTHdqNzBwVFVpMk85ZkU5ZjB4b2lTb3pBLklXaDJYS0JRVFluQkdMRUxfVDd2SXdnOVdkbnR0OU8ySThJejRTOGRfVFk.EgJZqj8zW848w5Rf_ifNk_0ioEKzS6L_kyfpuElwIzSkIHa0MuODpi04F6cKa5hUC3WvmZY5OlGP-B-F1GBTz9kLRQ6apXxssCGwNA3_1qWQkjAiRHioqRLW5aQlEzNZa_9GUyzEYn2bigJacgjnMUORF7sbMg2fblEhn-2ajBHu_bGTjr8o3C_B1OrHK46D0uU1Ati6o9KWRUl5aVQGn4WNVybPPIVYg6zHBdsyizbCrjyFa-8ypjzV5KNJUlS9q1RJSX0eJhd1oWcLDVN_f5i-gDcDKtLpAiIG3iScVwxuV1lncMtA6R5Wh6mKIgmZy-9qO6dTy8OmXCFOtPc6Bg'
                data={
                    'Authorization': 'Bearer {}'.format(token)
                }
                print('hi')
                res=requests.get(
                    'https://geocode.search.hereapi.com/v1/geocode?q={}&limit=4&apiKey=NMY0mPbDOc_0CZ2JOyQhVeqlX9X6782u8mWozBryvnQ'.format(loc),
                    headers= data
                )
                res.raise_for_status()
                json=res.json()
                latlon=json['items'][0]['position']
                print(latlon)
                mongo.db.store.insert_one({
                    'loc': locd,
                    'owned_by': request.form['owned_by'],
                    'email': res['user'],
                    'making_charges': request.form['making_charges'],
                    'lat': latlon['lat'],
                    'long': latlon['lng']
                })
                return make_response({
                    'status': 'success',
                    'message': 'successfully added'
                },200)
            except Exception as err:
                print(err)
                message=str(err)
                return make_response({
                    'status': 'error',
                    'message': message
                },200)
        else:
            return render_template('store.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
