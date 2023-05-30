from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('new', views.new),
    path('create', views.create),
    path('shows', views.shows_page),
    path('shows/new', views.add_show_page),
    path('shows/<int:show_id>', views.show_detail),
    path('shows/<int:show_id>/edit', views.show_edit_page),
    path('shows/<int:show_id>/delete', views.show_delete),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
]
