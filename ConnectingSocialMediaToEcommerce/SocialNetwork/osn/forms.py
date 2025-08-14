from django.forms import Form, CharField, PasswordInput, FileField,MultipleChoiceField

INTEREST_CHOICES = [
    ('Technology', 'Technology'),
    ('Fashion', 'Fashion'),
    ('Electronics', 'Electronics'),
    ('Health & Fitness', 'Health & Fitness'),
    ('Books & Literature', 'Books & Literature'),
    ('Food & Cooking', 'Food & Cooking'),
    ('Travel & Adventure', 'Travel & Adventure'),
    ('Gaming', 'Gaming'),
    ('Sports', 'Sports'),
    ('Home Decor', 'Home Decor'),
    ('Beauty & Makeup', 'Beauty & Makeup'),
    ('Music', 'Music'),
    ('Movies & TV Shows', 'Movies & TV Shows'),
    ('Photography', 'Photography'),
    ('Cars & Bikes', 'Cars & Bikes'),
    ('Pets & Animals', 'Pets & Animals'),
    ('Finance & Investment', 'Finance & Investment'),
    ('Art & Design', 'Art & Design'),
    ('Education & Learning', 'Education & Learning'),
    ('Gardening', 'Gardening'),
    ('Mobile Phones', 'Mobile Phones'),
    ('Gadgets', 'Gadgets'),
    ('Baby & Kids', 'Baby & Kids'),
    ('Handicrafts', 'Handicrafts'),
    ('Online Shopping', 'Online Shopping'),
    ('Fitness Equipment', 'Fitness Equipment'),
    ('Smart Watches', 'Smart Watches'),
    ('Jewelry', 'Jewelry'),
    ('Stationery', 'Stationery'),
    ('Virtual Reality', 'Virtual Reality'),
    ('AI & Robotics', 'AI & Robotics'),
]

class RegistrationForm(Form):
    username = CharField(max_length=50)
    name = CharField(max_length=50)
    password = CharField(max_length=50)
    mobile = CharField(max_length=50)
    address = CharField(max_length=500)
    pic = FileField()
    gender = CharField(max_length=50)
    dob = CharField(max_length=50)
    interests = MultipleChoiceField(choices=INTEREST_CHOICES)

class UpdateProfileForm(Form):
    name = CharField(max_length=50)
    password = CharField(max_length=50)
    email = CharField(max_length=50)
    mobile = CharField(max_length=50)
    address = CharField(max_length=50)

class UpdatePICForm(Form):
    pic = FileField()

class LoginForm(Form):
    username = CharField(max_length=100)
    password = CharField(widget=PasswordInput())

class PostForm(Form):
    title = CharField(max_length=500)
    image = FileField()
    description = CharField(max_length=500)
    tags = CharField(max_length=500)

class CommentForm(Form):
    post = CharField(max_length=60)
    comment = CharField(max_length=3000)

class LikeOrDisLikeForm(Form):
    post = CharField(max_length=60)
    likeOrDislike = CharField(max_length=100)
