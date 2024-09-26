import logging
from django.http import HttpResponse
from django.shortcuts import redirect
logger = logging.getLogger(__name__)

class DashboardMiddlewere(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        url = request.path
        if request.user.is_authenticated:
            if request.path == '/admin/login/' or request.path == '/admin/register/':
                return redirect('dashboard')
            else:
                return self.get_response(request)
        else:
            if request.path == 'admin/dashboard':
               return redirect('login')
            else:
               return self.get_response(request)
