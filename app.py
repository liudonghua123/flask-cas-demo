import os
from flask import Flask, request, session, redirect, url_for, render_template, flash
from cas import CASClient
import logging

app = Flask(__name__)
app.secret_key = 'some_secret_key_here'

# configure the cas of ynu
CAS_SERVER = 'https://ids.ynu.edu.cn'

# Create CAS client using factory
cas_client = CASClient(
    version=3,
    service_url='http://localhost:8080/login',
    server_url=f"{CAS_SERVER}/authserver/"
)

def login_required(f):
    """Decorator to require CAS login"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    next_url = request.args.get('next')
    if next_url:
        return redirect(next_url)
    return render_template('index.html')

@app.route("/protected")
@login_required
def protected():
    username = session.get('username')
    attributes = session.get('attributes', {})
    return render_template('protected.html', username=username, attributes=attributes)

@app.route("/login")
def login():
    """CAS login handler"""
    next_url = request.args.get('next') or url_for('index')
    if 'username' in session:
        return redirect(next_url)

    ticket = request.args.get('ticket')
    if not ticket:
        cas_login_url = cas_client.get_login_url()
        app.logger.debug('CAS login URL: %s', cas_login_url)
        return redirect(f'{cas_login_url}?next={next_url}')
    
    app.logger.debug('ticket: %s', ticket)

    user, attributes, pgtiou = cas_client.verify_ticket(ticket)
    app.logger.debug('CAS verify: user=%s, attributes=%s, pgtiou=%s', user, attributes, pgtiou)

    if not user:
        flash('Failed to verify ticket', 'error')
        return redirect(url_for('login'))
    else:
        session['username'] = user
        session['attributes'] = attributes or {}
        flash(f'Welcome, {user}!', 'success')
        return redirect(next_url)

@app.route("/logout")
def logout():
    session.clear()
    redirect_url = url_for('index', _external=True)
    cas_logout_url = cas_client.get_logout_url(redirect_url)
    return redirect(cas_logout_url)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)