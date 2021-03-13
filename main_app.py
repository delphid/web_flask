from collections import defaultdict
import json
import logging
import secrets
import time

from flask import Flask, redirect, url_for, request, render_template, g, session
from jinja2 import Markup, Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig

from loan import Loan, PlotLoan


CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader('./templates/pyecharts_templates'))

app = Flask(__name__, static_folder='static')
app.secret_key = secrets.token_urlsafe()
logging.basicConfig(level=logging.DEBUG)
LOG = app.logger


def get_flask_request_body(req: request):
    # when use curl or python request (not when use js):
    # a flask bug: can't retrive request body from request.json,
    # but have to do this method. work both for request.form and .values
    ImmutableMultiDict = req.form
    body_string = list(ImmutableMultiDict.keys())[0]
    body = json.loads(body_string)
    return body


@app.route('/user/', defaults={'name': None})
@app.route('/user/<name>', methods=['GET'])
def user_page(name):
    g.user_name = name
    if request.args.get('action') == 'return to login page':
        return redirect(url_for('login_page'))
    if 'plot_loan' in session:
        plot_loan = PlotLoan.parse_obj(session['plot_loan'])
        line_plot = plot_loan.plot()
        g.chart = Markup(line_plot.render_embed())
    else:
        g.chart = ''
    if 'calc_input' not in session:
        session['calc_input'] = defaultdict(str)
    g.calc_input = session['calc_input']
    return render_template('user.html')

@app.route('/plot/', methods=['POST'])
def plot():
    LOG.info(request.json)
    body = request.json
    loan_amount_yuan = int(body['loan_amount_yuan'])
    yearly_interest_rate = float(body['yearly_interest_rate']) / 100
    year_limit = int(body['year_limit'])
    loan = Loan(
        loan_amount_yuan = loan_amount_yuan,
        yearly_interest_rate = yearly_interest_rate,
        year_limit = year_limit)
    chart = loan.plot()
    return chart.dump_options_with_quotes()


@app.route('/')
@app.route('/login/', methods=['POST', 'GET'])
def login_page():
    if request.method == 'POST':
        user = request.form['the_name_box']
        if request.form['action'] == 'get logged in':
            return redirect(url_for('user_page', name=user))
        elif request.form['action'] == 'print name':
            return render_template('login.html')
    else:
        user = request.args.get('the_name_box')
        if user != None:
            return redirect(url_for('user_page', name=user))
        return render_template('login.html')

app.run(host='localhost', debug=True, port=3000)
