from flask import *
import pyrebase
config = {
    'apiKey': "AIzaSyC7qkqByquC4feBmUbAI2Rf8y1S8l9G8Kc",
    'authDomain': "yoga-c1d98.firebaseapp.com",
    'databaseURL': "https://yoga-c1d98.firebaseio.com",
    'projectId': "yoga-c1d98",
    'storageBucket': "yoga-c1d98.appspot.com",
    'messagingSenderId': "965993472725",
    'appId': "1:965993472725:web:a108a3ac2cae4d7bbf785c",
    'measurementId': "G-003XRYSC8N"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
User = {
    'first_name':'',
    'last_name':'',
    'age':'',
    'email':'',
    'password':'',
    'classes':[],
    'contact_no':'',
    'tokens':0
}
# class User(object):
#     def __init__(self,first_name,last_name,age,email,password,contact_no):
#         self.first_name = first_name
#         self.last_name = last_name
#         self.age = age
#         self.email = email
#         self.password = password
#         self.contact_no = contact_no
#         self.tokens = 0
    
#     def id_of_user(self):
#         return self.email
    
#     def no_of_tokens(self):
#         return self.tokens





app = Flask(__name__)
app.secret_key='yogaclasses'
@app.route('/')
def hello():
    return render_template('home.html')

@app.route('/sign_in',methods=['GET','POST'])
def sign_in():
    unsuccessful = 'Please check your credentials'
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            user = auth.sign_in_with_email_and_password(email,password)
            session['localId']=user['localId']
            user = list(db.child('Users').child(user['localId']).get().val().values())[0]
            #print(db.child(user['localId']).get().val().values())
            # user = db.get(email[:-4]).val().values()
            # print(user)
            return render_template('user.html',user = user)
        except Exception as e:
            raise e
            return render_template('/sign_in.html',us=unsuccessful)
    return render_template('sign_in.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        User['first_name'] = request.form['first_name']
        User['last_name'] = request.form['last_name']
        User['age'] = request.form['age']
        User['email'] = request.form['email']
        User['password'] = request.form['password']
        User['contact_no'] = request.form['contact_no']
        user = auth.create_user_with_email_and_password(User['email'],User['password'])
        db.child('Users').child(user['localId']).push(User)
        return render_template('home.html')
    return render_template('register.html')

@app.route('/upi',methods=['GET','POST'])
def upi():
    if "localId" in session:
        localId = session['localId']
        user = list(db.child('Users').child(localId).get().val().values())[0]
        return render_template('upi.html',user=user)
    else:
        render_template('home.html')
@app.route('/logout')
def logout():
    session.pop('localId',None)
    return render_template('home.html')

@app.route('/user')
def user():
    if request.method=='POST':
        if request.form['add 10']:
            print(10)
        elif request.form['add 20']:
            print(20)
        elif request.form['add 100']:
            print(100)
    localId = session['localId']
    user = list(db.child('Users').child(localId).get().val().values())[0]
    
    return render_template('user.html',user=user)
    

if __name__=='__main__':
    app.run(debug=True)