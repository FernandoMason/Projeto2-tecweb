from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:note_id>/edit/', views.edit, name='edit'),
    path('<int:note_id>/delete/', views.delete, name='delete'),
]
