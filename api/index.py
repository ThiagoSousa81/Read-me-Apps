'''from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'About'
    '''
from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'Welcome to my API!'

@app.route('/equations', methods=['GET'])
def equations():
    equation = request.args.get('equation')
    if equation == None:
        return 'No equation provided', 400
    try:
        num1, num2, var = map(float, equation.split())
        result = np.solve([num1, num2], var)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)