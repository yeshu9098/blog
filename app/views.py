from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render, HttpResponseRedirect
from django.contrib.auth import logout
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail
from datetime import datetime
from app.models import Category, Contact, Post, Comment, Reply
from .forms import MessageForm, PostForm, CommentForm, ReplyForm
from account.models import CustomUser
import requests
from django.views.generic.detail import DetailView
# Create your views here.


def index(request):
    user = request.user
    cat = Category.objects.all()[:5]
    posts = Post.objects.all().order_by('-id')
    data = {
        'posts': posts,
        'cat' : cat,
        'user': user,
    }
    return render(request, 'index.html', data) 



def reply(request, id):
    comment = get_object_or_404(Comment, id=id)
    reply_form = ReplyForm(request.POST or None)

    if reply_form.is_valid():
        reply = request.POST.get('reply')
        reply = Reply.objects.create(comment = comment, user = request.user, reply = reply)
        reply.save()
        return redirect("/")

    context={
        "reply" : reply_form,
        "comment" : comment,
    }
    return render(request, 'reply.html', context)


def post(request, id):
    post = get_object_or_404(Post, id=id)
    cat = Category.objects.all()[:10]
    comments = Comment.objects.all()

    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = request.POST.get('comment')
        comment = Comment.objects.create(post = post, user = request.user, comment = comment)
        comment.save()
        return redirect("/")

    
    context={
        "post":post,
        "cat" : cat,
        "form" : form,
        "comments" : comments,
    }
    return render(request, 'post.html', context)





def category(request,title):
    category = Category.objects.get(title=title)
    posts = Post.objects.filter(category=category)
    cat = Category.objects.all()[:10]
    data = {
        'category': category,
        'posts': posts,
        'cat': cat,
    }
    return render(request, "category.html", data)


def addpost(request):
    if request.user.is_authenticated:
        cat = Category.objects.all()[:10]
        form = PostForm(request.POST or None)
        if form.is_valid():
            obj = form.save(commit = False)
            obj.user = request.user
            obj.save()
            return HttpResponseRedirect("/")     
        context = {
            'form' : form,
            'cat' : cat,
            }
        return render(request, "addpost.html", context)
    else:
        return redirect("account:login")



# delete view for details
def delete(request, id):
    if request.user.is_authenticated:
        context ={}

        post = get_object_or_404(Post, id = id)

        if request.user.id == post.user.id:
            
            if request.method =="POST":
                post.delete()
                return HttpResponseRedirect("/")
    
            return render(request, "delete.html", context)
        else:
            return redirect('/')
    else:
        return redirect("account:login")


def update(request, id):
    if request.user.is_authenticated:
        # dictionary for initial data with
        # field names as keys
        context ={}
        # fetch the object related to passed id
        post = get_object_or_404(Post, id = id)
        cat = Category.objects.all()

        if request.user.id == post.user.id:
            
            # pass the object as instance in form
            form = PostForm(request.POST or None, instance = post)
        
            # save the data from the form and
            # redirect to detail_view
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/")
        
            # add form dictionary to context
            context = {
                'form' : form,
                'post' : post,
                'cat' : cat,
                }

            return render(request, "update.html", context)
        else:
            return redirect('/')
    else:
        return redirect("account:login")



def profile(request, id):
    if request.user.is_authenticated:
        user = get_object_or_404(CustomUser, id = id)
        logged_in_user_posts = Post.objects.filter(user=user)
        # post = get_object_or_404(logged_in_user_posts, id = id)
        context = {
            'obj': user,
            'logged_in_user_posts': logged_in_user_posts,
            # 'post': post,
        }
        # print(logged_in_user_posts)
        return render(request, 'profile.html', context)
    else:
        return redirect("account:login")


def contact(request):
    if request.user.is_authenticated:
        error = False
        if request.method == "POST":
            form = MessageForm(request.POST)
            if form.is_valid():
                message = request.POST.get('message')

                user = request.user
                contact = Contact(user=user,
                                message=message,
                                date=datetime.today())
                contact.save()

                #receive email
                subject = f'Message From {user}!!!'
                send_mail(
                    subject,#subject
                    message, #message
                    user, #From email
                    ['yeshu9098@gmail.com'], #To email
                    )

                #send mail
                subject = 'Welcome To Django Application'
                message = f'Hi {user}, thank you for giving feedback'
                email = settings.EMAIL_HOST_USER
                recipient_list = [user]
                send_mail(
                    subject,
                    message,
                    email,
                    recipient_list,
                    )
                return redirect('/')          
            else: 
                error = True

        return render(request, 'contact.html',{ 'error': error })

    else:
        return redirect("account:login")


def log_out(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect(reverse('account:login'))
