from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from .models import *


# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        avatar = request.POST.get('avatar', '')
        bio = request.POST.get('bio', '')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username is already taken.'}, status=400)
        user = User(username=username, password=make_password(password), avatar=avatar, bio=bio)
        user.save()
        return JsonResponse({'success': 'User registered successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'User has not registered yet.'}, status=400)
        else:
            if check_password(password, User.objects.get(username=username).password):
                return JsonResponse({'success': 'User logged in successfully.'})
            else:
                return JsonResponse({'error': 'Password is not correct.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


def edit_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_username = request.POST.get('new_username')
        password = request.POST.get('password')
        avatar = request.POST.get('avatar', '')
        bio = request.POST.get('bio', '')

        user = User.objects.get(username=username)
        user.username = new_username
        user.password = make_password(password)
        user.avatar = avatar
        user.bio = bio
        user.save()
        return JsonResponse({'success': 'User info modified successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


def follow(request):
    if request.method == 'POST':
        if request.POST.get('_method') == 'PUT':
            follower_username = request.POST.get('follower')
            follower_id = User.objects.get(username=follower_username).id
            followee_username = request.POST.get('followee')
            followee_id = User.objects.get(username=followee_username).id
            Follow(follower_id=follower_id, followee_id=followee_id).save()
        elif request.POST.get('_method') == 'DELETE':
            follower_username = request.POST.get('follower')
            follower_id = User.objects.get(username=follower_username).id
            followee_username = request.POST.get('followee')
            followee_id = User.objects.get(username=followee_username).id
            Follow.objects.get(follower_id=follower_id, followee_id=followee_id).delete()
        else:
            return JsonResponse({'error': 'Invalid request method.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


def block(request):
    if request.method == 'POST':
        if request.POST.get('_method') == 'PUT':
            blocked_username = request.POST.get('blocked')
            blocked_id = User.objects.get(username=blocked_username).id
            blocker_username = request.POST.get('blocker')
            blocker_id = User.objects.get(username=blocker_username).id
            Block(blocked_id=blocked_id, blocker_id=blocker_id).save()
        elif request.POST.get('_method') == 'DELETE':
            blocked_username = request.POST.get('blocked')
            blocked_id = User.objects.get(username=blocked_username).id
            blocker_username = request.POST.get('blocker')
            blocker_id = User.objects.get(username=blocker_username).id
            Block.objects.get(blocked_id=blocked_id, blocker_id=blocker_id).delete()
        else:
            return JsonResponse({'error': 'Invalid request method.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


def message(request):
    if request.method == 'POST':
        sender_id = User.objects.get(username=request.POST.get('sender')).id
        receiver_id = User.objects.get(username=request.POST.get('receiver')).id
        content = request.POST.get('content')
        Message(sender_id=sender_id, receiver_id=receiver_id, content=content).save()
        return JsonResponse({'success': 'Message send successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


def post(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        posts_list = list(posts.values())
        return JsonResponse(posts_list, safe=False)
    if request.method == 'POST':
        user_id = User.objects.get(username=request.POST.get('username')).id
        username = request.POST.get('username')
        _type = request.POST.get('type')
        content = request.POST.get('content')
        location = request.POST.get('location')
        Post(user_id=user_id, username=username, type=_type, content=content, location=location, likes_count=0, comments_count=0, favorites_count=0).save()
        return JsonResponse({'success': 'Post successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


def likes(request):
    if request.method == 'POST':
        if request.POST.get('_method') == 'POST':
            user_id = User.objects.get(username=request.POST.get('username')).id
            post_id = request.POST.get('post_id')
            _likes = Likes(user_id=user_id, post_id=post_id)
            _likes.save()
            Post.objects.get(id=post_id).likes_count -= 1
            return JsonResponse({'success': 'Likes successfully.'})
        elif request.POST.get('_method') == 'DELETE':
            user_id = User.objects.get(username=request.POST.get('username')).id
            post_id = request.POST.get('post_id')
            _likes = Likes.objects.get(user_id=user_id, post_id=post_id)
            Post.objects.get(id=post_id).likes_count -= 1
            _likes.delete()
            return JsonResponse({'success': 'Delete likes successfully.'})
        else:
            return JsonResponse({'error': 'Invalid request method.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


def favorites(request):
    if request.method == 'POST':
        if request.POST.get('_method') == 'POST':
            user_id = User.objects.get(username=request.POST.get('username')).id
            post_id = request.POST.get('post_id')
            _favorites = Favorites(user_id=user_id, post_id=post_id)
            _favorites.save()
            Post.objects.get(id=post_id).favorites_count += 1
            return JsonResponse({'success': 'Favorites successfully.'})
        elif request.POST.get('_method') == 'DELETE':
            user_id = User.objects.get(username=request.POST.get('username')).id
            post_id = request.POST.get('post_id')
            _favorites = Favorites.objects.get(user_id=user_id, post_id=post_id)
            Post.objects.get(id=post_id).favorites_count -= 1
            _favorites.delete()
            return JsonResponse({'success': 'Delete favorites successfully.'})
        else:
            return JsonResponse({'error': 'Invalid request method.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


def comments(request):
    if request.method == 'POST':
        user_id = User.objects.get(username=request.POST.get('username')).id
        post_id = request.POST.get('post_id')
        content = request.POST.content
        _comments = Comments(user_id=user_id, post_id=post_id, content=content)
        _comments.save()
        Post.objects.get(id=post_id).comments_count += 1
        return JsonResponse({'success': 'Comments successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


def notification(request):
    if request.method == 'POST':
        user_id = User.objects.get(username=request.POST.get('username')).id
        _type = request.POST.get('type')
        content = request.POST.get('content')
        Notification(user_id=user_id, type=_type, content=content).save()
        return JsonResponse({'success': 'Notification successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
