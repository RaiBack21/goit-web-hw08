from mongoengine import Document
from mongoengine.fields import StringField, DateTimeField,\
    ReferenceField, ListField

class Author(Document):
    fullname = StringField()
    born_date = DateTimeField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField('Author', reverse_delete_rule='CASCADE')
    quote = StringField()
    meta = {'allow_inheritance': True}