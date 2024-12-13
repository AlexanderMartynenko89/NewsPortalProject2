from django.urls import path
from .views import InputPost, PostDetail


urlpatterns = [
   path('', InputPost.as_view()),
   path('<int:pk>', PostDetail.as_view()),
]