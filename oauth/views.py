from django.shortcuts import redirect
from django.http import JsonResponse
from django.conf import settings
import requests
import os

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = "https://backend-project-42w3.onrender.com/auth/callback/"

def google_login(request):
    google_auth_url = (
        "https://accounts.google.com/o/oauth2/auth"
        "?response_type=code"
        f"&client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        "&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email%20"
        "https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile%20"
        "https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive.readonly%20"
        "https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive.file"
        "&access_type=offline"
        "&prompt=consent"
    )
    return redirect(google_auth_url)

def google_callback(request):
    code = request.GET.get("code")
    if not code:
        return JsonResponse({"error": "No code provided"}, status=400)
    
    token_url = "https://oauth2.googleapis.com/token"

    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    response = requests.post(token_url, data=data)
    token_data = response.json()
    if "access_token" not in token_data:
        return JsonResponse({"error": "Failed to fetch access token"}, status=400)
    access_token = token_data["access_token"]
    request.session["access_token"] = access_token

    return JsonResponse({"authorization code": code, "access_token": access_token})
