from django.urls import path
from .views import SignupView, LoginView, CreateFormView, GetFormsView, SubmitResponseView, ShowAnalyticsView, GetFormView

urlpatterns = [
  path('auth/signup', SignupView.as_view(), name='signup'),
  path('auth/login', LoginView.as_view(), name='login'),
  path("create-form", CreateFormView.as_view(), name="create-form"),
  path("get-forms", GetFormsView.as_view(), name="get-forms"),
  path("/get-form/<int:form_id>", GetFormView.as_view(), name="get-form"),
  path("submit-response", SubmitResponseView.as_view(), name="submit-response"),
  path("show-analytics/<int:form_id>", ShowAnalyticsView.as_view(), name="show-analytics"),
]