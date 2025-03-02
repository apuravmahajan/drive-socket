from oauth.views import google_login
from django.urls import path, include

urlpatterns = [
    path('', google_login, name="google_login"),
    path('auth/', include("oauth.urls")),
    path('drive/', include("drive_app.urls"))
]
