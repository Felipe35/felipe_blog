from datetime import date

from django.http import HttpResponseRedirect
from django.views import View

from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog_db
# User Authentication
from .forms import CommentForm, CreateUserForm
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


def get_date(post):
    return post['date']


class RegisterPageView(View):
    def get(self, request):
        form = CreateUserForm()

        context = {"form": form}
        return render(request, "blog/registration.html", context)
    
    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, "Account was created for " + user)
            return redirect("login")
        
        context = {"form": form}
        return render(request, "blog/registration.html", context)

        

class LoginPageView(View):

    def get(self, request):
         context = {}

         return render(request, "blog/login.html", context)
    
    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("starting-page")
        else:
            messages.info(request, "Username OR password is incorrect")
        
        context = {}

        return render(request, "blog/login.html", context)
        



# def registerPage(request):
#     form = CreateUserForm()

#     if request.method == "POST":
#         form = CreateUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             user = form.cleaned_data.get("username")
#             messages.success(request, "Account was created for " + user)
#             return redirect("login")

#     context = {"form": form}
#     return render(request, "blog/registration.html", context)


# def loginPage(request):

#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect("starting-page")
#         else:
#             messages.info(request, "Username OR password is incorrect")
            
#     context = {}

#     return render(request, "blog/login.html", context)


def logOutUser(request):
    logout(request)
    return redirect("login")



def starting_page(request):
    # sorted_posts = sorted(all_posts, key=get_date)
    # latest_posts = sorted_posts[-3:] #Get the last 3 items from the list
    latest_posts = Blog_db.objects.all().order_by("-date")[:3]
    
    return render(request, "blog/index.html", {
        "posts": latest_posts,
        
    })

def posts(request):
    all_posts = Blog_db.objects.all().order_by("-date")

    return render(request, "blog/all-posts.html", {
        "all_posts": all_posts
    })


class PostDetailView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'login'
    def is_stored_posts(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
        return is_saved_for_later

    def get(self, request, slug):
        all_posts = Blog_db.objects.get(slug=slug)
        
        context = {
            "post": all_posts,
            "tags": all_posts.blog_tags.all(),
            "comment_form": CommentForm(),
            "comments":all_posts.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_posts(request, all_posts.id)
            }   
       
        return render(request, "blog/post-detail.html", context)
    

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        all_posts = Blog_db.objects.get(slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = all_posts
            comment.save()

            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))
            
        context = {
                "post": all_posts,
                "tags": all_posts.blog_tags.all(),
                "comment_form": comment_form,
                "commments": all_posts.comments.all().order_by("-id"),
                "saved_for_later": self.is_stored_posts(request, all_posts.id)
                }   
        return render(request, "blog/post-detail.html", context)


class ReadLaterView(View):

    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Blog_db.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, "blog/stored-posts.html", context)


    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect("/")