from django.db import models


class FBUser(models.Model):
    user_id = models.CharField("Facebook user ID", max_length=80, unique=True)
    user_name = models.CharField("User name", max_length=80)
    created_at = models.DateTimeField("Created at", auto_now=True)
    updated_at = models.DateTimeField("Updated at", auto_now_add=True)

    def __str__(self):
        return self.user_name + " : " + self.user_id


class Post(models.Model):
    fbuser = models.ForeignKey(FBUser, verbose_name="Facebook User", on_delete=models.CASCADE)
    post_id = models.CharField("Post ID", max_length=50, unique=True)
    message = models.TextField("Post message", null=True, blank=True)
    post_link = models.URLField(max_length=250, null=True, blank=True)
    created_time = models.DateTimeField("Post creation time")
    updated_time = models.DateTimeField("Post update time")
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.message


class Comment(models.Model):
    post = models.ForeignKey(Post, verbose_name="Post", on_delete=models.CASCADE)
    fbuser = models.ForeignKey(FBUser, verbose_name="Comment by", on_delete=models.CASCADE, null=True, blank=True)
    comment_id = models.CharField(max_length=50)
    message = models.TextField("Message", null=True, blank=True)
    created_time = models.DateTimeField("Comment creation time")
    updated_time = models.DateTimeField("Comment update time")
    created_at = models.DateTimeField("Created at", auto_now=True)  # i need to figure out this difference
    updated_at = models.DateTimeField("Updated at", auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.post.post_id + " " + self.message


class PostPhoto(models.Model):
    post = models.ForeignKey(Post, verbose_name="Post", on_delete=models.CASCADE)
    photo = models.ImageField("Post photo")
    name = models.CharField(max_length=250)
    is_deleted = models.BooleanField(default=False)


class CommentPhoto(models.Model):
    comment = models.ForeignKey(Comment, verbose_name="Comment", on_delete=models.CASCADE)
    photo = models.ImageField("Comment Photo")
    is_deleted = models.BooleanField(default=False)
