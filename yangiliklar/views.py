from http.client import responses

from django.contrib.auth import login,authenticate,logout
from django.db.models.fields.related_lookups import RelatedGreaterThan
from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.template.defaultfilters import title, slugify
from unicodedata import category
from .forms import AddNewsForm,UpdateNews,RegisterForm,LoginForm
from django.db.models import Q
from .models import New,Advertisement,Users_info,Comments,Contact

from django.core.paginator import Paginator

import requests

# for log out
from django.contrib import messages


def home_view(request):
    latest_new = New.published.order_by('-id').first()
    latest_news = New.published.order_by('-id')[1:5]
    sport_news = New.published.filter(category__name="Sport")
    techno_news = New.published.filter(category__name="Texnalogiya")
    intertain_news = New.published.filter(category__name="Kongilxushlik")
    busines_news = New.published.filter(category__name="Bussines")
    popular_news = New.published.filter(is_trending=True)

    context = {
        "latest_new" : latest_new,
        "latest_news" : latest_news,
        "sport_news" : sport_news,
        "techno_news" : techno_news,
        "intertain_news" : intertain_news,
        "busines_news" : busines_news,
        "popular_news" : popular_news,

    }
    return render(request,'index.html',context)




def detail_page(request,slug):
    news=New.published.get(slug=slug)
    news.view_count += 1
    news.save()


    # all_comments = Comments.published.filter(new=news).order_by('-created_at')
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')

        # comment_text = request.POST.get('comment')
        # if comment_text:
        #     Comments.objects.create(
        #         comment=comment_text,
        #         new=news,
        #         user=request.user
        #     )

        return redirect("detail",new=news.slug)


    context = {
        "news" : news,
        # "all_comments" : all_comments,
    }
    #   commentlar uchun joy
    return render(request,"single-page.html",context)



def sport_page(request):
    sport_news=New.published.filter(category__name="Sport")

    context={
        "sport_news" : sport_news
    }

    return render(request,"sport.html",context)


def local_page(request):
    local_news=New.published.filter(category__name="Mahalliy")

    context={
        "local_news" : local_news
    }

    return render(request,"local.html",context)


def foreign_page(request):
    foreign_news=New.published.filter(category__name="Xorij")

    context={
        "foreign_news" : foreign_news
    }

    return render(request,"foreign.html",context)



def texno_page(request):
    texno_news=New.published.filter(category__name="Texnalogiya")

    context={
        "texno_news" : texno_news
    }

    return render(request,"texno.html",context)








def add_news(request):
    if request.method == "POST":
        form=AddNewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = AddNewsForm()
    context = {
        "form": form
    }
    return render(request,"news_add.html",context)



def delete_new(request,pk):
    new =New.objects.get(pk=pk)
    if new:
        new.delete()
        return redirect('home')

    else:
        return redirect('home')

def update_new(request,pk):
    new=New.objects.get(pk=pk)
    if request.method == 'POST':
        form = AddNewsForm(request.POST, request.FILES, instance=new)
        if form.is_valid() :
            form.save()
            return redirect('home')
    else:
        form=UpdateNews(instance=new)
    context={
        'form':form
    }

    return render(request,"update_news.html",context)



# registration


# def register_wiew(request):
#     if request.user.is_authenticated:
#         return redirect('home')
#
#     if request.method == "POST":
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user=form.save(commit=False)
#             user.set_password(form.cleaned_data["password"])
#             user.save()
#             login(request, user)
#             return redirect('home')
#
#     else:
#         form = RegisterForm()
#     context={"form":form}
#
#     return render(request,'register.html',context)

def register_view(request):
    if request.method == "POST" :
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = RegisterForm
    context = {
        "form" : form
    }
    return render(request,'register.html',context)




def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home' )

    else:
        form = LoginForm()
    context={"form":form}

    return render(request,'login.html',context)



def logout_user(request):
    logout(request)
    return redirect('home')


# SEARCH FUNCTION

def search_view(request):
    query = request.GET.get('q')
    if query:
        response = New.published.filter(Q(title__icontains=query))

    else:
        response = None
    paginator = Paginator(query,2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "response" : response,
        "page_obj" : page_obj,
    }
    return render(request,"search.html",context)

# Contact view


def contact_view(request):

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("eemail")
        subject = request.POST.get("subject")
        message = request.POST.get("message")


        if not full_name or not email or not subject or not message:
            context = {
                "error" : "Barcha maydonlarini to'ldirishingiz shart"
            }

            return render(request,"contact.html",context)

        Contact.objects.create(
            full_name=full_name,
            email=email,
            subject=subject,
            message=messages,
        )
        BOT_TOKEN="7724414870:AAEMJ4N-cTye2kxB9hZbQBNmUGSx7TRqWG4"
        chat_id="6746520976"

        text=(
            "<b> YANGI MUROJAT !</b>\n\n"
            f"<b> Ismi: !</b>{full_name}\n"
            f"<b> Email: !</b>{email}\n"
            f"<b> Mavzu: !</b>{subject}\n"
            f"<b> Xabar: !</b>{message}\n"
        )

        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={
            "chat_id" : chat_id,
            "text" : text,
            "parse_mode" : "HTML"
        })

        context = {
            'success' : 'Xabaringiz Muvaffaqqiyatli Jonatildi'
        }

        return render(request,'contact.html',context)
    return render(request,"contact.html")



# Advertisemeny

def advertisement_view(request):
    ads = Advertisement.objects.filter(is_active=True).order_by('-id').first()

    context = {
        "ads" : ads
    }

    return render(request,"index.html",context)
