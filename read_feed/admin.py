from django.contrib import admin

from .models import Post, PostPhoto, Comment,CommentPhoto, FBUser


admin.site.register(FBUser)
admin.site.register(Post)
admin.site.register(PostPhoto)
admin.site.register(Comment)
admin.site.register(CommentPhoto)
