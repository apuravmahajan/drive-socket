import requests
from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


LOGIN_URL = "http://localhost:8000/auth/login/"
CALLBACK_URL = "http://127.0.0.1:8000/auth/callback/"
    
def con_drive(request):
    return redirect(LOGIN_URL)

def list_drive_files(request):

    access_token = request.session.get("access_token")
    if not access_token:
        access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not access_token:
            return JsonResponse({"error": "User not authenticated"}, status=401)
    
    drive_api_url = "https://www.googleapis.com/drive/v3/files"
    headers = { "Authorization": f"Bearer {access_token}"}

    response = requests.get(drive_api_url, headers = headers)

    return JsonResponse(response.json())

@csrf_exempt
def file_upload(request):
    if request.method == "POST":
        access_token = request.session.get("access_token")
        if not access_token:
            access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
            if not access_token:
                return JsonResponse({"error": "User not authenticated"}, status=401)

        if "file" not in request.FILES:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        uploaded_file = request.FILES["file"]
        file_data = uploaded_file.read()

        metadata = {
        "name": uploaded_file.name,
        "mimeType": uploaded_file.content_type
         }

        drive_api_url = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart"
        headers = { "Authorization": f"Bearer {access_token}",}
        
        files = {
        "metadata": ("metadata", json.dumps(metadata), "application/json"),
        "file": (uploaded_file.name, file_data, uploaded_file.content_type),
        }
        response = requests.post(drive_api_url, headers = headers, files=files)

        if response.status_code != 200:
            return JsonResponse({"error": "Failed to upload file", "details": response.json()}, status=400)

        return JsonResponse(response.json())
    else:
        return render(request, "upload.html")
    
def download_files(request):
   
    access_token = request.session.get("access_token")
    if not access_token:
        access_token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not access_token:
            return JsonResponse({"error": "User not authenticated"}, status=401)

    file_id = request.GET.get("file_id")
    if not file_id:
        return JsonResponse({"error": "File ID is required"}, status=400)

    metadata_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?fields=name,mimeType"
    headers = {"Authorization": f"Bearer {access_token}"}

    metadata_response = requests.get(metadata_url, headers=headers)

    if metadata_response.status_code != 200:
        return JsonResponse({"error": "Failed to fetch file metadata", "details": metadata_response.json()}, status=400)

    metadata = metadata_response.json()
    file_name = metadata.get("name", f"{file_id}.bin")
    mime_type = metadata.get("mimeType", "application/octet-stream")
    google_docs_mime_types = {
        "application/vnd.google-apps.document": "application/pdf",
        "application/vnd.google-apps.spreadsheet": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.google-apps.presentation": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    }

    if mime_type in google_docs_mime_types:
        export_mime_type = google_docs_mime_types[mime_type]
        drive_api_url = f"https://www.googleapis.com/drive/v3/files/{file_id}/export?mimeType={export_mime_type}"
    else:
        drive_api_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
    response = requests.get(drive_api_url, headers=headers, stream=True)

    if response.status_code != 200:
        return JsonResponse({"error": "Failed to download file", "details": response.json()}, status=400)

    response_content = response.content
    response_headers = {
        "Content-Disposition": f'attachment; filename="{file_name}"',
        "Content-Type": mime_type,
    }
    return HttpResponse(response_content, headers=response_headers)
