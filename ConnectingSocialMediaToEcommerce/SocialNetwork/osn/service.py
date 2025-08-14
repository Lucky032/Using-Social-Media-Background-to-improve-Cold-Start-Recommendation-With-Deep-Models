from .beans import PostBean
from .models import LikeOrDisLikeModel, CommentModel, PostModel, ShareModel, FriendRequestModel, RegistrationModel

def getPostBeanById(postid):

    post=PostModel.objects.get(id=postid)
    post.image = str(post.image).split("/")[1]
    comments = CommentModel.objects.filter(post=post.id)
    likes = 0
    dislikes = 0

    for likeordislike in LikeOrDisLikeModel.objects.filter(post=post.id):
        if int(likeordislike.status) == 0:
            dislikes = dislikes + 1
        elif int(likeordislike.status) == 1:
            likes = likes + 1


    return PostBean(post, comments, likes, dislikes)

def getAllPosts():

    posts = []

    for post in PostModel.objects.all().order_by('-datetime'):
        posts.append(getPostBeanById(post.id))

    return posts

def getAllPostsByUser(username):

    posts = []

    friends=getMyFriends(username)
    friends.add(username)

    friends=list(friends)

    print("users", friends)

    for post in PostModel.objects.filter(username__in=friends).order_by('-datetime'):
        posts.append(getPostBeanById(post.id))

    for share in ShareModel.objects.filter(username__in=friends):
        print("shares", friends)
        posts.append(getPostBeanById(share.post))

    return posts

def getAllPostsBySearch(keyword):

    posts = []

    for post in PostModel.objects.order_by('-datetime'):
        if keyword in post.title or keyword in post.username:
            posts.append(getPostBeanById(post.id))

    return posts

def getMyFriends(username):

    friends=set()

    for request in FriendRequestModel.objects.filter(username=username,status="yes"):
        friends.add(request.friendname)

    for request in FriendRequestModel.objects.filter(friendname=username,status="yes"):
        friends.add(request.username)

    return friends
