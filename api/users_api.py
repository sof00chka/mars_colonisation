import flask
from flask import jsonify, make_response, request
from datetime import datetime

from data import db_session
from data.users import User

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users', methods=['GET'])
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'surname', 'name', 'age',
                                    'position', 'speciality', 'address',
                                    'email', 'modified_date'))
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.get(User, user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'user': user.to_dict(only=('id', 'surname', 'name', 'age',
                                       'position', 'speciality', 'address',
                                       'email', 'modified_date'))
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['surname', 'name', 'email', 'age']):
        return make_response(jsonify({'error': 'Bad request'}), 400)

    db_sess = db_session.create_session()

    existing_user = db_sess.query(User).filter(User.email == request.json['email']).first()
    if existing_user:
        return make_response(jsonify({'error': 'Email already exists'}), 400)

    try:
        age = int(request.json['age'])
        if age < 0 or age > 150:
            return make_response(jsonify({'error': 'Age must be between 0 and 150'}), 400)
    except (ValueError, TypeError):
        return make_response(jsonify({'error': 'Age must be integer'}), 400)

    user = User(
        surname=request.json['surname'],
        name=request.json['name'],
        age=age,
        position=request.json.get('position'),
        speciality=request.json.get('speciality'),
        address=request.json.get('address'),
        email=request.json['email'],
        modified_date=datetime.now()
    )

    db_sess.add(user)
    db_sess.commit()
    return jsonify({'id': user.id})


@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.get(User, user_id)

    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)

    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)

    if 'surname' in request.json:
        user.surname = request.json['surname']
    if 'name' in request.json:
        user.name = request.json['name']
    if 'age' in request.json:
        try:
            age = int(request.json['age'])
            if age < 0 or age > 150:
                return make_response(jsonify({'error': 'Age must be between 0 and 150'}), 400)
            user.age = age
        except (ValueError, TypeError):
            return make_response(jsonify({'error': 'Age must be integer'}), 400)
    if 'position' in request.json:
        user.position = request.json['position']
    if 'speciality' in request.json:
        user.speciality = request.json['speciality']
    if 'address' in request.json:
        user.address = request.json['address']
    if 'email' in request.json:
        existing_user = db_sess.query(User).filter(User.email == request.json['email'], User.id != user_id).first()
        if existing_user:
            return make_response(jsonify({'error': 'Email already in use'}), 400)
        user.email = request.json['email']

    user.modified_date = datetime.now()
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.get(User, user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


from flask import render_template
import requests


@blueprint.route('/users_show/<int:user_id>', methods=['GET'])
def show_user_city(user_id):
    db_sess = db_session.create_session()
    user = db_sess.get(User, user_id)
    if not user:
        return make_response(jsonify({'error': 'User not found'}), 404)

    city = user.city_from
    if not city:
        return make_response(jsonify({'error': 'City not specified'}), 404)

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": city,
        "format": "json"
    }

    try:
        response = requests.get(geocoder_api_server, params=geocoder_params)
        json_response = response.json()
        feature_member = json_response["response"]["GeoObjectCollection"]["featureMember"]

        if feature_member:
            toponym = feature_member[0]["GeoObject"]
            toponym_coordinates = toponym["Point"]["pos"]
            lon, lat = toponym_coordinates.split(" ")

            return render_template('user_city.html',
                                   user=user,
                                   city=city,
                                   lon=lon,
                                   lat=lat,
                                   api_key='f3a0fe3a-b07e-4840-a1da-06f18b2ddf13')
        else:
            return render_template('user_city.html',
                                   user=user,
                                   city=city,
                                   error="Город не найден")
    except Exception as e:
        return render_template('user_city.html',
                               user=user,
                               city=city,
                               error=f"Ошибка: {str(e)}")
