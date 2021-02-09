from django.contrib.auth.models import AbstractUser
from django.db import models

from django.db.models import constraints, Q, F


class User(AbstractUser):
    
    def __str__(self):       
        return f"{self.username} ({self.id})"

class Post(models.Model):
    post = models.AutoField(primary_key=True)
    user_id =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    username = models.CharField(max_length=255, default='Name')
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(User, default=None, blank=True, related_name="liked")



    def __str__(self):       
        return f"{self.post} : {self.username} ({self.user_id}) \ Date ({self.date}) : text: {self.body}."

# this method will be treated fild
    @property
    def num_likes(self):
        return self.liked.all().count()

    @property
    def likes_list(self):
        return list(self.liked.all().values("id"))


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)
class Like(models.Model):
    user_id =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
    post_id =  models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked_post")
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)

    class Meta:
        # to be unique cuple / To Like only Once.
        unique_together = [['user_id', 'post_id']]

    def __str__(self):
        return f"{self.user_id} ({self.post_id})"


class Follow(models.Model):
    follower_id =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following_id =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_user")
    following_posts = models.ManyToManyField(Post)

    class Meta:
        unique_together = [['follower_id', 'following_id']]
        constraints = [
        # follower_id != following_id
        models.CheckConstraint(check=~Q(follower_id=F('following_id')), name='follower_id_and_following_id_can_not_be_equal')
    ]

    def __str__(self):
        return f"{self.following_id} (Follow By: {self. follower_id }) |||  POSTS: {self.following_posts}"