from django.db import models


class Dag(models.Model):
    name = models.CharField(max_length=12)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)


class Tweet(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.TextField()
    photo = models.URLField(max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'[{self.id}][{self.author.username}] {self.text}'


class Follow(models.Model):
    # User(username=Саша, follows=[Саша->Миша], followers=[])
    # related_name обратная связь
    follower = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='follows')
    # User(username=Миша, follows=[], followers=[Саша->Миша])
    follows = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='followers')
    followed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower.username} -> {self.follows.username}'

