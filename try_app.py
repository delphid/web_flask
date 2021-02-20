from flask import Flask,request, redirect, url_for, make_response
import json

app = Flask(__name__)

@app.route("/")
def index():
    rsp = make_response('Hello World!')
    rsp.headers['aaa'] = ['bbb']
    return dict(request.headers)
    #return rsp

@app.route("/another")
def another_page():
    return "new page 3"

@app.route("/try_customized_url/<name1>")
def costimized_url(name1):
    return name1

@app.route('/owner')
def as_owner():
    return "now visit as owner"

@app.route('/<guest>')
def as_guest(guest):
    return f"{guest} is now visitting as guest"

@app.route('/user/<name>')
def which_user(name):
    if name == 'owner':
        return redirect(url_for('as_owner'))
    else:
        return redirect(url_for('as_guest', guest=name))

@app.route('/try-api', methods=['POST', 'GET'])
def my_api():
    if request.method == 'GET':
        request_dict = request.args.to_dict()
    elif request.method == 'POST':
        # request.get_data() -> bytes
        # json.loads(bytes) -> dict
        request_dict = json.loads(request.get_data())
    return_dict = request_dict
    return json.dumps(return_dict)

app.run(debug=True, port=3000)
