from mongoengine import Document, ReferenceField, DateTimeField, StringField, FloatField
from models.user import User
from models.car import Car
from datetime import datetime

class Rental(Document):
    user = ReferenceField(User, required=True)
    car = ReferenceField(Car, required=True)
    start_date = DateTimeField(default=datetime.utcnow)
    end_date = DateTimeField()
    status = StringField(default="active")
    total_price = FloatField()
