from .models import Todo
from rest_framework import serializers

class TodoSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Todo
        fields = '__all__'
        # fields = ['list', 'of', 'attributes',]

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
        
        