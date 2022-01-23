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
    path('media/*', views.productAPIView.as_view()),
]