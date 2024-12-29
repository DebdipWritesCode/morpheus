from django.urls import path
from .views import SignupView, LoginView, CreateFormView, GetFormsView

urlpatterns = [
  path('auth/signup', SignupView.as_view(), name='signup'),
  path('auth/login', LoginView.as_view(), name='login'),
  path("/create-form", CreateFormView.as_view(), name="create-form"),
  path("/get-forms", GetFormsView.as_view(), name="get-forms"),
]