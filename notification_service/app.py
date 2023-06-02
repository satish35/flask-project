from flask import Flask,request,render_template,redirect,flash,make_response,jsonify
from flask_mail import Mail, Message

app= Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'udaiyar.satish03@gmail.com'
app.config['MAIL_PASSWORD'] = 'satish53'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail= Mail(app)

@app.route('/')
def home():
    return 'hi from notification service'

if __name__ == '__main__':
    app.run(debug=True)