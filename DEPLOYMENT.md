# Streamlit Cloud Deployment Guide

Your Commercial Real Estate Investment Analyzer is now on GitHub and ready to deploy to Streamlit Cloud!

## Repository Information

- **GitHub User**: arstraus
- **Repository**: realestate
- **URL**: https://github.com/arstraus/realestate

## Deploy to Streamlit Cloud

### Step 1: Access Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account (arstraus)

### Step 2: Deploy New App

1. Click **"New app"** button
2. Fill in the deployment settings:
   - **Repository**: `arstraus/realestate`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL** (optional): Choose a custom subdomain like `cre-analyzer`

### Step 3: Advanced Settings (Optional)

Click "Advanced settings" if you want to customize:
- **Python version**: 3.11 (recommended)
- **Secrets**: Not needed for this app
- **Resources**: Default (1 CPU, 800MB RAM) should work fine

### Step 4: Deploy

Click **"Deploy!"** and wait 2-5 minutes for the app to build and launch.

## Your App Will Be Live At:

```
https://[your-chosen-name].streamlit.app
```

Or the default:
```
https://arstraus-realestate-app-[random].streamlit.app
```

## What's Included

All files have been pushed to GitHub:
- ✅ `app.py` - Main application
- ✅ `requirements.txt` - Python dependencies
- ✅ `.streamlit/config.toml` - Theme and server configuration
- ✅ `README.md` - Full documentation
- ✅ `QUICKSTART.md` - Quick start guide
- ✅ `.gitignore` - Git ignore rules
- ✅ `warehouse_investment_model (2).xlsx` - Example Excel file

## Post-Deployment

### Testing Your Deployment

1. Open the app URL
2. Verify all tabs load correctly
3. Test Save/Load functionality (scenarios save in-memory on Streamlit Cloud)
4. Try adjusting inputs and viewing calculations
5. Test CSV export downloads

### Sharing Your App

Share your live app URL with:
- Investors
- Team members
- Real estate professionals
- Clients

No installation required - they just open the link!

## Streamlit Cloud Features

### Free Tier Includes:
- 1 public app
- Automatic GitHub sync
- HTTPS by default
- Community support

### Automatic Updates

When you push changes to GitHub:
```bash
git add .
git commit -m "Update description"
git push
```

Streamlit Cloud will automatically rebuild and redeploy your app!

## Managing Your App

From the Streamlit Cloud dashboard you can:
- **Reboot** - Restart the app
- **View logs** - Debug issues
- **Analytics** - See usage stats
- **Settings** - Update configuration
- **Delete** - Remove the app

## Troubleshooting

### App Won't Start

**Check the logs** in Streamlit Cloud dashboard for errors.

Common issues:
1. **Missing dependencies**: Update `requirements.txt`
2. **Python version**: Ensure 3.8+ in advanced settings
3. **Import errors**: Check all imports in `app.py`

### Scenarios Not Persisting

On Streamlit Cloud, the file system is ephemeral. Scenarios saved during a session will be lost on reboot. For persistent storage, consider:
- Using Streamlit's `st.session_state` (current approach)
- Integrating cloud storage (S3, Google Cloud Storage)
- Using a database (optional enhancement)

### Performance Issues

If the app is slow:
1. Reduce sensitivity analysis grid size
2. Optimize calculations in `CREAnalyzer` class
3. Consider caching with `@st.cache_data`
4. Upgrade to paid Streamlit Cloud tier for more resources

## Advanced: Local Development

### Making Changes

1. Edit files locally
2. Test locally: `streamlit run app.py`
3. Commit: `git add . && git commit -m "Your message"`
4. Push: `git push`
5. Wait for auto-deployment on Streamlit Cloud

### Branch Protection

For production apps, consider:
```bash
# Create development branch
git checkout -b dev
# Make changes and push to dev
git push -u origin dev
# Merge to main when ready
git checkout main
git merge dev
git push
```

## Custom Domain (Optional)

You can use a custom domain:
1. Go to app settings in Streamlit Cloud
2. Add your custom domain
3. Update DNS records as instructed
4. Your app will be at `app.yourdomain.com`

## Monitoring

Keep track of:
- **App health**: Check dashboard regularly
- **User feedback**: Monitor usage patterns
- **Error logs**: Review for issues
- **Performance**: Watch response times

## Support

- **Streamlit Docs**: https://docs.streamlit.io
- **Streamlit Forum**: https://discuss.streamlit.io
- **GitHub Issues**: Create issues in your repo

---

## Next Steps

1. ✅ Repository pushed to GitHub
2. 🔄 Deploy to Streamlit Cloud (follow steps above)
3. 📊 Test the live app
4. 🔗 Share with your team
5. 🚀 Start analyzing real estate deals!

**Your app is ready to go live!** 🎉

