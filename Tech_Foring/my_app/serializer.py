from rest_framework import serializers
from .models import Users, Projects, Project_Members, Tasks, Comments

# User registration serializer
class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = Users
        fields = ['user_name', 'email', 'first_name', 'last_name', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):

        # Check email
        if Users.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError({'email': 'Email is already in use.'})
        
        # Password validation
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        
        return attrs

    def create(self, validated_data):
        return Users.objects.create_user(**validated_data)

class ProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project_Members
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


# User login serializer
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = Users
        fields = ['email', 'password']
       
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = Users.objects.filter(email=email).first()
            if user:
                if not user.check_password(password):
                    raise serializers.ValidationError(
                        {'error': 'Invalid email or password'}
                    )
            else:
                raise serializers.ValidationError(
                    {'error': 'Invalid email or password'}
                )
        else:
            raise serializers.ValidationError(
                {'error': 'Email and password are required'}
            )
            
        attrs['user'] = user
        return attrs
    
# User profile serializer
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['user_name', 'email', 'first_name', 'last_name']

# Project serializer
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projects
        fields = '__all__'

# Task serializer
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = '__all__'
        
# Comment serializer
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'

