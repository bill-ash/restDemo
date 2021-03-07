from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views 

app_name = 'api'

urlpatterns = [
    path('todo/', views.todo_list, name='todo_list'),
    path('todo/<int:pk>', views.todo_detail, name='todo_detail'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
    