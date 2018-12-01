from __future__ import absolute_import, unicode_literals
from pprint import pprint
import json

import requests
from io import BytesIO

from django.utils import timezone
from django.core import files

from celery import shared_task

from .models import Comment, CommentPhoto, Post, PostPhoto, FBUser




@shared_task
def start_saving_process():
    response = requests.get(url=group_url, params=parameters)
    data_dict = json.loads(response.content.decode("utf-8"))

    data = data_dict.get("data")
    # pprint(data)

    for single_post in data:
        post_id = save_post(single_post)

        if not post_id:
            continue

        comments = single_post.get("comments")
        if comments:
            save_comments(comments, post_id)

        if single_post.get("attachments"):
            save_post_photos(single_post.get("attachments"), post_id)


def save_post(post_data):
    message = post_data.get("message")
    user = post_data.get("from")
    post_id = post_data.get("id")
    link = post_data.get("link")
    created_time = post_data.get("created_time")
    updated_time = post_data.get("updated_time")

    if not message:
        return

    if user:
        user_id = user.get("id")
        name = user.get("name")

        fbuser_object = FBUser.objects.filter(user_id=user_id).first()
        if not fbuser_object:
            fbuser_object = FBUser(user_id=user_id, user_name=name)
            fbuser_object.save()
    else:
        fbuser_object = None

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
        post_object = Post(fbuser=fbuser_object, post_id=post_id, message=message, post_link=link,
                           created_time=created_time,
                           updated_time=updated_time)
        post_object.save()
    return post_object.id


def save_post_photos(attachments, post_id):
    photo_queryset = PostPhoto.objects.filter(post_id=post_id)
    old_photos_name = [i.name for i in photo_queryset]

    photo_links_list = []

    attachment_list = attachments.get("data")

    try:
        for i in attachment_list:
            media = i.get("media")
            if media:
                image = media.get("image")
                if image:
                    src = image.get("src")
                    photo_links_list.append(src)
    except Exception as ex:
        print(ex)

    try:
        for attachment in attachment_list:
            sub_attachments = attachment.get("subattachments")

            if sub_attachments:
                data_list = sub_attachments.get("data")

                if data_list:
                    for data in data_list:
                        media = data.get("media")

                        if media:
                            image = media.get("image")

                            if image:
                                src = image.get("src")
                                photo_links_list.append(src)
    except Exception as ex:
        print(ex)

    new_images_name = list()
    for photo_url in photo_links_list:
        response = requests.get(photo_url)
        splitted_url = photo_url.split("/")
        image_name = max(splitted_url, key=len)
        # print(image_name)

        if response.status_code == requests.codes.ok:
            fp = BytesIO()
            fp.write(response.content)
            file_name = image_name
            file_name = file_name + ".jpg"
            new_images_name.append(image_name)

            if image_name not in old_photos_name:
                post_photo_object = PostPhoto(post_id=post_id)
                post_photo_object.name = image_name
                post_photo_object.photo.save(file_name, files.File(fp))
                post_photo_object.save()

    for i in old_photos_name:
        if i not in new_images_name:
            try:
                image_object = PostPhoto.objects.get(name=i)
                image_object.is_deleted = True
                image_object.save()
            except Exception as ex:
                print(ex)
    print(old_photos_name)


def save_comments(comments, post_id):
    comment_data = comments.get("data")

    post_object = Post.objects.filter(id=post_id).first()

    comment_queryset = Comment.objects.filter(post=post_object)
    comment_queryset.delete()

    for comment in comment_data:
        commenter = comment.get("from")
        if commenter:
            commenter_id = commenter.get("id")
            commenter_name = commenter.get("name")
            user = FBUser.objects.filter(user_id=commenter_id).first()
            if not user:
                user = FBUser(user_id=commenter_id, user_name=commenter_name)
                user.save()
        else:
            user = None

        created_time = comment.get("created_time")
        comment_id = comment.get("id")
        message = comment.get("message")

        if not message:
            continue

        comment_object = Comment(post=post_object, fbuser=user, comment_id=comment_id, message=message,
                                 created_time=created_time,
                                 updated_time=created_time)
        comment_object.save()
