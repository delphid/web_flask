import logging

from flask import Flask, redirect, url_for, request, render_template, g

import module1


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route('/user/', defaults={'name': None})
@app.route('/user/<name>', methods=['GET'])
def user_page(name):
    app.logger.info(request.args)
    g.user_name = name
    if request.args.get('action') == 'return to login page':
        return redirect(url_for('login_page'))
    return render_template('user.html')

@app.route('/')
@app.route('/login/', methods=['POST', 'GET'])
def login_page():
    a1 = module1.A()
    g.some_info = a1.a
    if request.method == 'POST':
        user = request.form['the_name_box']
        if request.form['action'] == 'get logged in':
            return redirect(url_for('user_page', name=user))
        elif request.form['action'] == 'print name':
            app.logger.info(request.form['the_name_box'])
            return render_template('login.html')
    else:
        user = request.args.get('the_name_box')
        if user != None:
            return redirect(url_for('user_page', name=user))
        return render_template('login.html')

app.run(host='localhost', debug=True, port=3000)
