"""dresses URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from dresses import views
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
urlpatterns = [
    path('admin/', admin.site.urls),
    path('dresses/', views.dress_list),
    path('dresses/<int:id>', views.dress_detail),
    path('dreses/<int:id>', views.drs),
    path('brands/', views.brand_list),
    #path('brands/1/<int:id>', views.nouu),
    path('brands/<int:id>/', views.brand_detail),
    path('showss/', views.redcarpetpres_list),
    path('shows/<int:id>', views.redcarpetpres_detail),
    path('pres/', views.show_event_list),
    path('pres/<int:id>', views.show_event_detail),
    path('brands/filter/<int:nr_models>', views.filter_brands),
    path('pres/report/', views.show_average_pieces),
    path('dress/report/models/', views.ReportModels.as_view()),
    path('brands-ordered-by-nr-models', views.FilterModels.as_view()),
    path('pres/report/guests/', views.ReportGuests.as_view()),
    path('dress/<int:pk>/presentation/', views.PresentationForDress.as_view()),
    path('presentation/<int:pk>/dress/', views.DressForPresentation.as_view()),
    #path('brand/add/multiple/', views.post),
    path('brands/<int:pk>/dresses/', views.DressBrandView.as_view())
]
