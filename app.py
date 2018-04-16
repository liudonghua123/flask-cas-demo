from flask import Flask
from flask_cas import CAS, login_required
from flask.ext.cas import login
from flask.ext.cas import logout
import logging

app = Flask(__name__)
cas = CAS(app)

# configure the cas of ynu
app.config['CAS_SERVER'] = 'http://ids.ynu.edu.cn'
app.config['CAS_LOGIN_ROUTE'] = '/authserver/login'
app.config['CAS_LOGOUT_ROUTE'] = '/authserver/logout'
app.config['CAS_VALIDATE_ROUTE'] = '/authserver/serviceValidate'

# configure some other settings
app.config['CAS_AFTER_LOGIN'] = '/'
app.config['SECRET_KEY'] = 'some_secret_key_here'

    
@app.route("/")
@login_required
def index():
    username = cas.username
    return "index of " + username

@app.route("/test")
@login_required
def test():
    username = cas.username
    return "test page of " + username

app.run(host='0.0.0.0', port=80, debug=True)