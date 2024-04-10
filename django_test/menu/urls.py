from django.urls import path

from .views import IndexView, SecondPageView

urlpatterns = [
    path('', IndexView.as_view()),
    path('second/', SecondPageView.as_view())
]
