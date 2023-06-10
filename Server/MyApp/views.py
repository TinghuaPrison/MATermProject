import time
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.core.files import *
from django.core import serializers
from django.forms.models import model_to_dict
from .models import *
from django.db.models import Q


def user_register(request):
    if request.method == 'POST':
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


def edit_avatar(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_avatar: File = request.FILES.get('new_avatar')
        if new_avatar:
            avatar_path = 'static/' + username + '_avatar_' + str(int(time.time() * (10 ** 4))) + '_' + new_avatar.name
        else:
            avatar_path = 'static/default_avatar.png'
        with open(avatar_path, 'wb+') as f:
            f.write(new_avatar.read)
        _user = User.objects.get(username=username)
        _user.avatar = avatar_path
        _user.save()
        return JsonResponse({'success': 'Avatar edit successfully.'})


def edit_username(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_username = request.POST.get('new_username')
        _user = User.objects.get(username=username)
        _user.username = new_username
        _user.save()
        return JsonResponse({'success': 'Username edit successfully.'})


def edit_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        _user = User.objects.get(username=username)
        _user.password = make_password(new_password)
        _user.save()
        return JsonResponse({'success': 'Password edit successfully.'})


def edit_bio(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_bio = request.POST.get('new_bio')
        _user = User.objects.get(username=username)
        _user.bio = new_bio
        _user.save()
        return JsonResponse({'success': 'Bio edit successfully.'})


def get_all_users(request):
    if request.method == 'POST':
        data = {}
        users = User.objects.values()
        data['list'] = list(users)
        return JsonResponse(data, safe=False)


def get_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username).values()
        data = {'list': list(user)}
        return JsonResponse(data, safe=False)


def follow(request):
    if request.method == 'POST':
        follower_username = request.POST.get('follower')
        followee_username = request.POST.get('followee')
        follower = User.objects.get(username=follower_username)
        followee = User.objects.get(username=followee_username)
        Follow.objects.create(follower=follower, followee=followee)
        return JsonResponse({'success': 'Followed successfully.'})


def unfollow(request):
    if request.method == 'POST':
        follower_username = request.POST.get('follower')
        followee_username = request.POST.get('followee')
        follower = User.objects.get(username=follower_username)
        followee = User.objects.get(username=followee_username)
        Follow.objects.get(follower=follower, followee=followee).delete()
        return JsonResponse({'success': 'Unfollowed successfully.'})


def get_followers(request):
    if request.method == 'POST':
        followee_username = request.POST.get('username')
        followee = User.objects.get(username=followee_username)
        followers = Follow.objects.filter(followee=followee)
        follower_list = []
        for follower in followers:
            follower_dict = model_to_dict(follower.follower)
            follower_list.append(follower_dict)
        data = {
            'list': follower_list
        }
        return JsonResponse(data)


def get_followees(request):
    if request.method == 'POST':
        follower_username = request.POST.get('username')
        follower = User.objects.get(username=follower_username)
        followees = Follow.objects.filter(follower=follower)
        followee_list = []
        for followee in followees:
            followee_dict = model_to_dict(followee.followee)
            followee_list.append(followee_dict)
        data = {
            'list': followee_list
        }
        return JsonResponse(data)



def block(request):
    if request.method == 'POST':
        blocker_username = request.POST.get('blocker')
        blocked_username = request.POST.get('blocked')
        blocker = User.objects.get(username=blocker_username)
        blocked = User.objects.get(username=blocked_username)
        Block.objects.create(blocker=blocker, blocked=blocked)
        return JsonResponse({'success': 'Blocked successfully.'})


def unblock(request):
    if request.method == 'POST':
        blocker_username = request.POST.get('blocker')
        blocked_username = request.POST.get('blocked')
        blocker = User.objects.get(username=blocker_username)
        blocked = User.objects.get(username=blocked_username)
        Block.objects.get(blocker=blocker, blocked=blocked).delete()
        return JsonResponse({'success': 'Unblocked successfully.'})


def get_blockers(request):
    if request.method == 'POST':
        blocked_username = request.POST.get('username')
        blocked = User.objects.get(username=blocked_username)
        blockers = Block.objects.filter(blocked=blocked)
        data = {
            'list': [serializers.serialize('json', [blocker.blocker]) for blocker in blockers]
        }
        return JsonResponse(data)


def get_blockeds(request):
    if request.method == 'POST':
        blocker_username = request.POST.get('username')
        blocker = User.objects.get(username=blocker_username)
        blockeds = Block.objects.filter(blocker=blocker)
        data = {
            'list': [serializers.serialize('json', [blocked.blocked]) for blocked in blockeds]
        }
        return JsonResponse(data)


def send_message(request):
    if request.method == 'POST':
        sender_username = request.POST.get('sender')
        receiver_username = request.POST.get('receiver')
        content = request.POST.get('content')
        sender = User.objects.get(username=sender_username)
        receiver = User.objects.get(username=receiver_username)
        session = Session.objects.get(user=sender, target=receiver)
        Message.objects.create(session=session, sender=sender, receiver=receiver, content=content)
        session = Session.objects.get(user=receiver, target=sender)
        Message.objects.create(session=session, sender=sender, receiver=receiver, content=content)

        s_sender = Session.objects.get(user=sender, target=receiver)
        s_sender.message_cnt += 1
        s_sender.last_message = content
        s_sender.save()

        s_receiver = Session.objects.get(user=receiver, target=sender)
        s_receiver.message_cnt += 1
        s_receiver.message_not_checked += 1
        s_receiver.last_message = content
        s_receiver.save()
        Notification.objects.create(
            user=receiver,
            title="New Message",
            content=f"You have received a new message from {sender_username}: {content}"
        )
        return JsonResponse({'success': 'Message sent successfully.'})


def start_session(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        target_username = request.POST.get('target')
        user = User.objects.get(username=username)
        target = User.objects.get(username=target_username)

        if Session.objects.filter(user=user, target=target).exists():
            s = Session.objects.get(user=user, target=target)
            s.message_not_checked = 0
            s.save()
            messages = Message.objects.filter(session=s).order_by('-c_time').reverse()
            messages_list = []
            for message in messages:
                message_dict = model_to_dict(message)
                message_dict['session'] = model_to_dict(message.session)
                message_dict['sender'] = model_to_dict(message.sender)
                message_dict['receiver'] = model_to_dict(message.receiver)
                message_dict['c_time'] = message.c_time.strftime("%H:%M:%S")
                if message.sender.username == username:
                    message_dict['side'] = 1
                else:
                    message_dict['side'] = 0
                messages_list.append(message_dict)
            data = {
                'list': messages_list
            }
            return JsonResponse(data)
        else:
            Session.objects.create(user=user, target=target)
            Session.objects.create(user=target, target=user)
            return JsonResponse({'success': 'Session created successfully.'}, status=201)


def get_sessions(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        if Session.objects.filter(user=user).exists():
            sessions = Session.objects.filter(user=user)
            session_list = []
            for session in sessions:
                session_dict = model_to_dict(session)
                session_dict['user'] = model_to_dict(session.user)
                session_dict['target'] = model_to_dict(session.target)
                session_dict['c_time'] = session.c_time.strftime("%H:%M:%S")
                session_list.append(session_dict)
            data = {
                'list': session_list
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'success': ''}, status=201)


def post_moment(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        _type = request.POST.get('type')
        content = request.POST.get('content')
        media: File = request.FILES.get('media')
        location = request.POST.get('location')
        save_path = 'null'
        _location = 'null'
        __type = '未分类'
        if media:
            save_path = 'static/' + username + '_post_' + str(int(time.time() * (10 ** 4))) + '_' + media.name
            with open(save_path, 'wb+') as f:
                f.write(media.read())
        if location:
            _location = location
        if _type:
            __type = _type
        Moment.objects.create(user=user, type=__type, content=content, media=save_path, location=_location)
        return JsonResponse({'success': 'Post successfully.'})


def get_moments(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            blocked_users = [block.blocked for block in Block.objects.filter(blocker=user)]

            if request.POST.get('sorted_by') == 'user':
                moments = Moment.objects.filter(user=user).exclude(user__in=blocked_users).order_by('-c_time')
            elif request.POST.get('sorted_by') == 'new':
                moments = Moment.objects.all().exclude(user__in=blocked_users).order_by('-c_time')
            elif request.POST.get('sorted_by') == 'hot':
                moments = Moment.objects.all().exclude(user__in=blocked_users)
                moments = reversed(sorted(moments, key=lambda x: x.likes_count + x.favorites_count + x.comments_count))
            elif request.POST.get('sorted_by') == 'follow':
                followees = [follow.followee for follow in Follow.objects.filter(follower=user)]
                moments = Moment.objects.filter(user__in=followees).exclude(user__in=blocked_users).order_by('-c_time')
            elif request.POST.get('sorted_by') == 'type':
                _type = request.POST.get('type')
                moments = Moment.objects.filter(type=_type).exclude(user__in=blocked_users).order_by('-c_time')

            moments_list = []
            for moment in moments:
                moment_dict = model_to_dict(moment)
                moment_dict['user'] = model_to_dict(moment.user)
                moment_dict['c_time'] = moment.c_time.strftime('%Y-%m-%d %H:%M:%S')
                flag = 0
                if Follow.objects.filter(follower=user, followee=moment.user).exists():
                    flag = 1
                moment_dict['followed'] = flag
                flag = 0
                if Like.objects.filter(user=user, moment=moment).exists():
                    flag = 1
                moment_dict['liked'] = flag
                flag = 0
                if Favorite.objects.filter(user=user, moment=moment).exists():
                    flag = 1
                moment_dict['favorited'] = flag
                moments_list.append(moment_dict)

            data = {
                'list': moments_list
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'success': ''}, status=201)


def search_moment(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        query: str = request.POST.get('query')
        keywords = query.split()
        q_objects = Q()
        for keyword in keywords:
            q_objects &= (Q(content__icontains=keyword)
                          | Q(user__username__icontains=keyword)
                          | Q(type__icontains=keyword))
        moments = Moment.objects.filter(q_objects)
        moments_list = []
        for moment in moments:
            moment_dict = model_to_dict(moment)
            moment_dict['user'] = model_to_dict(moment.user)
            moment_dict['c_time'] = moment.c_time.strftime('%Y-%m-%d %H:%M:%S')
            flag = 0
            if Follow.objects.filter(follower=user, followee=moment.user).exists():
                flag = 1
            moment_dict['followed'] = flag
            flag = 0
            if Like.objects.filter(user=user, moment=moment).exists():
                flag = 1
            moment_dict['liked'] = flag
            flag = 0
            if Favorite.objects.filter(user=user, moment=moment).exists():
                flag = 1
            moment_dict['favorited'] = flag
            moments_list.append(moment_dict)

        data = {
            'list': moments_list
        }
        return JsonResponse(data)


def like_moment(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        moment_id = request.POST.get('moment_id')
        moment = Moment.objects.get(id=moment_id)
        Like.objects.create(user=user, moment=moment)
        moment.likes_count += 1
        moment.save()
        Notification.objects.create(
            user=moment.user,
            title="Moment Liked",
            content=f"{username} liked your moment."
        )
        return JsonResponse({'success': 'Like successfully.'})


def unlike_moment(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        moment_id = request.POST.get('moment_id')
        moment = Moment.objects.get(id=moment_id)
        moment.likes_count -= 1
        moment.save()
        Like.objects.get(user=user, moment=moment).delete()
        return JsonResponse({'success': 'Unlike successfully.'})


def get_like_moments(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        moments = Moment.objects.filter(like__user=user)
        data = {
            'list': [serializers.serialize('json', [moment]) for moment in moments]
        }
        return JsonResponse(data)


def get_moment_likes(request):
    if request.method == 'POST':
        moment_id = request.POST.get('moment_id')
        moment = Moment.objects.get(id=moment_id)
        users = User.objects.filter(like__moment=moment)
        data = {
            'list': [serializers.serialize('json', [user]) for user in users]
        }
        return JsonResponse(data)


def favorite_moment(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        moment_id = request.POST.get('moment_id')
        moment = Moment.objects.get(id=moment_id)
        Favorite.objects.create(user=user, moment=moment)
        moment.favorites_count += 1
        moment.save()
        Notification.objects.create(
            user=moment.user,
            title="Moment Favorited",
            content=f"{username} favorited your moment."
        )
        return JsonResponse({'success': 'Favorite successfully.'})


def unfavorite_moment(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        moment_id = request.POST.get('moment_id')
        moment = Moment.objects.get(id=moment_id)
        moment.favorites_count -= 1
        moment.save()
        Favorite.objects.get(user=user, moment=moment).delete()
        return JsonResponse({'success': 'Unfavorite successfully.'})


def get_favorite_moments(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        moments = Moment.objects.filter(favorites__user=user)
        moments_list = []
        for moment in moments:
            moment_dict = model_to_dict(moment)
            moment_dict['user'] = model_to_dict(moment.user)
            moment_dict['c_time'] = moment.c_time.strftime('%Y-%m-%d %H:%M:%S')
            flag = 0
            if Follow.objects.filter(follower=user, followee=moment.user).exists():
                flag = 1
            moment_dict['followed'] = flag
            flag = 0
            if Like.objects.filter(user=user, moment=moment).exists():
                flag = 1
            moment_dict['liked'] = flag
            flag = 0
            if Favorite.objects.filter(user=user, moment=moment).exists():
                flag = 1
            moment_dict['favorited'] = flag
            moments_list.append(moment_dict)

        data = {
            'list': moments_list
        }
        return JsonResponse(data)


def get_moment_favorites(request):
    if request.method == 'POST':
        moment_id = request.POST.get('moment_id')
        moment = Moment.objects.get(id=moment_id)
        users = User.objects.filter(favorite__moment=moment)
        data = {
            'list': [serializers.serialize('json', [user]) for user in users]
        }
        return JsonResponse(data)


def comment_moment(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        moment_id = request.POST.get('moment_id')
        moment = Moment.objects.get(id=moment_id)
        content = request.POST.get('content')
        Comment.objects.create(user=user, moment=moment, content=content)
        moment.comments_count += 1
        moment.save()
        Notification.objects.create(
            user=moment.user,
            title="Moment Commented",
            content=f"{username} commented on your moment: {content}"
        )
        return JsonResponse({'success': 'Comment successfully.'})


def get_comment_moments(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.get(username=username)
        moments = Moment.objects.filter(comment__user=user)
        data = {
            'list': [serializers.serialize('json', [moment]) for moment in moments]
        }
        return JsonResponse(data)


def get_moment_comments(request):
    if request.method == 'POST':
        moment_id = request.POST.get('moment_id')
        moment = Moment.objects.get(id=moment_id)
        comments = Comment.objects.filter(moment=moment).order_by('-c_time')
        comments_list = []
        for comment in comments:
            comment_dict = model_to_dict(comment)
            comment_dict['user'] = model_to_dict(comment.user)
            comment_dict['c_time'] = comment.c_time.strftime('%Y-%m-%d %H:%M:%S')
            comments_list.append(comment_dict)
        data = {
            'list': comments_list
        }
        return JsonResponse(data)


def get_notifications(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if Notification.objects.filter(user=user).exists():
                notifications = Notification.objects.filter(user=user).order_by('-c_time')
                notifications_list = [{
                    'title': notification.title,
                    'content': notification.content,
                    'checked': notification.checked,
                    'c_time': notification.c_time.strftime('%H:%M:%S')
                } for notification in notifications]
                for notification in notifications:
                    notification.checked = True
                    notification.save()
                return JsonResponse({'list': notifications_list})
            else:
                return JsonResponse({'success': ''}, status=201)
        else:
            return JsonResponse({'success': ''}, status=201)

