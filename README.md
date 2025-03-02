# 🚀 Django Google Drive API & WebSockets Integration

This project integrates **Google OAuth 2.0**, **Google Drive API**, and **WebSockets (Django Channels)** to handle authentication, file management, and real-time chat communication.

## 📌 Features  
✅ **Google OAuth 2.0** – Authenticate users and retrieve access tokens  
✅ **Google Drive API** – Upload, list, and download files  
✅ **WebSockets (Django Channels)** – Real-time chat between two preconfigured users  
✅ **Postman Collection** – Ready-to-use API requests for testing  

---

## 🔧 **Tech Stack**  
- **Backend**: Django, Django Channels (for WebSockets)  
- **Authentication**: Google OAuth 2.0  
- **APIs**: Google Drive API  
- **Deployment**: Render  

---

## 🚀 **Live Demo & API Base URL**  
🌍 **Live API**: [`https://backend-project-42w3.onrender.com`](https://backend-project-42w3.onrender.com)

---

## **Steps to follow in browser**

### **1. Login**
go to /auth/login. after successful login, you will receive a json response containing authentication code and access token

### **2. View Files**
go to /drive/files and you will receive a JSON response

### **3. Upload Files**
go to /drive/upload and upload file and send it. you will receive id, type, and name as JSON response. Copy this id or any other file's id

### **4. Download Files**
go to /drive/download/?file_id={copied-file-id}

### **5. Postman Collection**
a postman collection is available in this repo. generate access token and use it to perform tests.

## **Test Web Socket**
Make two web socket requests from Postman to [`ws://backend-project-42w3.onrender.com/ws/chat/`](ws://backend-project-42w3.onrender.com/ws/chat/)
Send messages in this format from both:
{"sender":"User1","message":"Hello"}
You can switch between User1 and User2
