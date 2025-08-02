# 🚀 PrepDyno Flask App Deployment Guide

## 🎯 Best Option: Railway Deployment

Railway is perfect for your Flask app with Firebase authentication. Here's how to deploy:

### 📋 Prerequisites
Your app is already deployment-ready with:
- ✅ `requirements.txt` with all dependencies
- ✅ `Procfile` for web server configuration
- ✅ `runtime.txt` specifying Python version
- ✅ Flask app properly configured

### 🚀 Option 1: Railway Web Dashboard (Recommended - No CLI needed)

#### Step 1: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub (recommended)
3. Verify your account

#### Step 2: Deploy from GitHub
1. **Upload your code to GitHub first:**
   - Create a new repository on GitHub
   - Upload all files from `G:\New folder\` to the repository
   - Make sure to include: `app.py`, `requirements.txt`, `Procfile`, `runtime.txt`, `templates/`, `static/`

2. **Deploy on Railway:**
   - Click "New Project" on Railway dashboard
   - Select "Deploy from GitHub repo"
   - Choose your PrepDyno repository
   - Railway will automatically detect it's a Python app
   - Click "Deploy"

#### Step 3: Configure Environment Variables
1. In Railway dashboard, go to your project
2. Click "Variables" tab
3. Add these environment variables:
   ```
   FLASK_APP=app.py
   FLASK_ENV=production
   PORT=5000
   ```

#### Step 4: Get Your Deployment URL
- Railway will provide a URL like: `https://prepdyno-production-xxxx.up.railway.app`
- Your app will be live at this URL

### 🚀 Option 2: Railway CLI (If you want to install CLI)

#### Install Railway CLI:
```powershell
# Using npm (if you have Node.js)
npm install -g @railway/cli

# Or using PowerShell (Windows)
iwr https://railway.app/install.ps1 | iex
```

#### Deploy with CLI:
```bash
cd "G:\New folder"
railway login
railway init
railway up
```

### 🚀 Option 3: Alternative - Render.com

If Railway doesn't work, try Render:

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Environment**: Python 3

### 🔧 Post-Deployment Steps

#### 1. Fix Firebase Authentication
Once deployed, you'll get a URL like `https://your-app.railway.app`

**Add this domain to Firebase:**
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select project: `tracker-4fd2b`
3. Authentication → Settings → Authorized domains
4. Add your new domain:
   - `your-app.railway.app`
   - `https://your-app.railway.app`

#### 2. Test Your Deployment
1. Visit your deployed URL
2. Test all features:
   - ✅ Landing page loads
   - ✅ Expandable exam cards work
   - ✅ "Start Your Journey" button works
   - ✅ Google Sign-in works (after adding domain to Firebase)
   - ✅ Dashboard and tracker pages work

### 🎯 Expected Results

After deployment:
- **Live URL**: Your app will be accessible worldwide
- **HTTPS**: Automatic SSL certificate
- **Fast**: CDN-powered delivery
- **Scalable**: Handles traffic automatically
- **Firebase Auth**: Works perfectly with your setup

### 🆘 Troubleshooting

#### If deployment fails:
1. Check `requirements.txt` has all dependencies
2. Ensure `Procfile` exists with: `web: gunicorn app:app`
3. Verify `runtime.txt` has: `python-3.11.0`
4. Check Railway logs for specific errors

#### If Google Sign-in still fails:
1. Verify you added the deployed domain to Firebase authorized domains
2. Check browser console for specific Firebase errors
3. Ensure Firebase config is correct in your templates

### 📞 Need Help?

If you encounter any issues:
1. Check Railway/Render deployment logs
2. Verify all files are uploaded correctly
3. Ensure Firebase domains are configured
4. Test locally first to ensure everything works

## 🎉 Success!

Once deployed, your PrepDyno exam tracker will be:
- ✅ Live and accessible worldwide
- ✅ Secure with HTTPS
- ✅ Fast and reliable
- ✅ Ready for users to sign up and track their exam progress

**Your deployed app will have all features:**
- Interactive expandable exam cards
- Firebase Google authentication
- User dashboard and exam selection
- Progress tracking for JEE Advanced, NEET, IAT, UGEE
- Beautiful glassmorphism UI with dark theme
- Responsive design for all devices
