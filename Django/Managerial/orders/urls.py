from . import views
from django.urls import path


urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),

    # customer-list

    path('customer-list/', views.customer_list, name='customer-list'),

    #  customer-detail
    
    path('customer-detail/<int:pk>/', views.customer_detail, name='customer-detail'),

    #  worker_list

    path('worker-list/', views.worker_list, name='worker-list'), 

    #  order_list

    path('order-list/', views.order_list, name='order-list'),

    #  order_detail

    path('order-detail/<int:pk>', views.order_detail, name='order-detail'),

    #  create-order
    
    path('create_order/', views.create_order, name='create-order'),

    #  create-customer
    
    path('create_customer/', views.create_customer, name='create-customer'),

     #  create-worker
        
    path('create_worker/', views.create_worker, name='create-worker'),

        #  order-list
                
    path('order_list/', views.order_list, name='order-list'),

    # customer-list

     path('customer_list/', views.customer_list, name='customer-list'),
]


