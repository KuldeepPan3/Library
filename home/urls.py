"""
URL configuration for lms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from home import views
from django.contrib import admin

#Django admin panel Customization

admin.site.site_header = "Library Admin Panel"
admin.site.site_title = "My Library"
admin.site.index_title = "Welcome to the Library Management"

urlpatterns = [
    path('', views.home, name='home'),
    path('books', views.books, name='books'),
    path('logins', views.logins, name='logins'),
    path('registration', views.registration, name='registration'),
    path('issue', views.issue, name='issue'),
    path('return_item', views.return_item, name='return_item'),
    path('logout', views.logout, name='logout'),

]
