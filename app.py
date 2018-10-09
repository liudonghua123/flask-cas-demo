from flask import Flask, render_template, Response, stream_with_context
from flask_cas import CAS, login_required
from flask_cas import login
from flask_cas import logout
import requests
import logging
from pprint import pprint
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
cas = CAS(app)

# configure the cas of ynu
app.config['CAS_SERVER'] = 'http://ids.ynu.edu.cn'
app.config['CAS_LOGIN_ROUTE'] = '/authserver/login'
app.config['CAS_LOGOUT_ROUTE'] = '/authserver/logout'
app.config['CAS_VALIDATE_ROUTE'] = '/authserver/serviceValidate'
# standard cas
# app.config['CAS_SERVER'] = 'http://localhost:8080'
# app.config['CAS_LOGIN_ROUTE'] = '/cas/login'
# app.config['CAS_LOGOUT_ROUTE'] = '/cas/logout'
# app.config['CAS_VALIDATE_ROUTE'] = '/cas/serviceValidate'

# configure some other settings
app.config['CAS_AFTER_LOGIN'] = '/'
app.config['SECRET_KEY'] = 'some_secret_key_here'

# # set the configration of flask_debugtoolbar
# app.config['DEBUG_TB_ENABLED'] = True
# # the toolbar is only enabled in debug mode:
# app.debug = True
# https://pypi.org/project/Flask-DebugToolbar/
toolbar = DebugToolbarExtension(app)

@app.route("/protected/<path:url>")
@login_required
def protected(url):
    req = requests.get("http://github.com/{url}".format(url=url), stream = True)
    return Response(stream_with_context(req.iter_content()), content_type = req.headers['content-type'])

@app.errorhandler(404) 
def not_found(e): 
    return "404"

app.run(host='0.0.0.0', port=8080, debug=True)