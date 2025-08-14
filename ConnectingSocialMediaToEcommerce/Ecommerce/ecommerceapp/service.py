from django.db.models import Sum

from .beans import ProductBean
from .models import RatingModel, CommentModel, ProductModel
from .constants import SOCIAL_DB_PATH

import sqlite3
import datetime

def getProductById(productid):

    product=ProductModel.objects.get(id=productid)
    product.path = str(product.path).split("/")[1]

    comments = CommentModel.objects.filter(product=product.id)

    rating = 0
    count = 0

    for ratingmodel in RatingModel.objects.filter(product=product.id):
        rating = rating + int(ratingmodel.rating)
        count = count + 1

    totalrating = 0

    print("rating", rating)
    print("count", count)

    try:
        totalrating = int((rating / count))
    except Exception as e:
        print(e)

    print(totalrating)

    bean = ProductBean(product, comments, totalrating, product.description)

    return bean

def getAllProducts():

    products = []

    for product in ProductModel.objects.all():

        product.path = str(product.path).split("/")[1]

        comments = CommentModel.objects.filter(product=product.id)

        rating = 0
        count=0

        for ratingmodel in RatingModel.objects.filter(product=product.id):
            rating=rating+int(ratingmodel.rating)
            count=count+1

        totalrating=0

        print("rating",rating)
        print("count", count)

        try:
            totalrating=int((rating / count))
        except Exception as e:
            print(e)

        print(totalrating)

        bean = ProductBean(product, comments,totalrating,product.description)

        products.append(bean)

    return products


def get_age_group(dob):
    today = datetime.date.today()
    birth_date = datetime.datetime.strptime(dob, "%Y-%m-%d").date()  # Assuming dob format is 'YYYY-MM-DD'
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    if age < 13:
        return "Kids"
    elif 13 <= age <= 19:
        return "Teenagers"
    elif 20 <= age <= 35:
        return "Young Adults"
    elif 36 <= age <= 50:
        return "Middle Aged"
    else:
        return "Seniors"

def findrecommendations(username):

    # Connect to SQLite
    conn = sqlite3.connect(SOCIAL_DB_PATH)
    cursor = conn.cursor()

    try:
        
        # Step 1: Fetch user details
        cursor.execute("SELECT dob, gender, interests FROM osn_registrationmodel WHERE username = ?", (username,))
        user_row = cursor.fetchone()

        if not user_row:
            return []  # User not found

        dob, gender, interests_str = user_row
        interests = [i.strip().lower() for i in interests_str.split(",")] if interests_str else []
        user_gender = gender.lower()
        print("gender_original:",user_gender)
        user_age_group = get_age_group(dob)

        # Step 2: Fetch user's posts
        cursor.execute("SELECT title, description, tags FROM osn_postmodel WHERE username = ?", (username,))
        post_rows = cursor.fetchall()

        # Step 3: Fetch comments's posts
        cursor.execute("SELECT comment FROM osn_commentmodel WHERE username = ?", (username,))
        comment_rows = cursor.fetchall()

        post_tokens = set()
        
        for title, description, tags in post_rows:
            title_tokens = title.lower().split() if title else []
            description_tokens = description.lower().split() if description else []
            tags_tokens = [t.strip().lower() for t in tags.split(",")] if tags else []
            post_tokens.update(title_tokens + description_tokens + tags_tokens)

        for comment in comment_rows:
            print("comment:",comment,len(comment))
            comment_tokens = comment[0].lower().split() if comment[0] else []
            post_tokens.update(comment_tokens)

        matched_products = []

        print("Length:",len(getAllProducts()),"Type:",type(getAllProducts()))

        for prod in getAllProducts():
            
            print("in for ")

            name=prod.product.name
            description=prod.product.description
            tags=prod.product.tags
            prod_gender=prod.product.gender
            prod_age_group = prod.product.age_group

            print(name,description,tags,prod_gender,prod_age_group)

            # Product tags and description tokens
            product_tags = [t.strip().lower() for t in tags.split(",")] if tags else []
            product_tokens = name.lower().split() + (description.lower().split() if description else [])

            # Conditions for recommendation

            tag_match = bool(set(product_tags) & set(interests + list(post_tokens)))
            print("--------------------------------------------------------------")
            print(set(product_tags))
            print(list(post_tokens))
            print(tag_match)
            print("--------------------------------------------------------------")

            token_match = bool(set(product_tokens) & set(interests + list(post_tokens)))
            print("--------------------------------------------------------------")
            print(set(product_tokens))
            print(list(post_tokens))
            print(token_match)
            print("--------------------------------------------------------------")

            gender_match = False

            if user_gender==prod_gender.lower():
                gender_match=True

            print("--------------------------------------------------------------")
            print(user_gender)
            print(prod_gender)
            print(gender_match)
            print("--------------------------------------------------------------")

            age_group_match = user_age_group.lower() in prod_age_group.lower()

            print("--------------------------------------------------------------")
            print(user_age_group)
            print(prod_age_group)
            print(age_group_match)
            print("--------------------------------------------------------------")

            if tag_match or token_match or gender_match or age_group_match:
                print("if append ")
                matched_products.append(prod)

            print("for end ")

        return matched_products

    finally:
        conn.close()
