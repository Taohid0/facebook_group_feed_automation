import requests
import json

from rest_framework.decorators import api_view
from rest_framework.response import Response

from pprint import pprint
from .tasks import *

USER_ACCESS_TOKEN = 'EAAFIGgZC66zIBAAiwNPeFW1osV9ZBsJiHcvlJNkityY93kMTEpk67kwrQf2yibVlPPEjhsuNVsZAohzBxk0INUmox0VLh8Ma2AlqPSep2vUcEFNWDrVXxiPqXindIq1DWkwD5fTcirwLKOhZBSHGPlE4PZBCLyaxkA0fjDZA90buVn8OKja2NpGhbq9ZAzv3mdtXclAYFLDiGY1W6O2AoKr'
parameters = {"access_token": USER_ACCESS_TOKEN}
GROUP_ID = '1251085764934174'
group_url = 'https://graph.facebook.com/{}/feed/?fields=id,from,message,created_time, updated_time, link,attachments,comments'.format(
    GROUP_ID)


@api_view(["GET"])
def index(request):
    response = requests.get(url=group_url, params=parameters)
    data_dict = json.loads(response.content.decode("utf-8"))

    data = data_dict.get("data")

    for single_post in data:
        post = save_post(single_post)
        


    return Response({"status": True})
