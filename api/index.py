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

app = Flask(__name__)

@app.route('/fortunes', methods=['GET'])
def get_fortunes():
    fortunes = [
        {'id': 1, 'message': 'You will soon find yourself in a favorable position.'},
        {'id': 2, 'message': 'A new opportunity is coming your way.'},
        {'id': 3, 'message': 'Good luck will soon shine upon you.'}
    ]
    return jsonify(fortunes)

if __name__ == '__main__':
    app.run(debug=True)