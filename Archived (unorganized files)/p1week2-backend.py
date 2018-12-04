from flask import Flask, request, jsonify, session, render_template

app = Flask(__name__)

# app.secret_key = "jfidibfjnjzjkwf3iu99r9dhvjer0"
#I assigned data to an empty list and then I will let session equal to data therefore data won't be 
# empty therefore no error
data = []

@app.route('/')
def index():
    #  we do not need this part b/c this will reset the session to a
    # empty list, which when the user refresh the page the whole session would be reset 
    # session['data'] = []
    # session.modified = True
    return render_template('index.html')

@app.route('/todo/create', methods=['POST'])
def add():
    # if request.method != 'POST':
    #     return "error: wrong request type"
    # if len(request.get_json(force=True)) != 1:
    #     return "error: 1 parameter not sent"
   # if 'data' not in session:
    #    return "error: session data was not initialized"
    #newItem = request.get_json(force=True)['content']
    newItem = request.form["thingstodo"]
    data.append(newItem)
    session['data'] = data
    # session.modified = True
    return jsonify({"result": session['data'][-1]})

@app.route('/todo/read')
def fetch():
    # these two lines of code below suggest that when the user first open the page,
    #it will automatically shown an error b/c session[data] DNE

    #if 'data' not in session:
     #   return jsonify({ "error": "session data was not initialized"})
    session["data"] = data
    return jsonify({"result":"success", "data": session['data']})

@app.route('/todo/update', methods=['PUT'])
def update():
    if request.method != 'PUT':
        return "error: wrong request type"
    if len(request.get_json(force=True) != 2):
        return 'error: 2 parameters not sent'
    if 'data' not in session:
        return "error: session data was not initialized"
    if len(session['data']) >= index or session['data'] < 0:# what does index refer to here? I'm confused
        return "error: index out of range"
    index = request.get_json(force=True)['item']
    data = request.get_json(force=True)['content']
    session['data'][index] = data
    session.modified = True
    return jsonify({"result": "success"})

@app.route('/todo/delete', methods=['DELETE'])
def delete():
    if request.method != 'DELETE':
        return "error: wrong request type"
    if len(request.get_json(force=True)) != 1:
        return "error: 1 parameter is not sent"
    if 'data' not in session:
        return "error: session data was not initialized"

    index = request.get_json(force=True)['item']
    session['data'].pop(index)
    session.modified = True
    return jsonify({"result": "success"})



if __name__ == '__main__':
    app.secret_key = 'random string' #os.urandom(24)
    app.run(debug=True)
