# PrepDyno Deployment Guide

Your PrepDyno exam preparation platform is ready for deployment! Here are several deployment options:

## Option 1: Render (Recommended - Free Tier Available)

1. **Create a Render account**: Go to [render.com](https://render.com) and sign up
2. **Connect your repository**: 
   - Push your code to GitHub/GitLab
   - Connect your repository to Render
3. **Create a new Web Service**:
   - Choose your repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `python app.py`
   - Set environment to Python 3
4. **Deploy**: Render will automatically deploy your app

## Option 2: Railway (Simple and Fast)

1. **Create Railway account**: Go to [railway.app](https://railway.app)
2. **Deploy from GitHub**:
   - Connect your GitHub repository
   - Railway will auto-detect it's a Python app
   - It will automatically use your `requirements.txt` and `Procfile`
3. **Environment Variables**: Add any needed environment variables
4. **Deploy**: Railway handles the rest automatically

## Option 3: Heroku (Classic Option)

1. **Install Heroku CLI**: Download from [heroku.com](https://devcenter.heroku.com/articles/heroku-cli)
2. **Login and create app**:
   ```bash
   heroku login
   heroku create your-prepdyno-app
   ```
3. **Deploy**:
   ```bash
   git add .
   git commit -m "Deploy PrepDyno"
   git push heroku main
   ```

## Option 4: Vercel (Easy Setup)

1. **Install Vercel CLI**: `npm i -g vercel`
2. **Deploy**: Run `vercel` in your project directory
3. **Follow prompts**: Vercel will guide you through the setup

## Files Created for Deployment

- ✅ `Procfile` - Tells the platform how to run your app
- ✅ `runtime.txt` - Specifies Python version
- ✅ `requirements.txt` - Updated with gunicorn for production

## Important Notes

1. **Firebase Configuration**: Make sure to set up your Firebase config in the deployment platform's environment variables
2. **Static Files**: Your CSS/JS files in templates are embedded, so no additional static file serving needed
3. **Data Persistence**: Currently using JSON files - consider upgrading to a database for production
4. **Domain**: You'll get a free subdomain like `your-app.render.com` or `your-app.railway.app`

## Quick Start (Recommended: Railway)

1. Push your code to GitHub
2. Go to [railway.app](https://railway.app)
3. Click "Deploy from GitHub"
4. Select your repository
5. Your app will be live in minutes!

Your PrepDyno app includes:
- ✨ Modern exam preparation interface
- 🔥 Firebase authentication
- 📊 Progress tracking for JEE, NEET, IAT, UGEE
- 📱 Mobile-responsive design
- 🎯 Complete syllabus coverage

Ready to help thousands of students prepare for their exams! 🚀
