from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from frontend.models import *
from django.db.models import Q
from django.conf import settings


def home(request):
    if request.method == 'POST':
      action = request.POST['type']
      if action == 'View':
         start = request.POST['start']
         length = request.POST['length']
         search = request.POST['search']
         startIndex = (int(start)-1) * int(length)
         endIndex = startIndex + int(length)
        
        
         if search :
            data = Posts.objects.filter(name__contains=search,status=1)[startIndex:endIndex].all()
            totalLen = Posts.objects.filter(name__contains=search,status=1).count()
           
         else:
            data = Posts.objects.filter(status=1).all()[startIndex:endIndex]
            totalLen = Posts.objects.count()
           
         listData = []
         for i in data:
            
            post = {
               "id":i.id,
               "name":i.name,
               "image":i.image,
               "rate":i.rate,
              
            }
                
            listData.append(post)
        
         return JsonResponse({
            "success": True,
            "iTotalRecords":totalLen,
            "iTotalDisplayRecords":totalLen,
            "aaData":listData
         }, status=200)
    else:
      trands = Trand.objects.all()[0:4]
      context = {
         "Trands":trands,
      }
      
      
      
      return render(request,"home.html",context)

   
def menuList(request):
   if request.method == 'POST':
      menus =  Menu.objects.filter(status="1").all()
      MenuHtml = ''
      
      for m in menus:
         if m.menuId == None:
            MenuHtml += (f'<li><button class="nav-link dropdown-btn" data-dropdown="dropdown{m.id}" aria-haspopup="true" aria-expanded="false" aria-label="discover">{m.name}<i class="bx bx-chevron-down" aria-hidden="true"></i></button>'
                         f'{menuLoop(menus,m.id)}'
                         f'</li>')
      return JsonResponse({
               "Success": True,
               "Menus":MenuHtml
            }, status=200)


def menuLoop(Menus=[],MenuId=None,IsLoop=None):
   check = False
   if IsLoop:
      menu = f'<div id="dropdown{MenuId}" class="dropdown loopMenu"><ul role="menu">'
      arrow = '<i class="bx bx-chevron-down" aria-hidden="true"></i>'
   else:
      menu = f'<div id="dropdown{MenuId}" class="dropdown"><ul role="menu">'
      arrow = ''
   for m in Menus:
      if m.menuId:
         if m.menuId==str(MenuId):
            check = True
            menu += (f'<li><a class="dropdown-link dropdown-btn" data-dropdown="dropdown{m.id}" href="#" aria-haspopup="true" aria-expanded="false">{m.name}{arrow}</a>{menuLoop(Menus,m.id,True)}</li>')
   menu +='</ul></div>'
   if check:
      return menu
   else:    
      return ''

def postDetailView(request,Link=None):
      linkList = Link.split("+")
      MovieName = " ".join(linkList)
      data = Posts.objects.filter(name=MovieName,status=1).values().first()
      context = {
         "link":Link,
         "post":data
      }
      return render(request,"detail.html",context)

