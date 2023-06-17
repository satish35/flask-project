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
app=Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'
app.config["MONGO_URI"] = "mongodb://localhost:27017/file"
mongo=PyMongo(app)


allowed_extensions= { 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


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
    if request.method=='POST':
        data=request.form.to_dict(flat=True)
        print(data)
        if data['status'] == 'accepted':
            res=get_decision.accept(data['button'])
            return res
        else:
            res= get_decision.reject(data['button'])
            return res
    else:
        res=get_order_check.order_request_checkr('satish')
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
    if request.method=='POST':
        data= request.form
        res=get_decision.done(data['button'])
        return res
    else:
        res=get_order_check.accepted_orderr('satish')
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
    if request.method=='POST':
        try:
            detail=request.form
            loc='{}%2C+{}%2C+{}%2C+{}'.format(detail['shop_address'],detail['city'],detail['state'],detail['pincode'])
            locd='{}, {}, {}, {}'.format(detail['shop_address'],detail['city'],detail['state'],detail['pincode'])
            print(loc)
            token= 'eyJhbGciOiJSUzUxMiIsImN0eSI6IkpXVCIsImlzcyI6IkhFUkUiLCJhaWQiOiJjQXltUHh6RlhuWWhUZmIybzNtOSIsImlhdCI6MTY4Mjc2NTEwNywiZXhwIjoxNjgyODUxNTA3LCJraWQiOiJqMSJ9.ZXlKaGJHY2lPaUprYVhJaUxDSmxibU1pT2lKQk1qVTJRMEpETFVoVE5URXlJbjAuLncwZDVTOG5GNEJfWUdMVjdvQVBRdncuaGlwLVV2MThzSnRxSzJrWDdidVlDZ1lFRi12QktjX3VINlVVT0NIUElyOGIwRUhaYlltano4bWhHRnUtM1pCck9fdTAwTFpudzhkcEg0TWNWRjFoZ1ltNmRMNkk2eUhXTkludHlRazRKdEFVbGFNT0pJVDN1RGJIcHZmLWxoSDRZY09sU1FhSzNHcThsdUhweFJnOFA5bFIxZDBsOElEM0xtMUlCdnl3Y0trLnJKY1VuUzFZeGZ3dWgzdUI1dm15TUkwbEppS0N3ZlhhNXRzRmhVWUJGMTg.rLxGk6YTF6X0aNBcpv31j9l9ZQlnQUDHNWoOzxCyhQ96IjS7chYPGWV8qYR19JXvmaCqugl3sra9Tl_Y0ADkfnqHhcRbQD5qlDd_8nYuSxtl3B_2ZD3P3BGGn9fCC7H1fFKrFJBrSbXqIUHL5fYmEUQTDkhQzzDVdmczIqH0h0mrbjB9EUdzvgTo4Hi_RTxjmQmoS2JDaDiKJJWO4Tpo-VcIDCyM0YjUAD0RiJ2hGBe22NY4idYdwX86MVCaU_U-OSm484PKQiPYT0RkUyLuHzUbT3hU8u1ew0gwVwn2pXeQvbZ0GPZ0O8jr_VfAI6IpDEXQ-hagdyFqlUUPn8b9cA'
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
            return make_response({
                'status': 'error',
                'message': err
            },200)
    else:
        return render_template('store.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
