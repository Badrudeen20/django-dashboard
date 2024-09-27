from django.urls import path
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import UserLoginForm
 
urlpatterns = [
        # path('index', views.index, name ='index'),
        path('register/', views.register, name='register'),
        path('login/', auth_views.LoginView.as_view(template_name='login.html',authentication_form=UserLoginForm), name='login'),
        path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),

        # Dashboard Url
        path('dashboard/', views.dashboard, name ='dashboard'),
        path('administration/permission',views.permission),
        path('administration/permission/<int:roleId>',views.rolePermission,name="role-permission"),
        path('module/permission/<int:roleId>',views.savePermission,name="save-permission"),
        path('administration/permission/<int:roleId>/add-edit',views.addeditPermission),
        path('administration/permission/<int:roleId>/add-edit/<int:moduleId>',views.addeditPermission),
        path('getPermission/',views.getPermission),
        path('administration/user',views.user,name="user"),
        path('user/<int:id>/submodule',views.usersubmodule,name="user-submodule"),
       
        # path('plugin/chart',views.graphChart),
        path('administration/module',views.module,name="module"),
        # path('administration/module/<int:parentId>/',views.module,name="module"),
        path('administration/module/add',views.addeditModule),
        path('administration/module/<int:moduleId>/edit',views.addeditModule),
        # path('module/add/<int:parentId>',views.addModule,name="add-module"),
        path('module/list',views.moduleList,name="module-list"),
        # path('module/edit/<int:moduleId>',views.moduleEdit),
        path('sidebar/list',views.sidebarList,name="sidebar-list"),
        path('redirect',views.redirect,name="redirect"),
        # path('notFound',views.notFound,name="notFound"),
 

]