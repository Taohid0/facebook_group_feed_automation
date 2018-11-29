import requests
import json
from pprint import pprint

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .tasks import *

USER_ACCESS_TOKEN = 'EAAFIGgZC66zIBAHB71ut33RqQBW6VdPPMNn52IXNs79FNZAReS4JPlhIh0062i5gvOM9sGEnrj3S2eyUZCrAzvv8E7lyPAIbUkxfBDrVRrpUJ2ACmxj9p0qAY2ZA69ZA0ajRzfdkDlkZCO3dDZAc89oJGioSVf4ZAiUVelUpIcXwlJh374m7XZCOd9tiQts13HgMZD'
parameters = {"access_token": USER_ACCESS_TOKEN}
GROUP_ID = '1251085764934174'
group_url = 'https://graph.facebook.com/{}/feed/?fields=id,from,message,created_time, updated_time, link,attachments,comments'.format(
    GROUP_ID)


@api_view(["GET"])
def index(request):
    response = requests.get(url=group_url, params=parameters)
    data_dict = json.loads(response.content.decode("utf-8"))

    data = data_dict.get("data")
    pprint(data)

    for single_post in data:
        post = save_post(single_post)

        if not post:
            continue

        comments = single_post.get("comments")
        if comments:
            save_comments(comments, post.id)

        if single_post.get("attachments"):
            save_post_photos(single_post.get("attachments"), post.id)

        elif single_post.get("subattachments"):
            save_post_photos(single_post.get("subattachments"), post.id) # single image problem

    return Response({"status": True})
