from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.car import Car
from models.rental import Rental
from models.user import User
from datetime import datetime

rental = Blueprint('rental', __name__)

@rental.route('/cars', methods=['GET'])
def list_cars():
    cars = Car.objects()
    return jsonify([{
        "id": str(c.id),
        "brand": c.brand,
        "model": c.model,
        "daily_rate": c.daily_rate,
        "is_available": c.is_available
    } for c in cars])

@rental.route('/cars', methods=['POST'])
@jwt_required()
def add_car():
    data = request.get_json()
    car = Car(**data)
    car.save()
    return jsonify(msg="Car added")

@rental.route('/cars/<car_id>', methods=['PUT'])
@jwt_required()
def update_car(car_id):
    data = request.get_json()
    Car.objects(id=car_id).update_one(**data)
    return jsonify(msg="Car updated")

@rental.route('/cars/<car_id>', methods=['DELETE'])
@jwt_required()
def delete_car(car_id):
    Car.objects(id=car_id).delete()
    return jsonify(msg="Car deleted")

@rental.route('/rent/<car_id>', methods=['POST'])
@jwt_required()
def rent_car(car_id):
    user_id = get_jwt_identity()
    user = User.objects(id=user_id).first()
    car = Car.objects(id=car_id, is_available=True).first()
    if not car:
        return jsonify(msg="Car not available"), 400
    rental = Rental(user=user, car=car)
    rental.save()
    car.is_available = False
    car.save()
    return jsonify(msg="Car rented")

@rental.route('/return/<rental_id>', methods=['POST'])
@jwt_required()
def return_car(rental_id):
    rental = Rental.objects(id=rental_id, status="active").first()
    if not rental:
        return jsonify(msg="Rental not found or already returned"), 404

    rental.end_date = datetime.utcnow()
    rental.status = "completed"
    days = (rental.end_date - rental.start_date).days + 1
    rental.total_price = days * rental.car.daily_rate
    rental.save()

    rental.car.is_available = True
    rental.car.save()

    return jsonify(msg="Car returned", total_price=rental.total_price)

@rental.route('/myrentals', methods=['GET'])
@jwt_required()
def my_rentals():
    user_id = get_jwt_identity()
    user = User.objects(id=user_id).first()
    rentals = Rental.objects(user=user)
    return jsonify([{
        "id": str(r.id),
        "car": f"{r.car.brand} {r.car.model}",
        "start_date": r.start_date.strftime("%Y-%m-%d"),
        "status": r.status,
        "total_price": r.total_price
    } for r in rentals])
