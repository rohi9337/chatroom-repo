from django.urls import path
from . import views



urlpatterns = [
    path('',views.getRoutes),
    path('getrooms/',views.roomlist.as_view(), name ="getrooms"),
     path('getroom/<str:pk>/',views.roomlist.as_view(), name ="getroom"),
   ]
