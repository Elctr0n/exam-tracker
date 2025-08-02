# 🔥 Firebase Setup Guide for PrepDyno

This guide will help you set up Firebase Authentication and deploy your PrepDyno application.

## 📋 Prerequisites

- Google account
- Node.js installed (for Firebase CLI)
- Python 3.7+ installed
- Git installed

## 🚀 Step 1: Create Firebase Project

1. **Go to Firebase Console**
   - Visit [https://console.firebase.google.com/](https://console.firebase.google.com/)
   - Sign in with your Google account

2. **Create New Project**
   - Click "Create a project"
   - Enter project name: `prepdyno-app` (or your preferred name)
   - Enable Google Analytics (optional)
   - Click "Create project"

3. **Add Web App**
   - In project overview, click the web icon `</>`
   - Enter app nickname: `PrepDyno Web App`
   - Check "Also set up Firebase Hosting" (for deployment)
   - Click "Register app"

## 🔐 Step 2: Configure Authentication

1. **Enable Authentication**
   - In Firebase console, go to "Authentication" → "Get started"
   - Go to "Sign-in method" tab

2. **Enable Sign-in Providers**
   - **Email/Password**: Click and toggle "Enable" → Save
   - **Google**: Click and toggle "Enable" → Save
   - **GitHub**: 
     - Click and toggle "Enable"
     - You'll need to create a GitHub OAuth App:
       - Go to GitHub Settings → Developer settings → OAuth Apps
       - Create new OAuth App with:
         - Application name: `PrepDyno`
         - Homepage URL: `https://your-project-id.web.app`
         - Authorization callback URL: `https://your-project-id.firebaseapp.com/__/auth/handler`
       - Copy Client ID and Client Secret to Firebase
     - Save

3. **Configure Authorized Domains**
   - In Authentication → Settings → Authorized domains
   - Add your domains:
     - `localhost` (for development)
     - `your-project-id.web.app` (for production)
     - Your custom domain (if any)

## ⚙️ Step 3: Get Firebase Configuration

1. **Get Config Object**
   - Go to Project Settings (gear icon)
   - Scroll down to "Your apps" section
   - Click on your web app
   - Copy the `firebaseConfig` object

2. **Update login.html**
   - Open `templates/login.html`
   - Replace the placeholder config with your actual config:

```javascript
const firebaseConfig = {
    apiKey: "your-actual-api-key",
    authDomain: "your-project-id.firebaseapp.com",
    projectId: "your-project-id",
    storageBucket: "your-project-id.appspot.com",
    messagingSenderId: "your-messaging-sender-id",
    appId: "your-actual-app-id"
};
```

## 🌐 Step 4: Deploy to Firebase Hosting

1. **Install Firebase CLI**
```bash
npm install -g firebase-tools
```

2. **Login to Firebase**
```bash
firebase login
```

3. **Initialize Firebase in Your Project**
```bash
cd "g:\New folder"
firebase init
```

Select:
- ✅ Hosting: Configure files for Firebase Hosting
- Choose your existing project
- Public directory: `public` (we'll create this)
- Single-page app: `No`
- Automatic builds: `No`

4. **Prepare for Deployment**

Create a `public` folder and copy your files:
```bash
mkdir public
```

Copy these files to `public/`:
- All HTML templates (rename to remove `templates/` prefix)
- `app.py` (for reference, but won't run on Firebase Hosting)
- Any static assets

5. **Create firebase.json Configuration**
```json
{
  "hosting": {
    "public": "public",
    "ignore": [
      "firebase.json",
      "**/.*",
      "**/node_modules/**"
    ],
    "rewrites": [
      {
        "source": "**",
        "destination": "/index.html"
      }
    ]
  }
}
```

6. **Deploy**
```bash
firebase deploy
```

## 🐍 Step 5: Deploy Flask Backend (Alternative Options)

Since Firebase Hosting only serves static files, you have several options for your Flask backend:

### Option A: Google Cloud Run
1. Create `requirements.txt`:
```
Flask==2.3.3
gunicorn==21.2.0
```

2. Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
```

3. Deploy to Cloud Run:
```bash
gcloud run deploy prepdyno-api --source . --platform managed --region us-central1 --allow-unauthenticated
```

### Option B: Heroku
1. Create `Procfile`:
```
web: gunicorn app:app
```

2. Deploy to Heroku:
```bash
heroku create prepdyno-app
git push heroku main
```

### Option C: Vercel
1. Create `vercel.json`:
```json
{
  "functions": {
    "app.py": {
      "runtime": "python3.9"
    }
  },
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

2. Deploy:
```bash
npm i -g vercel
vercel
```

## 🔒 Step 6: Security Rules & Environment Variables

1. **Environment Variables**
   - Never commit Firebase config to public repositories
   - Use environment variables in production:

```python
import os
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key')

# Firebase Admin SDK (optional for server-side verification)
FIREBASE_PROJECT_ID = os.environ.get('FIREBASE_PROJECT_ID')
```

2. **Firebase Security Rules**
   - Set up Firestore rules (if using Firestore for data storage)
   - Configure Authentication rules

## 📱 Step 7: Testing

1. **Local Testing**
```bash
python app.py
```
Visit `http://localhost:5000`

2. **Production Testing**
   - Test all authentication methods
   - Verify redirects work correctly
   - Test on different devices/browsers

## 🛠️ Step 8: Additional Features

### Enable Firestore (Optional - for user data storage)
1. Go to Firestore Database → Create database
2. Choose production mode
3. Select location
4. Set up security rules

### Enable Cloud Functions (Optional - for backend logic)
1. Upgrade to Blaze plan
2. Initialize Cloud Functions:
```bash
firebase init functions
```

### Analytics & Performance
1. Enable Google Analytics
2. Add Performance Monitoring
3. Set up Crashlytics

## 🔧 Troubleshooting

### Common Issues:

1. **CORS Errors**
   - Add your domain to Firebase authorized domains
   - Check browser console for specific errors

2. **Authentication Popup Blocked**
   - Ensure popup blockers are disabled
   - Use redirect method instead of popup

3. **Deployment Issues**
   - Check Firebase CLI version: `firebase --version`
   - Verify project ID: `firebase projects:list`
   - Clear cache: `firebase hosting:channel:delete preview`

4. **Flask Backend Issues**
   - Check Python version compatibility
   - Verify all dependencies in requirements.txt
   - Test locally before deploying

## 📞 Support

- Firebase Documentation: [https://firebase.google.com/docs](https://firebase.google.com/docs)
- Flask Documentation: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
- GitHub Issues: Create issues in your repository

## 🎉 Success!

Once completed, your PrepDyno app will be:
- ✅ Deployed on Firebase Hosting
- ✅ Authenticated with Firebase Auth
- ✅ Accessible worldwide
- ✅ Scalable and secure

Your app URLs:
- **Production**: `https://your-project-id.web.app`
- **Preview**: `https://your-project-id--preview.web.app`

---

**Happy Learning! 🚀📚**
