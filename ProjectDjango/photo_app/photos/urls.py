from django.urls import path
from . import views

urlpatterns = [
    path('', views.photo_list, name='photo_list'),
    path('upload/', views.upload_photo, name='upload_photo'),
    path('delete/<int:pk>/', views.delete_photo, name='delete_photo'),
]