from django.urls import path
from .views import (home_view,detail_page,sport_page,local_page,foreign_page,
                    add_news,texno_page,delete_new,update_new,register_view,login_view,logout_user,search_view,contact_view,
                    advertisement_view)

urlpatterns=[
    path('',home_view,name='home'),
    path('detail/<slug:slug>' , detail_page  ,name='detail'),
    path('sport/' , sport_page , name="sport"),
    path('mahalliy/' , local_page , name="local"),
    path('foreign/' , foreign_page , name="foreign"),
    path('texnologiya/', texno_page ,name="technology"),
    path('add news/', add_news ,name="add_news"),
    path('delete/<int:pk>/',delete_new , name='delete'),
    path('update/<int:pk>/', update_new , name='update'),
    path('register/',register_view,name='register'),
    path('login/',login_view,name='login'),
    path('log out/',logout_user,name="logout"),
    path('search/',search_view,name="search"),
    path('contact/',contact_view,name="contact"),
    path('advertisement/',advertisement_view,name="ads"),
]