from django.urls import path
from . import views

urlpatterns = [
    path('modelpredicrtor', views.predictor, name='model-predictor'),
]
