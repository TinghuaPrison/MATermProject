import time
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.core.files import *
from .models import *


def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        avatar: File = request.FILES.get('avatar')
        bio = request.POST.get('bio', '')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username is already taken.'}, status=400)
        if avatar:
            avatar_path = 'http://39.101.74.64:8000/static/' + username + '_avatar_' + avatar.name
            with open(avatar_path, 'wb+') as f:
                f.write(avatar.read())
        else:
            avatar_path = 'static/default_avatar.png'
        _user = User(username=username, password=make_password(password), avatar=avatar_path, bio=bio)
        _user.save()
        return JsonResponse({'success': 'User registered successfully.'})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'User has not registered yet.'}, status=400)
        else:
            if check_password(password, User.objects.get(username=username).password):
                return JsonResponse({'success': 'User logged in successfully.'})
            else:
                return JsonResponse({'error': 'Password is not correct.'}, status=401)


def user_edit(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        newname = request.POST.get('newname')
        password = request.POST.get('password')
        avatar: File = request.FILES.get('avatar')
        bio = request.POST.get('bio', '')

        if newname != username and User.objects.filter(username=newname).exists():
            return JsonResponse({'error': 'New username already exists.'}, status=400)
        _user = User.objects.get(username=username)
        _user.username = newname
        _user.password = make_password(password)
        _user.bio = bio
        if avatar:
            avatar_path = 'static/' + username + '_avatar_' + avatar.name
            with open(avatar_path, 'wb+') as f:
                f.write(avatar.read())
            _user.avatar = avatar_path
        _user.save()
        return JsonResponse({'success': 'User info modified successfully.'})


def get_all_users(request):
    if request.method == 'POST':
        data = {}
        users = User.objects.values()
        data['user_list'] = list(users)
        return JsonResponse(data, safe=False)


def get_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username).values()
        data = {'user': list(user)}
        return JsonResponse(data, safe=False)


def follow(request):
    if request.method == 'POST':
        follower = request.POST.get('follower')
        followee = request.POST.get('followee')
        Follow(follower=follower, followee=followee).save()
        return JsonResponse({'success': 'Followed successfully.'})


def unfollow(request):
    if request.method == 'POST':
        follower = request.POST.get('follower')
        followee = request.POST.get('followee')
        Follow.objects.get(follower=follower, followee=followee).delete()
        return JsonResponse({'success': 'Unfollowed successfully.'})


def get_followers(request):
    if request.method == 'POST':
        followee = request.POST.get('username')
        data = {}
        follower_list = []
        for i in Follow.objects.filter(followee=followee).all():
            follower_list += list(User.objects.filter(username=i.follower).values())
        data['list'] = follower_list
        return JsonResponse(data)


def get_followees(request):
    if request.method == 'POST':
        follower = request.POST.get('username')
        data = {}
        followee_list = []
        for i in Follow.objects.filter(follower=follower).all():
            followee_list += list(User.objects.filter(username=i.followee).values())
        data['list'] = followee_list
        return JsonResponse(data)


def block(request):
    if request.method == 'POST':
        blocker = request.POST.get('blocker')
        blocked = request.POST.get('blocked')
        Block(blocker=blocker, blocked=blocked).save()
        return JsonResponse({'success': 'Blocked successfully.'})


def unblock(request):
    if request.method == 'POST':
        blocker = request.POST.get('blocker')
        blocked = request.POST.get('blocked')
        Block.objects.get(blocker=blocker, blocked=blocked).delete()
        return JsonResponse({'success': 'Unblocked successfully.'})


def get_blockers(request):
    if request.method == 'POST':
        blocked = request.POST.get('username')
        data = {}
        blocker_list = []
        for i in Block.objects.filter(blocked=blocked).all():
            blocker_list += list(User.objects.filter(username=i.blocker).values())
        data['list'] = blocker_list
        return JsonResponse(data)


def get_blockeds(request):
    if request.method == 'POST':
        blocker = request.POST.get('username')
        data = {}
        blocked_list = []
        for i in Block.objects.filter(blocker=blocker).all():
            blocked_list += list(User.objects.filter(username=i.blocked).values())
        data['list'] = blocked_list
        return JsonResponse(data)


def send_message(request):
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
        return JsonResponse({'success': 'Message sent successfully.'})


def start_session(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        target = request.POST.get('target')
        if Session.objects.filter(username=username, target=target).exists():
            s = Session.objects.get(username=username, target=target)
            s.message_not_checked = 0
            s.save()
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
            return JsonResponse({'success': 'Session created successfully.'}, status=201)


def get_sessions(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        data = {}
        sessions = Session.objects.filter(username=username).values()
        data['list'] = list(sessions)
        return JsonResponse(data)


def post_moment(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        avatar = User.objects.get(username=username).avatar
        _type = request.POST.get('type')
        content = request.POST.get('content')
        media: File = request.FILES.get('media')
        if media:
            save_path = 'http://39.101.74.64:8000/static/' + username + '_post_' + str(int(time.time() * (10 ** 4))) + '_' + media.name
            with open(save_path, 'wb+') as f:
                f.write(media.read())
        else:
            save_path = ''
        location = request.POST.get('location')
        Moment(username=username, avatar=avatar, type=_type, content=content, media=save_path, location=location).save()
        return JsonResponse({'success': 'Post successfully.'})


def get_moments(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if request.POST.get('sorted_by') == 'new':
            data = {}
            moments = Moment.objects.all().values()
            moments_list = sorted(list(moments), key=lambda x: x['c_time'], reverse=True)
            for i in moments_list:
                if Block.objects.filter(blocker=username, blocked=i['username']):
                    moments_list.remove(i)
            data['list'] = moments_list
            return JsonResponse(data)
        elif request.POST.get('sorted_by') == 'hot':
            data = {}
            moments = Moment.objects.all().values()
            moments_list = sorted(list(moments),
                                  key=lambda x: x['likes_count'] + x['favorites_count'] + x['comments_count'])
            for i in moments_list:
                if Block.objects.filter(blocker=username, blocked=i['username']):
                    moments_list.remove(i)
            data['list'] = moments_list
            return JsonResponse(data)
        elif request.POST.get('sorted_by') == 'follow':
            data = {}
            followee = Follow.objects.get(follower=username)
            moments = Moment.objects.filter(username=followee.followee).values()
            moments_list = sorted(list(moments), key=lambda x: x['c_time'])
            for i in moments_list:
                if Block.objects.filter(blocker=username, blocked=i['username']):
                    moments_list.remove(i)
            data['list'] = moments_list
            return JsonResponse(data)
        elif request.POST.get('sorted_by') == 'type':
            _type = request.POST.get('type')
            data = {}
            moments = Moment.objects.filter(type=_type).values()
            moments_list = sorted(list(moments), key=lambda x: x['c_time'])
            for i in moments_list:
                if Block.objects.filter(blocker=username, blocked=i['username']):
                    moments_list.remove(i)
            data['list'] = moments_list
            return JsonResponse(data)


def like_moment(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        moment_id = request.POST.get('moment_id')
        Like(username=username, moment_id=moment_id).save()
        moment = Moment.objects.get(id=moment_id)
        moment.likes_count += 1
        moment.save()
        return JsonResponse({'success': 'Like successfully.'})


def unlike_moment(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        moment_id = request.POST.get('moment_id')
        moment = Moment.objects.get(id=moment_id)
        moment.likes_count -= 1
        moment.save()
        Like.objects.get(username=username, moment_id=moment_id).delete()
        return JsonResponse({'success': 'Unlike successfully.'})


def get_like_moments(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        data = {}
        moment_list = []
        for i in Like.objects.filter(username=username).all():
            moment_list += list(Moment.objects.filter(id=i.moment_id).values())
        moment_list.reverse()
        data['list'] = moment_list
        return JsonResponse(data)


def get_moment_likes(request):
    if request.method == 'POST':
        moment_id = request.POST.get('moment_id')
        data = {}
        user_list = []
        for i in Like.objects.filter(moment_id=moment_id).all():
            user_list += list(User.objects.filter(username=i.username).values())
        data['list'] = user_list
        return JsonResponse(data)


def favorite_moment(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        moment_id = request.POST.get('moment_id')
        Favorite(username=username, moment_id=moment_id).save()
        moment = Moment.objects.get(id=moment_id)
        moment.favorites_count += 1
        moment.save()
        return JsonResponse({'success': 'Favorite successfully.'})


def unfavorite_moment(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        moment_id = request.POST.get('moment_id')
        moment = Moment.objects.get(id=moment_id)
        moment.favorites_count -= 1
        moment.save()
        Favorite.objects.filter(username=username, moment_id=moment_id).delete()
        return JsonResponse({'success': 'Unfavorite successfully.'})


def get_favorite_moments(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        data = {}
        moment_list = []
        for i in Favorite.objects.filter(username=username).all():
            moment_list += list(Moment.objects.filter(id=i.moment_id).values())
        data['list'] = moment_list
        return JsonResponse(data)


def get_moment_favorites(request):
    if request.method == 'POST':
        moment_id = request.POST.get('moment_id')
        data = {}
        user_list = []
        for i in Favorite.objects.filter(moment_id=moment_id).all():
            user_list += list(User.objects.filter(username=i.username).values())
        data['list'] = user_list
        return JsonResponse(data)


def comment_moment(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        moment_id = request.POST.get('moment_id')
        content = request.POST.get('content')
        Comment(username=username, moment_id=moment_id, content=content).save()
        moment = Moment.objects.get(id=moment_id)
        moment.comments_count += 1
        moment.save()
        return JsonResponse({'success': 'Comment successfully.'})


def get_comment_moments(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        data = {}
        moment_list = []
        for i in Comment.objects.filter(username=username).all():
            l = list(Moment.objects.filter(id=i.moment_id).values())
            set1 = {tuple(d.items()) for d in moment_list}
            set2 = {tuple(d.items()) for d in l}
            union_set = set1.union(set2)
            moment_list = [dict(item) for item in union_set]
        data['list'] = moment_list
        return JsonResponse(data)


def get_moment_comments(request):
    if request.method == 'POST':
        moment_id = request.POST('moment_id')
        data = {}
        comment_list = list(Comment.objects.filter(moment_id=moment_id).values())
        data['list'] = comment_list
        return JsonResponse(data)


def post_notification(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        title = request.POST.get('title')
        content = request.POST.get('content')
        Notification(username=username, title=title, content=content).save()
        return JsonResponse({'success': 'Notification successfully.'})


def get_notifications(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        data = {}
        notifications = Notification.objects.filter(username=username).values()
        data['list'] = list(notifications)
        return JsonResponse(data)
