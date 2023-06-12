from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    # path('books', views.),
    path('books/add', views.add_book),
    path('books/<int:book_id>', views.book_detail),
    path('books/<int:book_id>/add/review', views.book_detail),
]
