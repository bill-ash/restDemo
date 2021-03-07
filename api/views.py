from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from rest_framework.parsers import JSONParser 

from .models import Todo
from .serializers import TodoSerializer

@csrf_exempt
def todo_list(request): 
    if request.method == 'GET': 
        queryset = Todo.objects.all()
        # many=True for more than one object (querysets)
        serializer = TodoSerializer(queryset, many=True)
        # I think there is another way to do this 
        # return HttpResponse(serializer.data, content='application/json')
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TodoSerializer(data)
        if serializer.is_valid(): 
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.error, status=400)


@csrf_exempt
def todo_detail(request, pk): 

    try: 
        queryset = Todo.objects.get(id=pk)
    except Todo.DoesNotExist:
        return HttpResponse(status=404)
        
    if request.method == 'GET':
        serializer = TodoSerializer(queryset)
        return JsonResponse(serializer.data)

    elif request.method == 'POST': 
        data = JSONParser(request)
        todo = TodoSerializer(data)
        if todo.is_valid(): 
            todo.save()
            return JsonResponse(todo.data, status=201)
        else: 
            return JsonResponse(todo.error, status=400)

    else:
        return JsonResponse({'error': 'Could not process'})


    
