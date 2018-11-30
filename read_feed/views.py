import requests
import json
from pprint import pprint

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .tasks import *

USER_ACCESS_TOKEN = 'EAAFIGgZC66zIBAPbArATdaTpA1DM8R3L48NfbKYLPrTi7bqohY4G4ARi3irNYdYnr553UZBTxAdN1NUjt9dytINcIsH4WkvWunCXM9ZC2QLzjzCnxP5ooUkZAYOqDc5gFhrXrVdD9eh7L4HUDkEY3CxW76E0UyabPN6walnouZCVUrUO6WA0qdxXSQg5gwlMZD'
parameters = {"access_token": USER_ACCESS_TOKEN}
GROUP_ID = '1251085764934174'
group_url = 'https://graph.facebook.com/{}/feed/?fields=id,from,message,created_time, updated_time, link,attachments,comments'.format(
    GROUP_ID)


@api_view(["GET"])
def index(request):
    # response = requests.get(url=group_url, params=parameters)
    # data_dict = json.loads(response.content.decode("utf-8"))

    # data = data_dict.get("data")
    # pprint(data)
    # test.delay(data)

    # for single_post in data:
    #     post_id = save_post.delay(single_post)
    #
    #     if not post_id:
    #         continue
    #
    #     comments = single_post.get("comments")
    #     if comments:
    #         save_comments.delay(comments, post_id)
    #
    #     if single_post.get("attachments"):
    #         save_post_photos.delay(single_post.get("attachments"), post_id)

    return Response({"status": True})
