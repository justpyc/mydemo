from django.urls import path
from myapp import views

urlpatterns = [
    path("index", views.index, name="index"),
    path("list-files", views.list_files, name="list-files"),
    path("api/v1/upload-file", views.upload_file, name="upload-file"),
    path("api/v1/execute", views.execute_file, name="execute-file"),
]