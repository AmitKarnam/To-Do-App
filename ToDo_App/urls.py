from django.urls import path

from . import views

app_name = "ToDo_App"

urlpatterns = [
     path("",views.index,name="Welcome_page"),
     path("signup",views.signup,name="Sign_up"),
     path("login",views.login_page,name="Login_Page"),
     path("logout",views.logout_view,name="logout"),
     path("ToDo",views.ToDo,name="ToDo"),
     path("Update_Task/<str:pk>/",views.Update_Task, name="Update_Task"),
     path("Delete_Task/<str:pk>/",views.Delete_Task, name="Delete_Task")

]