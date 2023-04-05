from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=128, write_only=True)
    class Meta:
        model = User
        fields = ('id','username','first_name','role','email','password','password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password2')
        user = User(**validated_data)
        user.set_password(password)
        user.debet = 0
        user.save()
        return user


