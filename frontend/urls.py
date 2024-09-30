from django.urls import path
#now import the views.py file into this code
from . import views
urlpatterns=[
  path('',views.home,name="home"),
  # path('movie/posts',views.posts),
  # path('movie/trand',views.trand),
  path('menuList',views.menuList),
  # path('movie/menu',views.menu),
  # path('movie/menu/<int:pId>',views.menu),
  # path('movie/posts/<int:id>',views.posts),
  # path('movie/posts/<int:id>/add-edit',views.postAddEditView),
  # path('movie/posts/add-edit',views.postAddEditView),
  path('detail/<str:Link>',views.postDetailView),
 
 
]
