from flask import Flask, request, jsonify, session, render_template
import os

app = Flask(__name__)


@app.route('/')
def index():
    session['data'] = []
    session.modified = True
    return render_template('index.html')

@app.route('/todo/create', methods=['POST'])
def add():
    if request.method != 'POST':
        return "error: wrong request type"
    if 'data' not in session:
        return "error: session data was not initialized"
    task = request.json
    session['data'].append(task)
    session.modified = True
    print(session['data']) #print the session to make sure it was added
    return jsonify({"result":"success", "task":task})

@app.route('/todo/read', methods=['GET'])
def fetch():
    if 'data' not in session:
        return "error: session data was not initialized"
    return jsonify({"result":"success", "task": session['data']})

@app.route('/todo/update', methods=['PUT'])
def update():
    if request.method != 'PUT':
        return "error: wrong request type"
    if len(request.json) != 2:
        return 'error: 2 parameters not sent'
    if 'data' not in session:
        return "error: session data was not initialized"
    index = request.get_json()['index']
    task = request.get_json()['task']
    if len(session['data']) < int(index) or len(session['data']) < 0:
        return "error: index out of range"
    session['data'][int(index)-1] = task
    session.modified = True
    print(session['data']) #print the session to make sure it was added
    return jsonify("success")

@app.route('/todo/delete', methods=['DELETE'])
def delete():
    if request.method != 'DELETE':
        return "error: wrong request type"
    deleteIndex = request.json
    if len(session['data']) < int(deleteIndex) or len(session['data']) < 0:
    	return "error: index out of range"
    del session['data'][int(deleteIndex)]
    session.modified = True
    print(session['data']) #print the session to make sure it was deleted
    return jsonify("success")



if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(debug=True)
