
from django.urls import path
from .views import signup,login,otp_ver,FileUploadView,download_file
urlpatterns = [
    path('signup/',signup),
    path('login/',login),
    path('email_ver/',otp_ver),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('download/<int:file_id>/', download_file, name='download_file'),
]