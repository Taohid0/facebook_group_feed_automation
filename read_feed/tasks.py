from .models import Comment, CommentPhoto, Post, PostPhoto, FBUser
from django.utils import timezone


def save_post(post_data):
    message = post_data.get("message")
    user = post_data.get("from")
    post_id = post_data.get("id")
    link = post_data.get("link")
    created_time = post_data.get("created_time")
    updated_time = post_data.get("updated_time")

    if not message:
        return

    if not user:
        return

    user_id = user.get("id")
    name = user.get("name")

    fbuser_object = FBUser.objects.filter(user_id=user_id).first()
    if not fbuser_object:
        fbuser_object = FBUser(user_id=user_id, user_name=name)
        fbuser_object.save()

    post_object = Post.objects.filter(post_id=post_id).first()

    if post_object and post_object.updated_time != updated_time:
        post_object.message = message
        post_object.link = link
        post_object.updated_time = updated_time
        post_object.updated_at = timezone.now()
        post_object.save()
    elif not post_object:
        if not updated_time:
            updated_time = created_time
        post_object = Post(fbuser=fbuser_object, post_id=post_id, message=message, post_link=link, created_time=created_time,
                           updated_time=updated_time)
        post_object.save()
        return post_object
