from django.urls import path
#from django.contrib import admin

from .views import GrupMovimentView, GrupMovimentNew, GrupMovimentEdit, GrupMovimentDelete, grupMoviment_inactivar, \
SubgrupMovimentView, SubgrupMovimentNew, SubgrupMovimentEdit, SubgrupMovimentDelete, subgrupMoviment_inactivar, \
DetallMovimentView, DetallMovimentNew, DetallMovimentEdit, DetallMovimentDelete, detallMoviment_inactivar,  \
FormaPagamentView, FormaPagamentNew, FormaPagamentEdit, FormaPagamentDelete, formaPagament_inactivar, \
CaixaView, CaixaNew, CaixaEdit, CaixaDelete, caixa_inactivar, caixa_usuaris, caixa_usuari_canvia_estat


urlpatterns = [
    path('grupsDeMoviments/', GrupMovimentView.as_view(), name='grupMoviment_list'),
    path('grupsDeMoviments/new', GrupMovimentNew.as_view(), name='grupMoviment_new'),
    path('grupsDeMoviments/edit/<int:pk>',
         GrupMovimentEdit.as_view(), name='grupMoviment_edit'),
    path('grupsDeMoviments/delete/<int:pk>',
         GrupMovimentDelete.as_view(), name='grupMoviment_del'),
    path('grupsDeMoviments/inactivar/<int:id>',
         grupMoviment_inactivar, name='grupMoviment_inactivar'),
    
    
    path('subgrupsDeMoviments/', SubgrupMovimentView.as_view(), name='subgrupMoviment_list'),
    path('subgrupsDeMoviments/new', SubgrupMovimentNew.as_view(), name='subgrupMoviment_new'),
    path('subgrupsDeMoviments/edit/<int:pk>',
         SubgrupMovimentEdit.as_view(), name='subgrupMoviment_edit'),
    path('subgrupsDeMoviments/delete/<int:pk>',
         SubgrupMovimentDelete.as_view(), name='subgrupMoviment_del'),
    path('subgrupsDeMoviments/inactivar/<int:id>',
         subgrupMoviment_inactivar, name='subgrupMoviment_inactivar'),
    
    
    path('detallsDeMoviments/', DetallMovimentView.as_view(), name='detallMoviment_list'),
    path('detallsDeMoviments/new', DetallMovimentNew.as_view(), name='detallMoviment_new'),
    path('detallsDeMoviments/edit/<int:pk>',
         DetallMovimentEdit.as_view(), name='detallMoviment_edit'),
    path('detallsDeMoviments/delete/<int:pk>',
         DetallMovimentDelete.as_view(), name='detallMoviment_del'),
    path('detallsDeMoviments/inactivar/<int:id>',
         detallMoviment_inactivar, name='detallMoviment_inactivar'),
    
    
    path('formaPagaments/', FormaPagamentView.as_view(), name='formaPagament_list'),
    path('formaPagaments/new', FormaPagamentNew.as_view(), name='formaPagament_new'),
    path('formaPagaments/edit/<int:pk>',
         FormaPagamentEdit.as_view(), name='formaPagament_edit'),
    path('formaPagaments/delete/<int:pk>',
         FormaPagamentDelete.as_view(), name='formaPagament_del'),
    path('formaPagaments/inactivar/<int:id>',
         formaPagament_inactivar, name='formaPagament_inactivar'),
    
    
    path('caixes/', CaixaView.as_view(), name='caixa_list'),
    path('caixes/new', CaixaNew.as_view(), name='caixa_new'),
    path('caixes/edit/<int:pk>',
         CaixaEdit.as_view(), name='caixa_edit'),
    path('caixes/delete/<int:pk>',
         CaixaDelete.as_view(), name='caixa_del'),
    path('caixes/inactivar/<int:id>',
         caixa_inactivar, name='caixa_inactivar'),    
    path('caixes/usuaris/<int:id>',
         caixa_usuaris, name='caixa_usuaris'),
    path('caixes/usuarisestat/<int:id>',
         caixa_usuari_canvia_estat, name='caixa_canvia_estat'),               
]