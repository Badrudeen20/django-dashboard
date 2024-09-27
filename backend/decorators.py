from functools import wraps 
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .models import *

def permission_required():
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            
            url = request.path.split('/')[2]
            if request.method == 'GET':
                return view(request, *args, **kwargs)      
                      
            elif request.method == 'POST':
                groupIds = list(request.user.groups.values_list('id', flat=True))
                kwargs['moduleIds'] = list(GroupPermission.objects.filter(group__in=groupIds,permission='View').values_list('module', flat=True))
                kwargs['groupIds'] = groupIds
                return view(request, *args, **kwargs) 
   
             
            if request.META.get('HTTP_REFERER') == None:
               return redirect("redirect")
            else:
                return redirect(request.META.get('HTTP_REFERER'))
        return _wrapped_view
    return decorator


def xhr_request_only():
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                groupIds = list(request.user.groups.values_list('id', flat=True))
                kwargs['moduleIds'] = list(GroupPermission.objects.filter(group__in=groupIds,permission='View').values_list('module', flat=True))
                kwargs['groupIds'] = groupIds
                return view(request, *args, **kwargs)     
        return wrapper
    return decorator


