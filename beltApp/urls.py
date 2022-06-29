from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path ('register', views.register),
    path ('login', views.login),
    path ('logout', views.logout),
    path('trips', views.success),
    path ('trip', views.trip),
    path ('create', views.create),
    path ('edit/<int:number>', views.edit),
    path ('delete/<int:number>', views.delete),
    path ("info/<int:number>", views.info),
    path("join/<int:number>", views.join),
    path ("cancel/<int:number>", views.cancel),
    path ('update/<int:number>', views.update)
    ]   