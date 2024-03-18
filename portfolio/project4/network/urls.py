
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("npost", views.npost , name = "npost"),
    path("delete_post/<int:post_id>/", views.delete_post , name = "delete_post"),
    path("smprofile/<str:username>/", views.smprofile , name = "smprofile"),
    path("followingpage/", views.followingpage , name = "followingpage"),
    path("smprofilefollowing/<str:username>/", views.smprofilefollowing, name = "smprofilefollowing"),
    # smprofile stands for social media profile
    path("edit_post/<int:id>", views.edit_post , name = "edit_post"),
    path("liked_post/<int:id>", views.liked_post , name = "liked_post")
    


]
