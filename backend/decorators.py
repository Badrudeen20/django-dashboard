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
            
            url = request.path.split('/')
            filterUrl = url[1:4]
            access = "/".join(filterUrl)
            groupIds = list(request.user.groups.values_list('id', flat=True))
            groupList = GroupPermission.objects.filter(group__in=groupIds,permission__icontains='View').all()
            kwargs['moduleIds'] = []
            kwargs['access'] = False
            kwargs['permission'] = []
            for item in groupList:
                kwargs['moduleIds'].append(item.module_id)
                if access==item.module.url:
                    kwargs['access'] = True
                    access = item.permission.split(",")
                    kwargs['permission'].extend(access)
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
                # groupIds = list(request.user.groups.values_list('id', flat=True))
                # kwargs['moduleIds'] = list(GroupPermission.objects.filter(group__in=groupIds,permission__icontains='View').values_list('module', flat=True))
                # kwargs['groupIds'] = groupIds
                # return view(request, *args, **kwargs)   

                url = request.path.split('/')
                filterUrl = url[1:4]
                access = "/".join(filterUrl)
                groupIds = list(request.user.groups.values_list('id', flat=True))
                groupList = GroupPermission.objects.filter(group__in=groupIds,permission__icontains='View').all()
                kwargs['moduleIds'] = []
                kwargs['access'] = False
                kwargs['permission'] = []
                for item in groupList:
                    kwargs['moduleIds'].append(item.module_id)
                    if access==item.module.url:
                        kwargs['access'] = True
                        access = item.permission.split(",")
                        kwargs['permission'].extend(access)
                kwargs['groupIds'] = groupIds  
                return view(request, *args, **kwargs)  
        return wrapper
    return decorator


