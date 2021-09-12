from flask import Flask, render_template, request , session ,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import json
from datetime import datetime


with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD=  params['gmail-password']
    )

mail = Mail(app)

app.config['SQLALCHEMY_DATABASE_URI'] ="mysql+pymysql://root:@localhost/Travelix"
db = SQLAlchemy(app)


class Contacts(db.Model):
    '''
    sno, name email, message, subject
    '''
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    

@app.route("/" , methods = ['GET', 'POST'])
def home():
   
    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        entry = Contacts(name=name,email = email, message = message,subject = subject )
        db.session.add(entry)
        db.session.commit()

        mail.send_message('New message from Travelix: ' + name,
                          sender=email,
                          recipients = [params['gmail-user']],
                          body = subject  + "\n"+ message 
                          )

    return render_template('index.html',params=params)



@app.route("/about")
def about():
    return render_template('about.html')



@app.route("/contact", methods = ['GET', 'POST'])
def contact():
    if(request.method=='POST'):
        '''Add entry to the database'''
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        entry = Contacts(name=name,email = email, message = message,subject = subject )
        db.session.add(entry)
        db.session.commit()

        # mail.send_message('New message from blogapp' + name,
        #                   sender=email,
        #                   recipients = [params['gmail-user']],
        #                   body = message + "\n" + phone
        #                   )

    return render_template('contact.html',params=params)


@app.route("/blog")
def blog():
    return render_template('blog.html')



@app.route("/offers")
def offers():
    return render_template('offers.html')



app.run(debug=True) 