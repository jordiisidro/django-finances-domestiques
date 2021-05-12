from django.urls import path

from .views import usuari_edit

urlpatterns = [
    path('usuari/edit/<int:id>',
         usuari_edit, name='usuari_edit'),
    
]