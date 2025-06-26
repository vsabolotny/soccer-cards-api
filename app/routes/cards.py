from flask import Blueprint, request, jsonify
from ..models.card import Card
from ..services.card_service import CardService

bp = Blueprint('cards', __name__)
card_service = CardService()

@bp.route('/cards', methods=['GET'])
def get_cards():
    filters = request.args
    cards = card_service.get_all_cards(filters)
    return jsonify(cards)

@bp.route('/cards', methods=['POST'])
def add_card():
    data = request.form
    image_front = request.files['imageFront']
    image_back = request.files['imageBack']
    card = card_service.add_card(data, image_front, image_back)
    return jsonify(card), 201

@bp.route('/cards/<int:card_id>', methods=['GET'])
def get_card(card_id):
    card = card_service.get_card_by_id(card_id)
    if card:
        return jsonify(card)
    return jsonify({'message': 'Card not found'}), 404

@bp.route('/cards/<int:card_id>', methods=['DELETE'])
def delete_card(card_id):
    success = card_service.delete_card(card_id)
    if success:
        return jsonify({'message': 'Card deleted successfully'}), 204
    return jsonify({'message': 'Card not found'}), 404