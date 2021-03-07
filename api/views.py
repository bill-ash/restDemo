from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt 

from rest_framework.parsers import JSONParser 
from rest_framework import status 
# For function based views 
from rest_framework.decorators import api_view
# For class based views
from rest_framework.views import APIView
# For propely handling content negotiation of response objects 
# Make sure the response content is what the client requested 
from rest_framework.response import Response 

# Format suffix patterns: format=None adds support to handle an array of content 
# types since our Response objects will now default to whatever the clinet requests. 

# TodoSerializer requires a *data* argument. data=request.data 

from .models import Todo
from .serializers import TodoSerializer

# Class based views inherit from APIView
class TodoList(APIView): 

    def get(self, request, format=None): 
        queryset = Todo.objects.all()
        todos = TodoSerializer(queryset, many=True)
        return Response(todos.data)
        
    def post(self, request, format=None): 
        todo = TodoSerializer(data=request.data)
        if todo.is_valid(): 
            todo.save()
            return Response(todo.data, status=status.HTTP_201_CREATED)
        return Response(todo.errors, status=status.HTTP_400_BAD_REQUEST)
        

class TodoDetail(APIView): 

    def get_object(self, pk):
        try:
            return Todo.objects.get(pk=pk)
        except Todo.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None): 
        queryset = self.get_object(pk)
        todo = TodoSerializer(queryset)
        return Response(todo.data)

    def put(self, request, pk, format=None): 
        queryset = self.get_object(pk)
        todo = TodoSerializer(queryset, data=request.data)
        if todo.is_valid(): 
            todo.save()
            return Response(todo.data)
        return Response(todo.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, format=None): 
        queryset = self.get_object(pk)
        todo = TodoSerializer(queryset, data=request.data)
        if todo.is_valid(): 
            todo.save()
            return Response(todo.data)
        return Response(todo.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        queryset = self.get_object(pk)
        # No need to serialize - delete 
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





# Decorator adds features to request object so they can be handled by serializers. 
@api_view(['GET', 'POST'])
def todo_list(request, format=None): 

    if request.method == 'GET': 
        queryset = Todo.objects.all()
        # many=True for more than one object (querysets)
        serializer = TodoSerializer(queryset, many=True)
        # I think there is another way to do this 
        # return HttpResponse(serializer.data, content='application/json')
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid(): 
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.error, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def todo_detail(request, pk, format=None): 

    try: 
        queryset = Todo.objects.get(pk=pk)
    except Todo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    if request.method == 'GET':
        serializer = TodoSerializer(queryset)
        return Response(serializer.data)

    elif request.method == 'PUT': 
        # Serializer takes two arguments, the queryset in the database, 
        # and the incoming request object.
        todo = TodoSerializer(queryset, data = request.data)
        if todo.is_valid(): 
            todo.save()
            return Response(todo.data)
        else: 
            return Response(todo.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    
