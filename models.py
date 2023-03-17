from mongoengine import *

connect(host="mongodb+srv://PWHomeWork:123321@cluster0.duijelz.mongodb.net/PWHomeWork9?retryWrites=true&w=majority",
        ssl=True)


class Authors(Document):
    fullname = StringField(max_length=50, required=True)
    born_date = StringField()
    born_location = StringField(max_length=150)
    description = StringField()


class Quotes(Document):
    tags = ListField(StringField(max_length=50))
    author = ReferenceField(Authors)
    quote = StringField()
