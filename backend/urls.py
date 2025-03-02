from oauth.views import GoogleLoginView
from django.urls import path, include

urlpatterns = [
    path('/', GoogleLoginView, name="google_login"),
    path('auth/', include("oauth.urls")),
    path('drive/', include("drive_app.urls"))
]
