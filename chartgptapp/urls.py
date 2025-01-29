from django.urls import path

from chartgptapp import views

urlpatterns = [
    path('api/UserType/create/', views.UPLOADPDFCHARTGPT.as_view(), name='uploadpdfapi'),
]