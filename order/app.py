from flask import Flask,request,make_response,jsonify
from flask_pymongo import PyMongo, ObjectId
app=Flask(__name__)
app.config['MONGO_URI']= "mongodb://localhost:27017/file"
mongo=PyMongo(app)

@app.route('/')
def home():
    result=[]
    res=mongo.db.user.find(
        {'email': 'udaiyar.satish03@gmail.com'}
    )
    for data in res:
        data['_nid']=str(data['_id'])
        data.pop('_id')
        data.pop('photo')
        result.append(data)
    return make_response(jsonify({
        'data': result
    }),200)

@app.route('/placerequest')
def add_order_request():
    try:
        data=request.get_json()
        store_id=data['_sid']
        print(store_id)
        user_id=data['_uid']
        print(user_id)
        res1=mongo.db.user.find({
            "_id": ObjectId(user_id)
        })
        for data1 in res1:
            data1.pop('_id')
            data1.pop('photo')
        print(data1)
        res2=mongo.db.store.find({
            "_id": ObjectId(store_id)
        })
        for data2 in res2:
            data2.pop('_id')
        print(data2)
        fres=mongo.db.order.insert_one({
            'email': data1['email'],
            'description': data1['description'],
            'loc': data2['loc'],
            'owned_by': data2['owned_by'],
            'making_charges': data2['making_charges'],
            'status': 'pending',
            'lat': data2['lat'],
            'long': data2['long']
        })
        return make_response(jsonify({
            'status': 'success',
            'message': 'order request successfully placed'
        }),200)
    except Exception as err:
        message=str(err)
        print(err)
        return make_response(jsonify({
            'status': 'error',
            'message': err
        }))
    
@app.route('/uorder_check')
def uorder_check():
    try:
        result=[]
        data= request.get_json()
        email= data['email']
        res=mongo.db.order.find({
            '$and': [{'status': 'pending'}, {'email': email}]
        })
        for data in res:
            data['_nid']=str(data['_id'])
            data.pop('_id')
            result.append(data)
        return make_response(jsonify({
            'data': result
        }),200)
    except Exception as err:
        return make_response(jsonify({
            'status': 'error',
            'message': 'something went wrong in server side with error {}'.format(err)
        }))
    
@app.route('/rorder_check')
def rorder_check():
    try:
        result=[]
        data= request.get_json()
        username= data['user']
        res=mongo.db.order.find({
            '$and': [{'status': 'pending'}, {'owned_by': username}]
        })
        for data in res:
            data['_nid']=str(data['_id'])
            data.pop('_id')
            result.append(data)
        return make_response(jsonify({
            'data': result
        }),200)
    except Exception as err:
        return make_response(jsonify({
            'status': 'error',
            'message': 'something went wrong in server side with error {}'.format(err)
        }))
    
@app.route('/uaccepted_order')
def uaccepted_order():
    try:
        result=[]
        data=request.get_json()
        email=data['email']
        res=mongo.db.order.find({
            '$and': [{'status': 'accepted'}, {'email': email}]
        })
        for data in res:
            data['_nid']=str(data['_id'])
            data.pop('_id')
            result.append(data)
        return make_response(jsonify({
            'data': result
        }),200)
    except Exception as err:
        return make_response(jsonify({
            'status': 'error',
            'message': 'something went wrong in server side with error {}'.format(err)
        }))
    
@app.route('/raccepted_order')
def raccepted_order():
    try:
        result=[]
        data=request.get_json()
        username= data['user']
        res=mongo.db.order.find({
            '$and': [{'status': 'accepted'}, {'owned_by': username}]
        })
        for data in res:
            data['_nid']=str(data['_id'])
            data.pop('_id')
            result.append(data)
        return make_response(jsonify({
            'data': result
        }),200)
    except Exception as err:
        return make_response(jsonify({
            'status': 'error',
            'message': 'something went wrong in server side with error {}'.format(err)
        }))
    
@app.route('/accept')
def accept():
    try:
        data=request.get_json()
        _id= data['_id']
        query_find={"_id": ObjectId(_id)}
        query_update={ "$set": {
            "status": "accepted"
        }}
        print('hi')
        res=mongo.db.order.update_one(query_find, query_update)
        print(res)
        return make_response(jsonify({
            'status': 'success',
            'message': 'successfully accepted'
        }))
    except Exception as err:
        return make_response(jsonify({
            'status': 'error',
            'message': 'something went wrong'
        }))
    
@app.route('/reject')
def reject():
    try:
        data=request.get_json()
        _id= data['_id']
        query_find={"_id": ObjectId(_id)}
        res=mongo.db.order.delete_one(query_find)
        return make_response(jsonify({
            'status': 'success',
            'message': 'successfully rejected'
        }))
    except Exception as err:
        return make_response(jsonify({
            'status': 'error',
            'message': 'something went wrong'
        }))

@app.route('/done')
def done():
    try:
        data=request.get_json()
        _id= data['_id']
        query_find={"_id": ObjectId(_id)}
        query_update={ "$set": {
            "status": "done"
        }}
        res=mongo.db.order.update_one(query_find, query_update)
        return make_response(jsonify({
            'status': 'success',
            'message': 'successfully done'
        }))
    except Exception as err:
        return make_response(jsonify({
            'status': 'error',
            'message': 'something went wrong'
        }))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)