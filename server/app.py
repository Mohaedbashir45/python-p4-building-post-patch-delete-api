#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, User, Review, Game

app = Flask(__name__)

@app.route('/games')
def games():
    games = Game.query.all()
    games_list = [game.to_dict() for game in games]
    response = make_response(jsonify(games_list), 200)
    return response

@app.route('/games/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def game_by_id(id):
    game = Game.query.get(id)

    if not game:
        return make_response(jsonify({'error': 'Game not found'}), 404)

    if request.method == 'GET':
        return make_response(jsonify(game.to_dict()), 200)
    elif request.method == 'DELETE':
        db.session.delete(game)
        db.session.commit()
        return make_response(jsonify({'delete_successful': True, 'message': 'Game deleted'}), 200)

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'GET':
        reviews = [review.to_dict() for review in Review.query.all()]
        return make_response(jsonify(reviews), 200)
    elif request.method == 'POST':
        new_review = Review(
            score=request.form.get('score'),
            comment=request.form.get('comment'),
            game_id=request.form.get('game_id'),
            user_id=request.form.get('user_id'),
        )
        db.session.add(new_review)
        db.session.commit()
        return make_response(jsonify(new_review.to_dict()), 201)

@app.route('/reviews/<int:id>', methods=['PATCH', 'DELETE'])
def review_by_id(id):
    review = Review.query.get(id)

    if not review:
        return make_response(jsonify({'error': 'Review not found'}), 404)

    if request.method == 'PATCH':
        for attr in request.form:
            setattr(review, attr, request.form.get(attr))
        db.session.commit()
        return make_response(jsonify(review.to_dict()), 200)
    elif request.method == 'DELETE':
        db.session.delete(review)
        db.session.commit()
        return make_response(jsonify({'delete_successful': True, 'message': 'Review deleted'}), 200)

@app.route('/users')
def users():
    users = [user.to_dict() for user in User.query.all()]
    return make_response(jsonify(users), 200)

if __name__ == '__main__':
    app.run(debug=True)
