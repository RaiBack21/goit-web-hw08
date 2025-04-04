from mongoengine import Document
from mongoengine.fields import StringField, BooleanField

class Contact(Document):
    fullname = StringField()
    email = StringField()
    number = StringField()
    favorite = StringField()
    is_sent = BooleanField(default=False)