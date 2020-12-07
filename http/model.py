from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from auth.token_auth import token_encode, token_verify
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:iam100%pureROOT@localhost:3306/csmdb'
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

###MODELS
class AppAdmin(db.Model):
    """Model for App Admin accounts."""
    __tablename__ = 'appadmin'

    id = db.Column(db.Integer,
                   primary_key=True)
    username = db.Column(db.String(200),
                         nullable=False,
                         unique=False)
    password = db.Column(db.String(200),
                         primary_key=False,
                         unique=False,
                         nullable=False)
    app_id = db.Column(db.Integer, db.ForeignKey('apps.id'), unique=False, nullable=True)
    
    def __init__(self, username, password, app_id):
        self.username = username
        self.password = password
        self.app_id = app_id

class User(db.Model):
    """Model for users."""
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True)
    username = db.Column(db.String(250),
                         nullable=False,
                         unique=False)
    notifications = db.relationship('Notifications', backref='users', lazy=True)
    def __init__(self, username):
        self.username = username

class App(db.Model):
    """Model for user apps."""
    __tablename__ = 'apps'

    id = db.Column(db.Integer,
                   primary_key=True)
    title = db.Column(db.String(100),
                         nullable=False,
                         unique=False)
    notifications = db.relationship('Notifications', backref='apps', lazy=True)
    appadmins = db.relationship('AppAdmin', backref='apps', lazy=True)

    def __init__(self, title):
        self.title = title

class Notifications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(80), unique=False, nullable=True)
    time = db.Column(db.String(80), unique=False, nullable=True)
    description = db.Column(db.String(80), unique=False, nullable=False)
    app_id = db.Column(db.Integer, db.ForeignKey('apps.id'), unique=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=False, nullable=True)

    def __init__(self, description, date, time,  app_id, user_id):
        self.description = description
        self.date = date
        self.time = time
        self.app_id = app_id
        self.user_id = user_id


###SCHEMA
class AppAdminSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password', 'app_id')
appadmin_schema = AppAdminSchema()
appadmin_all_schema = AppAdminSchema(many=True)


class NotificationsSchema(ma.Schema):
    class Meta:
        fields = ('id','description','time', 'date', 'app_id', 'user_id')
notif_schema = NotificationsSchema()
notifs_all_schema = NotificationsSchema(many=True)

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username')
user_schema = UserSchema()
users_all_schema = UserSchema(many=True)

class AppSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title')
app_schema = AppSchema()
apps_all_schema = AppSchema(many=True)

#### ROUTES

#Retrieve Notifications
@app.route('/notifications', methods=['POST'])
def dump_notifs():
        try:
            token = request.form['token']
            app_id = token_verify(token)['app_id']
            print(app_id, file=sys.stdout)
            query_notif = Notifications.query.filter_by(app_id=app_id)
            dump_notif = notifs_all_schema.dump(query_notif)
            return jsonify({"message" :"OK", "Notifications" : dump_notif})
        except Exception as error:
            return jsonify({"message" : "Invalid Token"})

#Add App admin
@app.route('/signup/app', methods=['POST'])
def new_app_admin():
   app_name =  request.form['app']
   add_app = App(app_name)
   db.session.add(add_app)
   db.session.commit()###Add new app name

   username = request.form['username']
   password = request.form['password']
   app_query = App.query.filter_by(title=app_name)
   app_dump = apps_all_schema.dump(app_query) 
   app_id = app_dump[0]['id']
   add_admin = AppAdmin(username, password, app_id)
   db.session.add(add_admin)
   db.session.commit()#Add new admin

   return jsonify({"message:" : "OK"})

#App Admin LOGIN
@app.route('/app/login', methods=['POST'])
def app_login():
   username = request.form['username']
   password = request.form['password']
   try:
       admin_query = AppAdmin.query.filter_by(username=username)
       admin_dump = appadmin_all_schema.dump(admin_query)
       #print(admin_dump, file=sys.stdout)
       admin_password = admin_dump[0]['password']
       app_id = admin_dump[0]['app_id']
       if admin_password == password:
           return jsonify({"message" : "OK","token" : token_encode(username,app_id)}) ,200
       else:
            return jsonify({"message" : "Unauthorized access."}) ,403
   except Exception as error:
       print(error, file=sys.stdout)
       return jsonify({"message" : "Unauthorized access."}) ,403


# New App Activity
@app.route('/add/activity', methods=['POST'])
def add_activity():
   try:
        token = request.form['token']
        app_id = token_verify(token)['app_id']###Get APP id from token
        date = request.form['date']
        time = request.form['time']
        description = request.form['description']
        user_id = request.form['user_id']
        add_activity = Notifications(description, date, time,  app_id, user_id) 
        db.session.add(add_activity)
        db.session.commit()###save new activity
        return jsonify({"message": "New activity added sucessfully"}) ,200
   except Exception as error:
       return jsonify({"message": "Token Invalid"}) ,403

   
   



# if __name__ == "__main__":
#     app.run(port=5005)