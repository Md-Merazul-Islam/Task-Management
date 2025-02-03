from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password =serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username','email', 'password', 'confirm_password']
        
     #checking input data are valid or not   
    def validate(self, data):
        if data['password']!= data['confirm_password']:
            raise serializers.ValidationError({'password':'Password does not match'})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email':'Email already exists'})
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username':'Username already exists'})
    
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password') 
        user= User(**validated_data)
        user.set_password(validated_data['password'])
        user.is_active=True # if we use OTP verification then we can set False then it will handel on activate function
        user.save()
        return user
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('password', None)
        return representation
    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'profile_image']  
   
    def validate_email(self, value):
        if User.objects.filter(email=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value

