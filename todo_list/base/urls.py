from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import *

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'), # тут ми вказуємо через next_page, що якщо ми виходимо з акаунту то переходимо на сторінку "login"

    path('', TaskList.as_view(), name='tasks'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>', DeleteView.as_view(), name='task-delete'),
]