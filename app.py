from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

cards = []

@app.route('/')
def index():
    return "Welcome! Use /cards to access the cards endpoint."

@app.route('/cards', methods=['GET'])
def get_cards():
    app.logger.debug('GET /cards called')
    return jsonify(cards)

@app.route('/cards', methods=['POST'])
def add_card():
    app.logger.debug('POST /cards called')
    image_front = request.files['imageFront']
    image_back = request.files['imageBack']
    card = {
        'id': len(cards) + 1,
        'name': request.form.get('name', 'Unknown'),
        'imageFront': f'/static/{image_front.filename}',
        'imageBack': f'/static/{image_back.filename}',
    }
    image_front.save(os.path.join('static', image_front.filename))
    image_back.save(os.path.join('static', image_back.filename))
    cards.append(card)
    return jsonify(card), 201

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True)