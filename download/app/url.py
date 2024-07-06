from django.urls import path 
from  . import views

urlpatterns = [
  path('',views.download,name= 'download'),
  path('download/',views.process_video,name= 'process_video'),
  path('download_video/<path:youtube_url>/<int:itag>/', views.download_video, name='download_video'),
]