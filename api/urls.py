from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from api import views 
from api.views import (
    TodoList, TodoDetail, 
    UserList, UserDetail
)

app_name = 'api'

urlpatterns = [
    # path('todo/', views.todo_list, name='todo_list'),
    # path('todo/<int:pk>', views.todo_detail, name='todo_detail'),
    path('', views.api_root),
    path('todo/', TodoList.as_view(), name='todo-list'),
    path('todo/<int:pk>', TodoDetail.as_view(), name='todo-detail'),
    path('user/', UserList.as_view(), name='user-list'),
    path('user/<int:pk>', UserDetail.as_view(), name='user-detail'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
    