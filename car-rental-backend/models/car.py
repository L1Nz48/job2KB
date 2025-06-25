from mongoengine import Document, StringField, FloatField, BooleanField

class Car(Document):
    brand = StringField(required=True)
    model = StringField(required=True)
    daily_rate = FloatField(required=True)
    is_available = BooleanField(default=True)
