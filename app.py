from flask import Flask, render_template
from flask_cas import CAS, login_required
from flask_cas import login
from flask_cas import logout
import logging
from pprint import pprint
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
cas = CAS(app)

# configure the cas of ynu
# app.config['CAS_SERVER'] = 'http://ids.ynu.edu.cn'
# app.config['CAS_LOGIN_ROUTE'] = '/authserver/login'
# app.config['CAS_LOGOUT_ROUTE'] = '/authserver/logout'
# app.config['CAS_VALIDATE_ROUTE'] = '/authserver/serviceValidate'
# standard cas
app.config['CAS_SERVER'] = 'http://localhost:8080'
app.config['CAS_LOGIN_ROUTE'] = '/cas/login'
app.config['CAS_LOGOUT_ROUTE'] = '/cas/logout'
app.config['CAS_VALIDATE_ROUTE'] = '/cas/serviceValidate'

# configure some other settings
app.config['CAS_AFTER_LOGIN'] = '/'
app.config['SECRET_KEY'] = 'some_secret_key_here'

# # set the configration of flask_debugtoolbar
# app.config['DEBUG_TB_ENABLED'] = True
# # the toolbar is only enabled in debug mode:
# app.debug = True
# https://pypi.org/project/Flask-DebugToolbar/
toolbar = DebugToolbarExtension(app)

    
@app.route("/")
@login_required
def index():
    username = cas.username
    return "This is protected index content of " + username

@app.route("/protected/")
@login_required
def protected():
    # import pdb; pdb.set_trace()
    # pprint(vars(cas))
    username = cas.username
    # cas.attributes['myattr'] = 'myvalue'
    # return "This is protected content of " + username
    return render_template('protected.html', username = username, cas = cas)

@app.route("/public/")
def public():
    return "This is public content!"

app.run(host='0.0.0.0', port=9000, debug=True)