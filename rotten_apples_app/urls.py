from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('login',views.login),
    path('register',views.register),
    path('hub',views.hub),
    path('logout',views.logout),
    path('addgame',views.addgame),
    path('newgame',views.newgame),
    path('<int:game_id>',views.showgame),
    path('<int:game_id>/edit',views.edit),
    path('<int:game_id>/update',views.update),
    path('<int:game_id>/delete',views.delete),
    path('create_post/<int:id>',views.create_post),
    path('delete/<int:id>',views.delete_post),
    path('like/<int:id>',views.add_like),
]