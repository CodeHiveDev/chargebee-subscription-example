
from django.urls import path
from .views import *
urlpatterns = [
    path("subscription/", PaymentSubscription.as_view()),
    path("get-subscription/", GetCharbeSubscription.as_view()),
    path("accounts/login/", LoginView.as_view()),
    path("accounts/signup/", SignUpView.as_view()),
    path("webhook", PaymetWebHook.as_view())

]
