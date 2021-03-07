from .models import Todo
from rest_framework import serializers

## Adding auth to our endpoints: 
from django.contrib.auth.models import User

# Instead of defining the Todos, we serializer Users and reverse lookup 
# todos by seeing which todos are associated with the current user. This is 
# possible because we defined the related field in the Todo Model. 
# class UserSerializer(serializers.ModelSerializer): 

# From documentation: 

# The HyperlinkedModelSerializer has the following differences from ModelSerializer:

#     It does not include the id field by default.
#     It includes a url field, using HyperlinkedIdentityField.
#     Relationships use HyperlinkedRelatedField, instead of
#       PrimaryKeyRelatedField.

class UserSerializer(serializers.ModelSerializer): 
# class UserSerializer(serializers.HyperlinkedModelSerializer): 
    # queryset = Todo.objects.all()
    todo = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name='api:todo-detail'
        ) #, queryset=queryset)

    # todo = serializers.HyperlinkedRelatedField(
        # many=True, view_name = 'api:todo-detail', read_only=True
    # )

    class Meta:
        model = User
        # Will only return all fields for the User model we want to know the Todos
        # fields = '__all__'
        # Reverse look up; need to manually define the todo key
        # [{'id': 1, 'username': 'bill', 'todo': [1, 3, 4]}, .....]
        fields = ['id', 'username', 'todo']
        # fields = ['url', 'id', 'username', 'todo']

class TodoSerializer(serializers.ModelSerializer):
# class TodoSerializer(serializers.HyperlinkedModelSerializer):
    # Both do the same things. This is how we control which attribute from the 
    # user instance is used as the foreign key. When we make a post request 
    # from command line, we are an anonomous user. 
    # Can now make requests with adding auth as username/password.
    # owner = serializers.CharField(read_only=True, source='owner.pk')
    owner = serializers.ReadOnlyField(source='owner.username')
    

    class Meta: 
        model = Todo
        # fields = '__all__'
        fields = [
            'id',  'owner', 'title', 'description', 'is_complete', 
            'time_created', 'last_modified'
        ]

    # Used when defining serializers manually s
    def create(self, validated_data): 
        # wondering why validated_data is not **
        # validated data is passed as a dictionary?
        # what is done when we create a new Todo
        return Todo.objects.create(**validated_data)

    def update(self, instance, validated_data): 
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.is_complete = validated_data.get('is_complete', instance.is_complete)
        instance.save()
        return instance 
        
        