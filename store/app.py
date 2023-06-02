from flask import Flask,request,make_response,jsonify
from flask_pymongo import PyMongo
app=Flask(__name__)
app.config['MONGO_URI']= "mongodb://localhost:27017/file"
mongo=PyMongo(app)

@app.route('/search')
def search():
    try:
        result=[]
        data=request.get_json()
        print(data)
        range=data['range']
        filter=data['filter']
        res=mongo.db.store.find(
            { "$and" : [{ "lat" : { "$lte" : data['lat']+range}},{ "long" : { "$lte" : data['long']+range}}] }
        ).sort('making_charges',filter)
        for doc in res:
            print(doc)
            _id= str(doc['_id'])
            doc['_nid']=str(doc['_id'])
            print(doc['_nid'])
            doc.pop('_id')
            doc.pop('lat')
            doc.pop('long')
            result.append(doc)
        return make_response(jsonify({
            'data': result
        }),200)
    except Exception as err:
        print(err)
        return make_response(jsonify({
            'status': 'error',
            'message': err
        }))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)