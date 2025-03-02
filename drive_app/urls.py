from .views import list_drive_files, con_drive, file_upload, download_files
from django.urls import path


urlpatterns = [
    path("connect/", con_drive, name = "drive_connect"),
    path("files/", list_drive_files, name = "list_drive_files"),
    path("upload/", file_upload, name = "file_upload"),
    path("download/", download_files, name = "download_files")
]