from django.urls import path

from . import views

# you could do 1 for each month
# path("Jan", views.jan), path("Feb", views.feb),
# but better to do dynamic not(str: ensures value is string)

# <anything> handles all urls
urlpatterns = [
    path("", views.index, name="index"),  # /testapp/
]
