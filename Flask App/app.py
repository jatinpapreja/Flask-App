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
# available_sessions =list(db.child('Sessions').get().val().values())
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

new_session = {
    'date':'',
    'start_time':'',
    'end_time':'',
    'details':'',
    'users_joined':[],
    'cost':0
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
            if email=='kartikay@gmail.com':
                available_sessions =list(db.child('Sessions').get().val().values())
                return render_template('masteruser.html',available_sessions = available_sessions)
            else:
                # user = list(db.child('Users').child(user['localId']).get().val().values())[0]
                # return render_template('user.html',user = user)
                return redirect(url_for('user'))
        except:
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
        if User['email']=='kartikay@gmail.com':
            db.child('MasterUsers').child(user['localId']).push(User)
        else:
            db.child('Users').child(user['localId']).push(User)
        return render_template('home.html')
    return render_template('register.html')

@app.route('/create_session',methods=['GET','POST'])
def create_session():
    if request.method == 'POST':
        new_session['date'] = request.form['date']
        new_session['start_time'] = request.form['start_time']
        new_session['end_time'] = request.form['end_time']
        new_session['details'] = request.form['details']
        new_session['cost'] = request.form['cost']
        db.child('Sessions').push(new_session)
        return redirect(url_for('masteruser'))
    return render_template('create_session.html')

@app.route('/masteruser',methods=['GET','POST'])
def masteruser():
    available_sessions =list(db.child('Sessions').get().val().values())
    return render_template('masteruser.html',available_sessions=available_sessions)

@app.route('/masteruser/delete/<int:id>')
def masterdelete(id):
    available_id =list(db.child('Sessions').get().val().keys())
    delete_id = available_id[id]
    data = db.child('Sessions').child(delete_id).get().val()
    if 'users_joined' in data:
        for elem in data['users_joined']:
            user = list(db.child('Users').child(elem['localId']).get().val().values())[0]
            user['tokens']+=int(elem['cost'])
            user['classes'].remove(delete_id)
            db.child('Users').child(elem['localId']).remove()
            db.child('Users').child(elem['localId']).push(user)

    db.child('Sessions').child(delete_id).remove()
    return redirect(url_for('masteruser'))

@app.route('/masteruser/edit/<int:id>',methods=['GET','POST'])
def masteredit(id):
    
    data = list(db.child('Sessions').get().val().values())[id]
    if request.method == 'POST':
        available_id =list(db.child('Sessions').get().val().keys())
        edit_id = available_id[id]
        new_session['date'] = request.form['date']
        new_session['start_time'] = request.form['start_time']
        new_session['end_time'] = request.form['end_time']
        new_session['details'] = request.form['details']
        new_session['cost'] = request.form['cost']
        if 'users_joined' in data:
            new_session['users_joined']=data['users_joined']
        db.child('Sessions').child(edit_id).update(new_session)
        return redirect(url_for('masteruser'))
    return render_template('masteredit.html',id=id,data=data)





@app.route('/upi',methods=['GET','POST'])
def upi():
    if "localId" in session:
        return render_template('upi.html')
    else:
        return render_template('home.html')

@app.route('/book_session')
def book_session():
    if "localId" in session:
        available_sessions =list(db.child('Sessions').get().val().values())
        return render_template('book_session.html',available_sessions=available_sessions)
    else:
        return render_template('home.html')

@app.route('/buy/<int:id>')
def buy(id):
    localId = session['localId']
    user = list(db.child('Users').child(localId).get().val().values())[0]
    available_id =list(db.child('Sessions').get().val().keys())
    edit_id = available_id[id]
    data = list(db.child('Sessions').get().val().values())[id]
    if user['tokens']>=int(data['cost']):
        user['tokens']-=int(data['cost'])
        if 'classes' in user:
            user['classes'].append(edit_id)
        else:
            user['classes']=[edit_id]
        
        db.child('Users').child(localId).remove()
        db.child('Users').child(localId).push(user)


        join = {}
        join['first_name']=user['first_name']
        join['last_name']=user['last_name']
        join['email']=user['email']
        join['cost']=data['cost']
        join['localId'] = localId

        if 'users_joined' in data:
            data['users_joined'].append(join)
        else:
            data['users_joined']=[join]
        
        db.child('Sessions').child(edit_id).update(data)

        return redirect(url_for('user'))


    else:
        unsuccessful='You do not have enough tokens to buy this session.'
        return redirect(url_for('book_session',uns=unsuccessful))

    





@app.route('/logout')
def logout():
    session.pop('localId',None)
    return render_template('home.html')

@app.route('/user',methods=['GET','POST'])
def user():
    # if request.method=='POST':
    #     if request.form['add 10']:
    #         print(10)
    #     elif request.form['add 20']:
    #         print(20)
    #     elif request.form['add 100']:
    #         print(100)
    localId = session['localId']
    user = list(db.child('Users').child(localId).get().val().values())[0]
    classes = []
    if 'classes' in user:
        for elem in user['classes']:
            data = db.child('Sessions').child(elem).get().val() 
            d = {}
            d['date']=data['date']
            d['start_time']=data['start_time']
            d['end_time']=data['end_time']
            d['cost']=data['cost']
            d['details']=data['details']
            classes.append(d)  

    return render_template('user.html',user=user,classes=classes)

@app.route('/user/delete/<int:id>')
def userdelete(id):
    localId = session['localId']
    user = list(db.child('Users').child(localId).get().val().values())[0]
    delete_id = user['classes'][id]
    user['classes'].pop(id)
    data = db.child('Sessions').child(delete_id).get().val()
    
    for elem in data['users_joined']:
        if elem['first_name']==user['first_name'] and elem['last_name']==user['last_name'] and elem['email']==user['email']:
            user['tokens']+=int(elem['cost'])
            data['users_joined'].remove(elem)
            break

    db.child('Sessions').child(delete_id).update(data)
    db.child('Users').child(localId).remove()
    db.child('Users').child(localId).push(user)
    return redirect(url_for('user')) 




@app.route('/add10')
def add10():
    localId = session['localId']
    user = list(db.child('Users').child(localId).get().val().values())[0]
    user['tokens']+=10
    db.child('Users').child(localId).remove()
    db.child('Users').child(localId).push(user)
    # user = list(db.child('Users').child(localId).get().val().values())[0]   
    # return render_template('user.html',user=user)
    return redirect(url_for('user'))

@app.route('/add20')
def add20():
    localId = session['localId']
    user = list(db.child('Users').child(localId).get().val().values())[0]
    user['tokens']+=20
    db.child('Users').child(localId).remove()
    db.child('Users').child(localId).push(user)
    # user = list(db.child('Users').child(localId).get().val().values())[0]
    # return render_template('user.html',user=user)
    return redirect(url_for('user'))


@app.route('/add100')
def add100():
    localId = session['localId']
    user = list(db.child('Users').child(localId).get().val().values())[0]
    user['tokens']+=100
    db.child('Users').child(localId).remove()
    db.child('Users').child(localId).push(user)
    # user = list(db.child('Users').child(localId).get().val().values())[0]
    # return render_template('user.html',user=user)
    return redirect(url_for('user'))

    

    

if __name__=='__main__':
    app.run(debug=True)