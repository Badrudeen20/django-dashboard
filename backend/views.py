from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import Group, Permission,ContentType
from django import forms
from .forms import UserRegistrationForm
from .forms import UserLoginForm
from django.conf import settings
from .models import *
import json
from backend.decorators import (
   permission_required,
   xhr_request_only,
   # add_edit_permission
)

def index(request):
    # print(request.user.email)
    return render(request,"index.html")
    
def login(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
       
        user = authenticate(request, username = username, password = password)
        if user is not None:
            form = login(request, user)
            messages.success(request, f' welcome {username} !!')
            # return redirect('home')
            return redirect('dashboard')
        else:
            # messages.info(request, f'account done not exit plz sign in')
            messages.error(request,'username or password not correct')
    form = UserLoginForm()
    return render(request, 'login.html', {'form':form, 'title':'log in'})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
       
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email =  userObj['email']
            password =  userObj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                print(password)
                User.objects.create_user(username, email, password)
                user = authenticate(username = username, password = password)
                login(request, user)
                return redirect('login')
                # return HttpResponseRedirect('/')    
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')
                
    else:
        form = UserRegistrationForm()
        
    return render(request, 'register.html', {'form' : form})

def logout(request):
    print('Logout')



def dashboard(request):
    return render(request,"admin/dashboard.html")


@permission_required()
def user(request):
    if request.method == 'POST':
      actionType = request.POST['type']
      if actionType == 'FETCH':
         start = request.POST['start']
         length = request.POST['length']
         search = request.POST['search']
         startIndex = (int(start)-1) * int(length)
         endIndex = startIndex + int(length)
        
         if search :
            data = list(User.objects.filter(username__contains=search)[startIndex:endIndex].values())
            totalLen = list(User.objects.filter(username__contains=search).values())
         else:
            data = User.objects.all()[startIndex:endIndex].all()
            totalLen = list(User.objects.all().values())
         
         listData = []
         for i in data:
             
             user = {
                "id":i.id,
                "name":i.username,
                "email":i.email,
                "role":i.rid.name,
                "action":(f'<button class="btn btn-primary" onclick=editModel({i.id})>Edit</button>'
                              f'<button class="btn btn-warning" onclick=delModel({i.id})>Delete</button>'
                              f'<a href="{settings.BASE_URL}dashboard/user/{i.id}/submodule" class="btn btn-success" >Action</a>')
             }
             
             listData.append(user)

         return JsonResponse({
            "success": True,
            "iTotalRecords":len(totalLen),
            "iTotalDisplayRecords":len(totalLen),
            "aaData":listData
         }, status=200)


      elif actionType == 'EDIT':
         pass
      else:  
         pass
    else:
      return render(request,"admin/user/index.html")


def usersubmodule(request,id=None):
     context = {
      "userId":id
     }
     return render(request,"admin/user/submodule.html",context)


@permission_required()
def permission(request,*args,**kwargs):
   
   if request.method == 'POST':

      action = request.POST['type']
      if action == 'View':
         start = request.POST['start']
         length = request.POST['length']
         search = request.POST['search']
         startIndex = (int(start)-1) * int(length)
         endIndex = startIndex + int(length)
         roleIds = list(Role.objects.filter(user=request.user.id).values_list('group', flat=True))
         if search :
            data = Group.objects.filter(name__contains=search,id__in=roleIds)[startIndex:endIndex].all()
            totalLen = list(Group.objects.filter(name__contains=search,id__in=roleIds).all())
           
         else:
            data = Group.objects.filter(id__in=roleIds)[startIndex:endIndex].all()
            totalLen = list(Group.objects.filter(id__in=roleIds).all())

         listData = []
         for i in data:
             
             permission = {
               "id":i.id,
               "roleName":i.name,
               "action":(f'<a class="btn btn-primary" href="{settings.BASE_URL}admin/administration/permission/{i.id}" >Permission</a>')
             }

             listData.append(permission)
       
         return JsonResponse({
            "success": True,
            "iTotalRecords":len(totalLen),
            "iTotalDisplayRecords":len(totalLen),
            "aaData":listData
         }, status=200)

      elif action == 'EDIT':
         pass
      else:
         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
   else:
      return render(request,"admin/permission/index.html")

@permission_required()
def module(request,*args,**kwargs):
   if request.method == 'POST':
      action = request.POST['type']

      if action == 'View':
         start = request.POST['start']
         length = request.POST['length']
         search = request.POST['search']
         startIndex = (int(start)-1) * int(length)
         endIndex = startIndex + int(length)
         # roleId = request.user.rid_id
         moduleIds = kwargs.get('moduleIds')
         # moduleIds = list(GroupPermission.objects.filter(group__in=groupIds).values_list('module',flat=True))
         uniqueModuleIds = list(dict.fromkeys(moduleIds))
        
         if search :
            data = Module.objects.filter(id__in=uniqueModuleIds,module__contains=search)[startIndex:endIndex].all()
            totalLen = list(Module.objects.filter(id__in=uniqueModuleIds,module__contains=search).all())
         else:
            data = Module.objects.filter(id__in=uniqueModuleIds)[startIndex:endIndex].all()
            totalLen = list(Module.objects.filter(id__in=uniqueModuleIds).all())
           
         
         listData = []
         for i in data:
             permission = {
               "id":i.id,
               "module":i.module,
               "action":(f'<a href="{settings.BASE_URL}admin/administration/module/{i.id}/edit" class="btn btn-primary" >Change</a>')
             }
                
             listData.append(permission)
         
         return JsonResponse({
            "success": True,
            "iTotalRecords":len(totalLen),
            "iTotalDisplayRecords":len(totalLen),
            "aaData":listData
         }, status=200)
      elif action == 'Edit':
           pass

      else:
         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

   else:
      return render(request,"admin/module/index.html")

@permission_required()
def addeditModule(request,moduleId=""):
    if request.method == 'POST':
       module = request.POST['module']
       parent = request.POST['parent']
       action = request.POST['type']
       moduleType = request.POST['moduleType']
      #  parent = request.POST['parent'] if request.POST['parent'] else ""
       addModule =  Module.objects.create(module=module,pid=parent,moduleType=moduleType)
       addModule.save()
       if moduleType == '2':
         permissionList = ['View']
       else:
         permissionList = ['View','Add','Edit','Delete']
       for i in permissionList:
           addPermission =  GroupPermission.objects.create(rid_id=request.user.rid_id,mid_id=addModule.id,mpid=addModule.pid,permission=i)
           addPermission.save()
       
        
       return render(request,"admin/module/index.html")
    else:
      if moduleId:
         module =  Module.objects.filter(id=moduleId).all().values()
      else:
         update = list(GroupPermission.objects.filter(rid_id=request.user.rid_id).values_list('mid_id',flat=True))
         module =  Module.objects.all().exclude(id__in=update).values()
     
      context = {
          "roleId":request.user.rid_id,
          "modules":module,
          "moduleId":moduleId,
      }
 
      return render(request,"admin/module/add.html",context)



@permission_required()
def rolePermission(request,*args,**kwargs):
    roleId = kwargs.get('roleId')
    if request.method == 'POST':
      actionType = request.POST['type']
      if actionType == 'View':
         start = int(request.POST['start'])
         length = int(request.POST['length'])
         search = request.POST['search']
         startIndex = (int(start)-1) * int(length)
         endIndex = startIndex + int(length)
         moduleIds = kwargs.get('moduleIds')
         groupIds = kwargs.get('groupIds')
         if search :
            data =  Module.objects.filter(module__contains=search,id__in=moduleIds)[startIndex:endIndex].all()
            totalLen = list(Module.objects.filter(module__contains=search,id__in=moduleIds).all())
         else:
            data =  Module.objects.filter(id__in=moduleIds)[startIndex:endIndex].all()
            totalLen = list(Module.objects.filter(id__in=moduleIds).all())

        
       
        
         listData = []
         lst = {}
         for i in data:
            per = '<div class="d-flex">' 
            for b in i.grouppermissions.filter(group__in=groupIds).all():
               per +=f'''
                        <div class="form-check px-3">
                              <input class="form-check-input" name="permission[{b.module_id}][{b.module_parent_id}]" type="checkbox" value="{b.permission}" id="flexCheck{b.id}">
                              <label class="form-check-label" for="flexCheck{b.id}">{b.permission}</label>  
                        </div>
                     '''
            per +='</div>'
            permission = {
               "id":i.id,
               "moduleName":i.module,
               "permission":per,
               "action":f'''
                           <div class="form-check">
                             <input class="form-check-input" type="checkbox" value="" id="flexCheckIndeterminate">
                             <label class="form-check-label" for="flexCheckIndeterminate"> All</label>
                           </div>
                        '''
            }
           
            listData.append(permission)
                   
         
         return JsonResponse({
            "success": True,
            "iTotalRecords":len(totalLen),
            "iTotalDisplayRecords":len(totalLen),
            "aaData":listData
         }, status=200)
    else:
      context = {
         "roleId":roleId
      }
      return render(request,"admin/permission/access.html",context)

@permission_required()  
def savePermission(request,*args,**kwargs):
    roleId = kwargs.get('roleId')
    if request.method == 'POST':
      moduleIds = kwargs.get('moduleIds')
      moduleList =  Module.objects.filter(id__in=moduleIds).all()
      post = request.POST
      assign = {}
      for i in moduleList:
         permission = i.grouppermissions.values('module','module_parent_id','permission')
         access = {}
         for b in permission:
            mid = b['module']
            mpid = b['module_parent_id']
            key = f'permission[{mid}][{mpid}]'
            if b['permission'] in request.POST.getlist(key):
               access[b['permission']] = [mid,mpid]
               assign[i.id] = access
     
      group_list = []
      group_instance = Group.objects.get(id=roleId)
      for i in assign:
          for b in assign[i]:
               module_instance = Module.objects.get(id=assign[i][b][0])
               group_permission = GroupPermission(
                  permission=f"{b}",                  
                  module=module_instance,                  
                  module_parent_id=f"{assign[i][b][1]}",
                  group=group_instance
               )
               group_list.append(group_permission)

      GroupPermission.objects.bulk_create(group_list)   
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@permission_required()
def addeditPermission(request,roleId=None,moduleId=None):
    if request.method == 'POST':
       mid = request.POST['module']
       rid = request.POST['role']
       action = request.POST['type']
       permission = request.POST.getlist('permission[]')
      #  url = request.path.split('/')[4]
       mpid = request.POST['mpid'] if request.POST['mpid'] else ""
       
       if action == 'Edit':
          
          update = list(GroupPermission.objects.filter(mid_id = mid,rid_id=rid).values_list('permission',flat=True))
          allPermission = call_name()
          if len(permission) > 0:
            if 'View' in permission:
               for i in permission:
               
                  allPermission.remove(i)
                  if i not in update:
                     if id:
                        content =  GroupPermission.objects.create(rid_id=rid,mid_id=mid,mpid=id,permission=i)
                     else:
                        content =  GroupPermission.objects.create(rid_id=rid,mid_id=mid,permission=i)
                     content.save()
            
               delete = GroupPermission.objects.filter(mid_id = mid,permission__in=allPermission,rid=rid).delete()
          else:
               delete = GroupPermission.objects.filter(mid_id = mid,permission__in=allPermission,rid=rid).delete()
       elif action == 'Add':
        
         for i in permission:
             content = GroupPermission.objects.create(rid_id=rid,mid_id=mid,mpid=mpid,permission=i)
             content.save()
       
       context = {
         "roleId":rid,
       }
       return render(request,"admin/permission/access.html",context)

    else:
       if moduleId:
          module =  Module.objects.filter(id=moduleId).all().values()
       else:
          update = list(GroupPermission.objects.filter(rid_id=roleId).values_list('mid_id',flat=True))
          module =  Module.objects.all().exclude(id__in=update).values()
      #  print(module)
       context = {
          "roleId":roleId,
          "modules":module,
          "moduleId":moduleId,
       }
       return render(request,"admin/permission/add.html",context)


@xhr_request_only()
def getPermission(request):
    roleId = request.POST['roleId']
    moduleId = request.POST['moduleId']
    data =  GroupPermission.objects.filter(rid_id=roleId,mid_id=moduleId).all()
    mpid  = Module.objects.filter(id=moduleId).values().first()
   #  mpid['moduleType']
    permission = call_name()
    
    if mpid['moduleType']=='2':
       
       moduleTypeList = ['Add','Edit','Delete']
       for i in moduleTypeList:
           permission.remove(i)
   
    selected = []
   
    for i in data:
        selected.append(i.permission)
      #   if request.POST['action']=='Add':
      #      permission.remove(i.permission)
        
        
        

    context = {
         "Success":True,
         "data":permission,
         "selected":selected,
         "mpid":mpid
    }   
    return JsonResponse(context, status=200)  




@xhr_request_only()
def moduleList(request):
   parentList =  list(Module.objects.all().values())
   permission = request.listData
   return JsonResponse({
      "success": True,
      "data":parentList,
      "permission":permission
   }, status=200)   


@xhr_request_only()
def moduleEdit(request,moduleId=None):
   data =  GroupPermission.objects.filter(rid_id=request.user.group,mid_id=moduleId).all()
   url = request.path.split('/')[3]
   context = {
      "Success":False,
      "data":[]
   }
   
   for i in data:  
       print(i)
       if i.permission.lower()==request.POST['type'].lower():
          context = {
            "Success":True,
            "data":list(Module.objects.filter(id=moduleId).values())
          }
      
         
   return JsonResponse(context, status=200)   

@xhr_request_only()
def sidebarList(request,*args,**kwargs):
   moduleIds = kwargs.get('moduleIds')
   sidebarList =  list(Module.objects.filter(id__in=moduleIds).values())
   return JsonResponse({
      "success": True,
      "data":sidebarList
   }, status=200)   
   

""" 
@permission_required()
def graphChart(request):
    return render(request,"admin/plugins/graph/chart.html") """
    
def redirect(request):
    return render(request,"index.html")




  
