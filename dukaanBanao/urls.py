from django.urls import path
from . import views

urlpatterns = [

    # ACCOUNT ACCESS
    path('account/', views.accountAPIView.as_view()),
    path('account/<int:id>', views.accountAPIView.as_view()),

    # STORE CREATION AND ACCESS
    path('createstore/', views.storeAPIView.as_view()),
    path('viewstores/<int:id>', views.storeAPIView.as_view()),
    path('viewstores/', views.storeAPIView.as_view()),

    # PRODUCT ADDITION AND FETCHING
    path('product/', views.productAPIView.as_view()),

    path('category/', views.categorisedView.as_view()),

    path('customer/', views.customerAPIView.as_view()),
    path('customer/<int:id>', views.customerAPIView.as_view()),
    path('order/', views.orderView.as_view()),
    path('cart/', views.cartView.as_view()),
    path('placeorder/', views.placeOrderAPIView.as_view()),
    path('storedisplay/', views.StoreDisplayAPIView.as_view()),
]