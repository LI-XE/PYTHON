from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login_view),
    path('logout', views.logout_user),
    path('books', views.dashboard),
    path('books/add', views.add_book),
    path('books/<int:book_id>', views.book_detail),
    path('books/<int:book_id>/add/review', views.book_detail),
    path('books/<int:book_id>/delete/<int:review_id>', views.review_delete),
    path('users/<int:user_id>', views.user_page),
]
