from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:note_id>/edit/', views.edit, name='edit'),
    path('<int:note_id>/delete/', views.delete, name='delete'),
    path('tags/', views.tags, name='tags'),
    path('tags/<int:tag_id>/', views.tag_detail, name='tag_detail'),
]
