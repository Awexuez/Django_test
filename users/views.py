from typing import Any
from django.shortcuts import render, HttpResponsePermanentRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView
from users.models import User

from products.models import Basket
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm

def login(request):
    if request.method == "POST":
        form = UserLoginForm(data = request.POST)
        if form.is_valid():
            username = request.POST['username']                             # Идентификация
            password = request.POST['password']
            user = auth.authenticate(username=username,password=password)   # Аутентификация
            if user:                        
                auth.login(request, user)                                   # Авторизация
                return HttpResponsePermanentRedirect(reverse('index'))
    else:
        form = UserLoginForm()    
    context = {'form': form}
    return render(request, 'users/login.html', context)

class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Store - Регистрация'
        return context

# def registration(request):
#     if request.method == "POST":
#         form = UserRegistrationForm(data = request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Поздравляем! Регистрация прошла успешно!')
#             return HttpResponsePermanentRedirect(reverse('users:login'))
#     else:
#         form = UserRegistrationForm()
#     context = {'form': form}
#     return render(request, 'users/registration.html', context)

# class UserProfileView(UpdateView):
#     model = User
#     form_class = UserProfileForm
#     template_name = 'users/profile.html'

#     def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Store - Личный кабинет'
#         context['baskets'] = Basket.objects.filter(user=self.object)
#         return context
    
@login_required
def profile(request):
    if request.method == "POST":
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)  
        if form.is_valid():                                               
            form.save()
            return HttpResponsePermanentRedirect(reverse('users:profile'))
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        'title': 'Store - Профиль', 
        'form': form,
        'baskets': Basket.objects.filter(user=request.user),
        }
    return render(request, 'users/profile.html', context)

def logout(request):
    auth.logout(request)
    return HttpResponsePermanentRedirect(reverse('index'))

