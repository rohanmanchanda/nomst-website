# 🚀 Deployment Guide: Vedic Astrology Dating App

## Prerequisites
- GitHub account
- Vercel account (free)
- OpenAI API key

## Step 1: Create GitHub Repository

### 1.1 Initialize Git Repository
```bash
cd "your-project-folder"
git init
git add .
git commit -m "Initial commit: Vedic astrology dating app"
```

### 1.2 Create GitHub Repository
1. Go to [GitHub.com](https://github.com)
2. Click **"New Repository"**
3. Name it: `vedic-astrology-dating-app`
4. Set to **Public** (required for free Vercel)
5. Click **"Create Repository"**

### 1.3 Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/vedic-astrology-dating-app.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy to Vercel

### 2.1 Connect to Vercel
1. Go to [Vercel.com](https://vercel.com)
2. Sign up/login with GitHub
3. Click **"New Project"**
4. Import your `vedic-astrology-dating-app` repository

### 2.2 Configure Project Settings
- **Framework Preset:** Other
- **Root Directory:** ./
- **Build Command:** (leave empty)
- **Output Directory:** (leave empty)

### 2.3 Add Environment Variables
In Vercel project settings:
1. Go to **Settings** → **Environment Variables**
2. Add: `OPENAI_API_KEY` = `your_actual_openai_api_key`
3. Click **"Save"**

### 2.4 Deploy
- Click **"Deploy"**
- Wait 2-3 minutes for deployment
- Your app will be live at: `your-app-name.vercel.app`

## Step 3: Alternative Hosting Options

### 3.1 Netlify Deployment
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
netlify deploy --dir=.
netlify deploy --prod
```

### 3.2 Heroku Deployment
Create `Procfile`:
```
web: python app.py
```

Deploy:
```bash
heroku create your-app-name
heroku config:set OPENAI_API_KEY=your_key
git push heroku main
```

## Step 4: Custom Domain (Optional)

### 4.1 In Vercel Dashboard
1. Go to **Settings** → **Domains**
2. Add your custom domain
3. Update DNS records as instructed

## Step 5: Monitoring & Updates

### 5.1 Automatic Deployments
- Every push to `main` branch auto-deploys
- Check deployment status in Vercel dashboard

### 5.2 Environment Variables
- Update API keys in Vercel settings
- Changes take effect on next deployment

## Troubleshooting

### Common Issues:
1. **Build fails**: Check requirements.txt versions
2. **API errors**: Verify OPENAI_API_KEY is set
3. **Import errors**: Ensure all files are committed

### Support:
- Vercel Docs: https://vercel.com/docs
- GitHub Issues: Create issues in your repo

## Live Example
Once deployed, your app will be accessible at:
`https://your-app-name.vercel.app`

## Security Notes
- Never commit `.env` files
- Use environment variables for API keys
- Enable HTTPS (automatic on Vercel) 