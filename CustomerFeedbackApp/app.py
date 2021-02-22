from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail


app=Flask(__name__,template_folder='template')

ENV='prod'

if ENV=='dev':
    app.debug=True
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Oraclejob1@localhost/cars'
else:
    app.debug=False
    app.config['SQLALCHEMY_DATABASE_URI']='postgres://dcrceoiwvmawrm:795d403c27341018a19b7ebddb0bb64a23feaacc1a2e80ab79261b2768f1ef84@ec2-54-164-241-193.compute-1.amazonaws.com:5432/dff6qhb7uc9fkh'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200))
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments):
        self.customer=customer
        self.dealer=dealer
        self.rating=rating
        self.comments=comments


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])  
def submit():
    if request.method=='POST' :
        customer=request.form['customer']
        dealer=request.form['dealer']
        rating=request.form['rating']
        comments=request.form['comments']
        #print(customer,dealer,rating,comments)
        if customer=='' or dealer=='':
            return render_template('index.html', message='Please enter the required fields')
        if db.session.query(Feedback).filter(Feedback.customer==customer).count()==0:
            data=Feedback(customer, dealer,rating,comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer, dealer, rating, comments)
            return render_template('success.html')
        return render_template('index.html', message='You had already submitted the feedback')

if __name__=='__main__':
    app.run()