from django.urls import path, include

from . import views

app_name = 'Moody'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('customers/', views.CustomersView.as_view(), name='customers'),
    path('new_cust/', views.new_cust, name='new_cust'),
    path('save_new_cust/', views.save_new_cust, name='save_new_cust'),
    path('<str:custname>/', views.PlatesView.as_view(), name='plates'),
    path('<str:custname>/new_plate/', views.new_plate, name='new_plate'),
    path('<str:custname>/save_new_plate/', views.save_new_plate, name='save_new_plate'),
    path('<str:custname>/<str:id_no>/', views.VerifsView.as_view(), name='verifs'),
    path('<str:custname>/<str:id_no>/new_verif/', views.NewVerifView.as_view(), name='new_verif'),
    path('<str:custname>/<str:id_no>/save_new_verif/', views.save_new_verif, name='save_new_verif'),
    path('<str:custname>/<str:id_no>/<str:ver_id>/', views.SummaryView.as_view(), name='summary'),
    path('<str:custname>/<str:id_no>/<str:ver_id>/map', views.CanvasView.as_view(), name='canvas'),
    path('<str:custname>/<str:id_no>/<str:ver_id>/heights', views.HeightsView.as_view(), name='heights'),
]
