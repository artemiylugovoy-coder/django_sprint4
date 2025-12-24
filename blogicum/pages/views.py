from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.http import HttpResponseForbidden


class About(TemplateView):
    template_name = 'pages/about.html'


class Rules(TemplateView):
    template_name = 'pages/rules.html'


def trigger_error(request):
    raise Exception("Тестовая ошибка для 500")


def page_not_found(request, exception):
    template_name = 'pages/404.html'
    return render(request, template_name, status=404)


def csrf_failure(request, reason=''):
    template_name = 'pages/403csrf.html'
    return render(request, template_name, status=403)


def server_problem(request):
    template_name = 'pages/500.html'
    return render(request, template_name, status=500)
