from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_manager', 'manager_id']
    

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'password2', 'is_manager', 'manager_id']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            first_name = validated_data.get('first_name', ''),
            last_name = validated_data.get('last_name', ''),
            is_manager = validated_data.get('is_manager', False),
            manager_id = validated_data.get('manager_id', None)
        )

        user.set_password(validated_data['password'])
        user.save()
        return user