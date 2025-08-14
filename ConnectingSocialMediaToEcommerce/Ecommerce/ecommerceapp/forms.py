from django.forms import Form, CharField, PasswordInput, FileField


class RegistrationForm(Form):

    username =CharField(max_length=50)
    name = CharField(max_length=50)
    password =CharField(max_length=50)
    mobile =CharField(max_length=50)
    address =CharField(max_length=50)

class LoginForm(Form):

    username = CharField(max_length=100)
    password = CharField(widget=PasswordInput())

class ProductForm(Form):

    name = CharField(max_length=500)
    price = CharField(max_length=30)
    manufacturer =CharField(max_length=500)
    category = CharField(max_length=500)
    description = CharField(max_length=500)
    path = FileField()
    tags=CharField(max_length=500)
    gender=CharField(max_length=500)
    age_group=CharField(max_length=500)

class CommentForm(Form):

    text = CharField(max_length=300)
    product = CharField(max_length=60)

class SearchHistoryForm(Form):

    keyord = CharField(max_length=300)

class RatingForm(Form):

    rating = CharField(max_length=100)
    product = CharField(max_length=60)