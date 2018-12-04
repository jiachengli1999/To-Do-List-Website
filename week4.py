from flask import Flask, request, jsonify, render_template
import os
import pymysql
import pymysql.cursors

app = Flask(__name__)
connection = pymysql.connect(host='localhost', 
                            db='task_database',
                            user='cs1122', 
                            password='cs1122',
                            charset='utf8mb4')

cur = connection.cursor()

@app.route('/')
def index():
    # session['data'] = []
    # session.modified = True
    return render_template('week4.html')

@app.route('/todo/create', methods=['POST'])
def add():
    if request.method != 'POST':
        return "error: wrong request type"
    task = request.json
    cur().execute("INSERT INTO task_table(task) VALUES(%s)",(task))
    connection.commit()
    cur().execute("SELECT * FROM task_table")
    items = cur().fetchall()
    print(items[-1])
    return jsonify({"result":"success", "task":items[-1]})

@app.route('/todo/read', methods=['GET'])
def fetch():
    cur().execute("SELECT * FROM task_table")
    items = cur().fetchall()     
    return jsonify({"result":"success", "task": items})

@app.route('/todo/update', methods=['PUT'])
def update():
    if request.method != 'PUT':
        return "error: wrong request type"
    if len(request.json) != 2:
        return 'error: 2 parameters not sent'
    index = request.get_json()['index']
    task = request.get_json()['task']
    cur().execute("UPDATE task_table SET task = %s WHERE task_index = %s",(task, index))
    connection.commit()
    return jsonify("success")

@app.route('/todo/delete', methods=['DELETE'])
def delete():
    if request.method != 'DELETE':
        return "error: wrong request type"
    deleteIndex = request.json
    print(deleteIndex)
    cur().execute("DELETE FROM task_table WHERE task_index = %s",(deleteIndex))
    connection.commit()
    return jsonify("success")

if __name__ == '__main__':
    app.secret_key = os.urandom(24)
    app.run(debug=True)
		# del session['data'][int(deleteIndex)]
		# session.modified = True
		# print(session['data']) #print the session to make sure it was deleted
		# return jsonify("success")
