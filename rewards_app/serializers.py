from rest_framework import serializers
from .models import RewardsAppUsers, RewardsAppAndroidapp, RewardsAppUsertask

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RewardsAppUsers
        # fields = ['id', 'name', 'email', 'role', 'profilepic', 'created_on', 'password']
        fields = '__all__'

class AndroidAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = RewardsAppAndroidapp
        fields = ['id', 'name', 'app_logo', 'url', 'category', 'subcategory', 'points', 'created_on', 'is_delete']

class UserTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = RewardsAppUsertask
        fields = ['id', 'user', 'task', 'is_completed', 'screenshot', 'points_earned']
