from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.RegisterPageView.as_view(), name="register"),
    path("login/", views.LoginPageView.as_view(), name="login"),
    path("logout/", views.logOutUser, name="logout"),

    path("", views.starting_page, name="starting-page"), # Starting page
    path("posts", views.posts, name="posts-page"), 
    path("posts/<slug:slug>", views.PostDetailView.as_view(), name="post-detail-page"), # /posts/my-first-post
    path("read-later", views.ReadLaterView.as_view(), name="read-later")
]
