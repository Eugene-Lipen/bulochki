from django.urls import path
from .views import index, answer, testing

urlpatterns = [
    path('', testing, name='testing'),
    #path('testing/', testing, name='testing'),
    path('answer/', answer, name='answer')


]
