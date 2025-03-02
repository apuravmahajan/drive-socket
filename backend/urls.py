from django.urls import path, include

urlpatterns = [
    path('auth/', include("oauth.urls")),
    path('drive/', include("drive_app.urls"))
]
