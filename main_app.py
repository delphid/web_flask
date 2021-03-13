from collections import defaultdict
import logging
import secrets

from flask import Flask, redirect, url_for, request, render_template, g, session
from jinja2 import Markup, Environment, FileSystemLoader
from pyecharts.globals import CurrentConfig

from loan import Loan, PlotLoan


CurrentConfig.GLOBAL_ENV = Environment(loader=FileSystemLoader('./templates/pyecharts_templates'))

app = Flask(__name__, static_folder='static')
app.secret_key = secrets.token_urlsafe()
logging.basicConfig(level=logging.DEBUG)


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
    loan_amount_yuan = int(request.form['loan_amount_yuan'])
    yearly_interest_rate = float(request.form['yearly_interest_rate']) / 100
    year_limit = int(request.form['year_limit'])
    loan = Loan(
        loan_amount_yuan = loan_amount_yuan,
        yearly_interest_rate = yearly_interest_rate,
        year_limit = year_limit)
    plot_loan = PlotLoan(
        p_num=loan.p_num,
        values_lists=loan.calc_plot_values())
    #app.secret_key = secrets.token_urlsafe()
    session['plot_loan'] = plot_loan.dict()
    session['calc_input'] = dict(request.form)
    return redirect(request.referrer)

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
