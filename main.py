from flask import Flask, request
from flask_cors import CORS, cross_origin
import json
app = Flask(__name__)
app.debug = True
CORS(app)

todos = []
indexTd = 0


@app.route('/', methods=['GET'])
def get():
    response = app.response_class(
        response=json.dumps(todos),
        status=200,
        mimetype='application/json'
    )
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/', methods=['POST'])
def post():
    global indexTd
    data = request.get_json()
    data['completed'] = False
    data['url'] = "http://127.0.0.1:5000/todos/" + str(indexTd)
    data['index'] = indexTd
    if 'order' not in data:
        data['order'] = 0
    indexTd += 1
    print data
    todos.append(data)
    return json.dumps(data), 201, {}


@app.route('/', methods=['DELETE'])
def delete():
    global todos
    todos = []
    response = app.response_class(
        response=json.dumps(todos),
        status=204,
        mimetype='application/json'
    )
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/todos/<int:id>', methods=['GET'])
def getTodo(id):
    # result
    for item in todos:
        if item['index'] == id:
            response = app.response_class(
                response=json.dumps(item),
                status=200,
                mimetype='application/json'
            )
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
            #print str(id)
    return "Item not find at this id", 404


@app.route('/todos/<int:id>', methods=['PATCH'])
def patchName(id):
    data = request.get_json()
    for item in todos:
        if item['index'] == id:
            if 'title' in data:
                item['title'] = data['title']
            if 'completed' in data:
                item['completed'] = data['completed']
            if 'order' in data:
                item['order'] = data['order']
            if 'title' not in data and 'completed' not in data and 'order' not in data:
                return "Error Bad Request", 400

            response = app.response_class(
                response=json.dumps(item),
                status=200,
                mimetype='application/json'
            )
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
            # print item
            # return json.dumps(item), 204, {'content-type':
            # 'application/json'}


@app.route('/todos/<int:id>', methods=['DELETE'])
def deleteItem(id):
    for index, item in enumerate(todos):
        if item['index'] == id:
            todos.pop(index)
            response = app.response_class(
                response=json.dumps(item),
                status=200,
                mimetype='application/json'
            )
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response


if __name__ == "__main__":
    app.run()
