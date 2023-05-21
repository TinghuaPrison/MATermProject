import time
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.core.files import *
from .models import *
from os import remove


def user(request):
    if request.method == 'POST':
        if request.POST.get('_method') == 'register':
            username = request.POST.get('username')
            password = request.POST.get('password')
            avatar: File = request.FILES.get('avatar')
            bio = request.POST.get('bio', '')

            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username is already taken.'}, status=400)
            if avatar:
                avatar_path = 'static/' + username + '_avatar_' + avatar.name
                with open(avatar_path, 'wb+') as f:
                    f.write(avatar.read())
            else:
                avatar_path = 'static/default_avatar.png'
            _user = User(username=username, password=password, avatar=avatar_path, bio=bio)
            _user.save()
            return JsonResponse({'success': 'User registered successfully.'})
        elif request.POST.get('_method') == 'login':
            username = request.POST.get('username')
            password = request.POST.get('password')

            if not User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'User has not registered yet.'}, status=400)
            else:
                if check_password(password, User.objects.get(username=username).password):
                    return JsonResponse({'success': 'User logged in successfully.'})
                else:
                    return JsonResponse({'error': 'Password is not correct.'}, status=400)
        elif request.POST.get('_method') == 'edit_user':
            username = request.POST.get('username')
            new_username = request.POST.get('new_username')
            password = request.POST.get('password')
            avatar: File = request.FILES.get('avatar')
            bio = request.POST.get('bio', '')

            if new_username != username and User.objects.filter(username=new_username).exists():
                return JsonResponse({'error': 'New username already exists.'}, status=400)
            _user = User.objects.get(username=username)
            _user.username = new_username
            _user.password = make_password(password)
            _user.bio = bio
            if avatar:
                avatar_path = user.avatar
                remove(avatar_path)
                avatar_path = 'static/images/' + username + '_avatar_' + avatar.name
                with open(avatar_path, 'wb+') as f:
                    f.write(avatar.read())
                user.avatar = avatar_path
            _user.save()
            return JsonResponse({'success': 'User info modified successfully.'})
        elif request.POST.get('_method') == 'get_all_users':
            data = {}
            users = User.objects.values()
            data['list'] = list(users)
            return JsonResponse(data)
        elif request.POST.get('_method') == 'get_user':
            username = request.POST.get('username')
            users = User.objects.filter(username=username).values()
            data = {'list': list(users)}
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Invalid request method.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


def follow(request):
    if request.method == 'POST':
        if request.POST.get('_method') == 'PUT':
            follower = request.POST.get('follower')
            followee = request.POST.get('followee')
            Follow(follower=follower, followee=followee).save()
        elif request.POST.get('_method') == 'DELETE':
            follower = request.POST.get('follower')
            followee = request.POST.get('followee')
            Follow.objects.get(follower=follower, followee=followee).delete()
        elif request.POST.get('_method') == 'get_follower_list':
            followee = request.POST.get('followee')
            data = {}
            follower = Follow.objects.filter(followee=followee).values()
            data['list'] = list(follower)
            return JsonResponse(data)
        elif request.POST.get('_method') == 'get_followee_list':
            follower = request.POST.get('follower')
            data = {}
            followee = Follow.objects.filter(follower=follower).values()
            data['list'] = list(followee)
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Invalid request method.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


def block(request):
    if request.method == 'POST':
        if request.POST.get('_method') == 'PUT':
            blocker = request.POST.get('blocker')
            blocked = request.POST.get('blocked')
            Block(blocker=blocker, blocked=blocked).save()
        elif request.POST.get('_method') == 'DELETE':
            blocker = request.POST.get('blocker')
            blocked = request.POST.get('blocked')
            Block.objects.get(blocker=blocker, blocked=blocked).delete()
        elif request.POST.get('_method') == 'get_blocker_list':
            blocked = request.POST.get('blocked')
            data = {}
            blocker = Block.objects.filter(blocked=blocked).values()
            data['list'] = list(blocker)
            return JsonResponse(data)
        elif request.POST.get('_method') == 'get_blocked_list':
            blocker = request.POST.get('blocker')
            data = {}
            blocked = Follow.objects.filter(blocker=blocker).values()
            data['list'] = list(blocked)
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Invalid request method.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


def message(request):
    if request.method == 'POST':
        sender = request.POST.get('sender')
        receiver = request.POST.get('receiver')
        content = request.POST.get('content')
        Message(sender=sender, receiver=receiver, content=content).save()
        s = Session.objects.get(username=sender, target=receiver)
        s.message_cnt += 1
        s.last_message = content
        s.save()
        s = Session.objects.get(username=receiver, target=sender)
        s.message_cnt += 1
        s.message_not_checked += 1
        s.last_message = content
        s.save()
        return JsonResponse({'success': 'Message send successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


def session(request):
    if request.method == 'POST':
        if request.POST.get('_method') == 'start':
            username = request.POST.get('username')
            target = request.POST.get('target')
            if Session.objects.filter(username=username, target=target).exists():
                Session.objects.get(username=username, target=target).message_not_checked = 0
                data = {}
                sent = Message.objects.filter(sender=username, receiver=target).values()
                received = Message.objects.filter(sender=target, receiver=username).values()
                messages = list(sent) + list(received)
                sorted_messages = sorted(messages, key=lambda x: x['c_time'])
                data['message_list'] = sorted_messages
                return JsonResponse(data)
            else:
                Session(username=username, target=target).save()
                Session(username=target, target=username).save()
                return JsonResponse({''}, status=201)
        elif request.POST.get('_method') == 'get_session_list':
            username = request.POST.get('username')
            data = {}
            sessions = Session.objects.filter(username=username).values()
            data['list'] = list(sessions)
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Invalid request method.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


def post(request):
    if request.method == 'POST':
        if request.POST.get('_method') == 'GET':
            if request.POST.get('sorted_by') == 'new':
                data = {}
                posts = Post.objects.all().values()
                posts_list = sorted(list(posts), key=lambda x: x['c_time'])
                data['list'] = posts_list
                return JsonResponse(data)
            elif request.POST.get('sorted_by') == 'hot':
                data = {}
                posts = Post.objects.all().values()
                posts_list = sorted(list(posts),
                                    key=lambda x: x['likes_count'] + x['favorites_count'] + x['comments_count'])
                data['list'] = posts_list
                return JsonResponse(data)
            elif request.POST.get('sorted_by') == 'follow':
                follower = request.POST.get('follower')
                data = {}
                followee = Follow.objects.get(follower=follower)
                posts = Post.objects.filter(username=followee.followee)
                posts_list = sorted(list(posts), key=lambda x: x['c_time'])
                data['list'] = posts_list
                return JsonResponse(data)
            elif request.POST.get('sorted_by') == 'type':
                _type = request.POST.get('type')
                data = {}
                posts = Post.objects.filter(type=_type).values()
                posts_list = sorted(list(posts), key=lambda x: x['c_time'])
                data['list'] = posts_list
                return JsonResponse(data)
        elif request.POST.get('_method') == 'POST':
            username = request.POST.get('username')
            _type = request.POST.get('type')
            content = request.POST.get('content')
            medias = request.FILES.getlist('media')
            media = ''
            for fm in medias:
                save_path = 'static/' + username + '_post_' + str(time.time()) + '_' + fm.name
                with open(save_path, 'wb+') as f:
                    f.write(fm.read())
                media += save_path + '#'
            location = request.POST.get('location')
            Post(username=username, type=_type, content=content, media=media, location=location).save()
        return JsonResponse({'success': 'Post successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


def likes(request):
    if request.method == 'POST':
        if request.POST.get('_method') == 'GET':
            username = request.POST.get('username')
            data = {}
            all_likes = Likes.objects.filter(username=username).values()
            data['list'] = list(all_likes)
            return JsonResponse(data)
        elif request.POST.get('_method') == 'POST':
            username = request.POST.get('username')
            post_id = request.POST.get('post_id')
            Likes(username=username, post_id=post_id).save()
            _post = Post.objects.get(id=post_id)
            _post.likes_count += 1
            _post.save()
        elif request.POST.get('_method') == 'DELETE':
            username = request.POST.get('username')
            post_id = request.POST.get('post_id')
            _post = Post.objects.get(id=post_id)
            _post.likes_count -= 1
            _post.save()
            Likes(username=username, post_id=post_id).delete()
            return JsonResponse({'success': 'Delete likes successfully.'})
        else:
            return JsonResponse({'error': 'Invalid request method.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


def favorites(request):
    if request.method == 'POST':
        if request.POST.get('_method') == 'GET':
            username = request.POST.get('username')
            data = {}
            all_favorites = Favorites.objects.filter(username=username).values()
            data['list'] = list(all_favorites)
            return JsonResponse(data)
        elif request.POST.get('_method') == 'POST':
            username = request.POST.get('username')
            post_id = request.POST.get('post_id')
            Favorites(username=username, post_id=post_id).save()
            _post = Post.objects.get(id=post_id)
            _post.favorites_count += 1
            _post.save()
        elif request.POST.get('_method') == 'DELETE':
            username = request.POST.get('username')
            post_id = request.POST.get('post_id')
            _post = Post.objects.get(id=post_id)
            _post.favorites_count -= 1
            _post.save()
            Favorites(username=username, post_id=post_id).delete()
            return JsonResponse({'success': 'Delete favorites successfully.'})
        else:
            return JsonResponse({'error': 'Invalid request method.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


def comments(request):
    if request.method == 'POST':
        if request.POST.get('_method') == 'GET':
            username = request.POST.get('username')
            data = {}
            all_comments = Comments.objects.filter(username=username).values()
            data['list'] = list(all_comments)
            return JsonResponse(data)
        elif request.POST.get('_method') == 'POST':
            username = request.POST.get('username')
            post_id = request.POST.get('post_id')
            content = request.POST.get('content')
            Comments(username=username, post_id=post_id, content=content).save()
            _post = Post.objects.get(id=post_id)
            _post.comments_count += 1
            _post.save()
        elif request.POST.get('_method') == 'DELETE':
            username = request.POST.get('username')
            post_id = request.POST.get('post_id')
            _post = Post.objects.get(id=post_id)
            _post.comments_count -= 1
            _post.save()
            Comments(username=username, post_id=post_id).delete()
            return JsonResponse({'success': 'Delete favorites successfully.'})
        else:
            return JsonResponse({'error': 'Invalid request method.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


def notification(request):
    if request.method == 'POST':
        if request.POST.get('_method') == 'GET':
            username = request.POST.get('username')
            data = {}
            notifications = Notification.objects.filter(username=username).values()
            data['list'] = list(notifications)
            return JsonResponse(data)
        elif request.POST.get('_method') == 'POST':
            username = request.POST.get('username')
            title = request.POST.get('title')
            content = request.POST.get('content')
            Notification(username=username, title=title, content=content).save()
            return JsonResponse({'success': 'Notification successfully.'})
        else:
            return JsonResponse({'error': 'Invalid request method.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
