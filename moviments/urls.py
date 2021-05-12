from django.urls import path
from django.conf.urls import url
#from django.contrib import admin

from .views import MovimentView, MovimentNew, MovimentEdit,  MovimentDelete, movimentDuplicate,\
     dashboardMoviments2, treeMapDespesa, dashboardSaldo, dashboardDespesa


urlpatterns = [
    path('moviment/', MovimentView.as_view(), name='moviment_list'),
    path('moviment/new', MovimentNew.as_view(), name='moviment_new'),
    path('moviment/edit/<int:pk>',MovimentEdit.as_view(), name='moviment_edit'),
    path('moviment/delete/<int:pk>',  MovimentDelete.as_view(), name='moviment_del'),
    path('moviment/duplicate/<int:id>', movimentDuplicate, name='moviment_duplicate'),
    
    path('moviment/dashboard/<int:year>', dashboardMoviments2, name='moviment_dash'),
    path('moviment/dashboard',  dashboardMoviments2, name='moviment_dash'),
    path('moviment/dashboardtree/<int:year>', treeMapDespesa, name='moviment_tree'),
    path('moviment/dashboardtree', treeMapDespesa, name='moviment_tree'),
    url('moviment/dashboardtree/(?P<dataInici>\d{4}-\d{2}-\d{2})/(?P<dataFi>\d{4}-\d{2}-\d{2})', treeMapDespesa, name='moviment_tree'),
    
    
    path('moviment/dashboardsaldo', dashboardSaldo, name='dashboard_saldo'),
    path('moviment/dashboardsaldo/<int:year>/<int:month>', dashboardSaldo, name='dashboard_saldo'),
    
    
    path('moviment/dashboarddespesa', dashboardDespesa, name='dashboard_despesa'),
    path('moviment/dashboarddespesa/<int:year>/<int:month>', dashboardDespesa, name='dashboard_despesa'),
    
    #path('moviment/dashboardtree/^(<dateStart>\d{4}-\d{2}-\d{2})/^(<dateEnd>\d{4}-\d{2}-\d{2})', treeMapDespesa, name='moviment_tree'),
    
    
    
    #url(r'^(?P<date>\d{4}-\d{2}-\d{2})/$', views.index, name='index'),
 ]