from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from .models import Task


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'  # LoginView одразу забезпечує нас формою
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

# За допомогою міксину LoginRequiredMixin ми перевіряємо чи
# користувач авторизований і цей міксин обов'язково має йти першим
# --------------------------------------
# ListView здатний повернути масив якихось даних
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    # Метод для того, щоб користувач отримував виключно ті дані, які належать йому
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count

        # search-area - це name нашого інпуту
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)

        context['search_input'] = search_input

        return context


# DetailView - для того, щоб отримати один конкретний об'єкт
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task

    # Вказуємо поля які хочемо бачити у нашій формі
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = '__all__'  # через '__all__' ми вказуємо що валідуємо всі поля
    success_url = reverse_lazy('tasks')


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
