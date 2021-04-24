from django.contrib.auth.models import User
from rest_framework import serializers
from tutorial.quickstart.models import Dag, Tweet, Follow
from rest_framework.relations import SlugRelatedField


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'first_name', 'last_name', 'email']
        extra_kwargs = {'url': {'lookup_field': 'username'}}


class DagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dag
        fields = ['url', 'name', 'owner']


class TweetSerializer(serializers.HyperlinkedModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = ['id', 'url', 'text', 'photo', 'author', 'created']


class FollowSerializer(serializers.ModelSerializer):
    # follows = SlugRelatedField('username')

    class Meta:
        model = Follow
        fields = []


class UserFollowsSerializer(serializers.ModelSerializer):
    follows = UserSerializer()

    class Meta:
        model = Follow
        fields = ['follows', 'followed']


class UserFollowedSerializer(serializers.ModelSerializer):
    follower = UserSerializer()

    class Meta:
        model = Follow
        fields = ['follower', 'followed']
