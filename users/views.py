from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .forms import SignInForm, SignUpForm, EditUserDataForm, EditPasswordForm


class Profile(View):
    template_name = 'profile.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('sign_in'))
        ctx = {
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        return render(request, self.template_name, context=ctx)


class SignIn(View):
    template_name = 'sign_in.html'

    def get(self, request):
        form = SignInForm()
        # render - Объединяет заданный шаблон с заданным контекстным словарем
        # и возвращает объект HttpResponse с этим визуализированным кодом.
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SignInForm(request.POST)
        # is_valid() возвращает True, если данные валидны, False, если нет.
        # появляется аттрибут cleaned_data, если данные оказались валидны.
        # появляется аттрибут errors, если данные оказались не валидны.
        if form.is_valid():
            # authenticate - проверяет предоставленные учетные данные.
            # Если ауентификация успешна - возвращает объект пользователя.
            # Если аутентификация неудачна, возвращает None.
            user = authenticate(**form.cleaned_data)
            if user:
                # login принимает реквест и объект модели пользователя и отвечает за процесс авторизации
                login(request, user)
                # reverse генерирует URL-адрес при помощи соответствующего имени URL
                url = reverse('sign_in')
                return HttpResponseRedirect(url)
        return render(request, self.template_name, {'form': form})


class SignUp(View):
    template_name = 'sign_up.html'

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.create_user()
            url = reverse('sign_in')
            return HttpResponseRedirect(url)
        return render(request, self.template_name, {'form': form})


class EditUserData(View):
    template_name = 'edit_user_data.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('sign_in'))
        user_data = {
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }

        form = EditUserDataForm(initial=user_data)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = EditUserDataForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            url = reverse('sign_in')
            return HttpResponseRedirect(url)
        return render(request, self.template_name, {'form': form})


class EditPassword(View):
    template_name = 'edit_password.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('sign_in'))
        form = EditPasswordForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = EditPasswordForm(request.POST, instance=request.user)
        if form.is_valid():
            form.edit_password()
            url = reverse('sign_in')
            return HttpResponseRedirect(url)
        return render(request, self.template_name, {'form': form})


class LogOut(View):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('sign_in'))
        logout(request)
        return redirect(reverse('sign_in'))
