import pyrebase
import json
from flask import Flask, request, jsonify

firebaseConfig = {
    'apiKey': "AIzaSyDAVMSj1_w5nQ0G1MbWEA-wlPWqJYp2kuY",
    'authDomain': "pythoncrud-8f1a9.firebaseapp.com",
    'databaseURL': "https://pythoncrud-8f1a9-default-rtdb.firebaseio.com",
    'projectId': "pythoncrud-8f1a9",
    'storageBucket': "pythoncrud-8f1a9.appspot.com",
    'messagingSenderId': "701216471755",
    'appId': "1:701216471755:web:df88f2adb7fcdb7bedf94e",
    'measurementId': "G-TY20KWTJQT"
}
firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()

app = Flask(__name__)

@app.route("/")
def home():
    return "<p>This is a crud api for firebase realtime database!</p>"

@app.route('/create', methods=['POST'])

def create():
    username = request.form.get('username')
    userage = request.form.get('userage')
    userid = request.form.get('userid')

    unique_Key = db.generate_key()
    data = {
        'username': username,
        'userage': userage,
        'userid': userid,
        'key': unique_Key,
    }
    db.child('users').child(unique_Key).set(data)

    return jsonify({'status': str('Data add successfully!')})




@app.route('/read', methods=['POST'])
def read():
    username = request.form.get('username')

    users = db.child('users').get()
    for user in users.each():
        if user.val()['username'] == username:
            x = db.child('users').child(user.key()).get().val()
            return jsonify(x)
        return jsonify({'status': str('There is no such name in the database!')})


@app.route('/update', methods=['POST'])
def update():
    username = request.form.get('username')
    update_username = request.form.get('update_username')
    users = db.child('users').get()
    for user in users.each():
        if user.val()['username'] == username:
            db.child('users').child(user.key()).update({'username': update_username})
            return jsonify({'status': str('username updated successfully! ')})
        else:
            return jsonify({'status': str('There is no such name in the database!')})




@app.route('/delete',methods=['POST'])
def delete():
    username = request.form.get('username')

    users = db.child('users').get()
    for user in users.each():
        if user.val()['username'] == username:
            x = db.child('users').child(user.key()).remove()
            return jsonify({'status': str('Successfully deleted!')})
        return jsonify({'status': str('There is no such name in the database!')})



if __name__ == '__main__':
    app.run(debug=True)
