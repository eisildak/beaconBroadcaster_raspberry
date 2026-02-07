# Vercel Deployment Instructions

## Quick Setup (5 minutes)

### 1. Create Vercel Account
- Go to [vercel.com](https://vercel.com)
- Sign up with GitHub (recommended)
- **100% FREE** for personal projects

### 2. Deploy to Vercel

**Option A: Via GitHub (Recommended)**
1. Push this repository to GitHub
2. Go to [vercel.com/new](https://vercel.com/new)
3. Import your GitHub repository
4. Click "Deploy"
5. ✅ Done! Your API is live

**Option B: Via Vercel CLI**
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy from this directory
cd /path/to/BeaconBroadcaster_raspberry
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? (Select your account)
# - Link to existing project? No
# - Project name? beacon-broadcaster-deployer
# - Directory? ./
# - Override settings? No

# Deploy to production
vercel --prod
```

### 3. Get Your API URL
After deployment, Vercel will provide a URL like:
```
https://beacon-broadcaster-deployer.vercel.app
```

Your API endpoint will be:
```
https://beacon-broadcaster-deployer.vercel.app/api/deploy
```

### 4. Update Setup Wizard
Edit `setup-wizard.html` and replace:
```javascript
const VERCEL_API_URL = 'https://YOUR-PROJECT.vercel.app/api/deploy';
```

With your actual Vercel URL:
```javascript
const VERCEL_API_URL = 'https://beacon-broadcaster-deployer.vercel.app/api/deploy';
```

### 5. Test the Deployment
1. Open your GitHub Pages URL
2. Fill in Raspberry Pi details
3. Click "🚀 Deploy via Cloud (Zero-Click)"
4. Wait for deployment to complete
5. Web UI opens automatically!

---

## Vercel Free Tier Limits

✅ **What's Included:**
- 100 GB bandwidth/month
- 100,000 function invocations/month
- Unlimited static hosting
- Automatic HTTPS
- Global CDN

❌ **What's NOT Included:**
- Custom domains (requires paid plan)
- Advanced analytics
- Team collaboration features

**For this project:** FREE tier is more than enough! ✨

---

## Updating the Deployment

When you update code in GitHub:
1. Vercel auto-deploys on every push
2. No manual steps needed
3. Changes live in ~30 seconds

**Manual redeploy:**
```bash
vercel --prod
```

---

## Environment Variables (Optional)

If you want to add extra security:

1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add variables:
   - `MAX_DEPLOYMENTS_PER_HOUR=10` (rate limiting)
   - `ALLOWED_IPS=192.168.*.*` (IP whitelist)
3. Redeploy

---

## Troubleshooting

### "Module not found: node-ssh"
```bash
npm install
vercel --prod
```

### "Build failed"
- Check Node.js version >= 18
- Verify `package.json` is present
- Run `npm install` locally first

### "Function timeout"
- Raspberry Pi is unreachable
- Check IP address and SSH port
- Verify network allows outbound SSH

### "CORS errors"
- Check `vercel.json` headers configuration
- Try clearing browser cache
- Test with `curl` first:
```bash
curl -X POST https://YOUR-PROJECT.vercel.app/api/deploy \
  -H "Content-Type: application/json" \
  -d '{"ip":"192.168.1.100","username":"pi","password":"raspberry"}'
```

---

## Cost Estimate

| Usage | Free Tier | Cost |
|-------|-----------|------|
| 0-100 deploys/month | ✅ Included | $0 |
| 101-1000 deploys/month | ✅ Included | $0 |
| 1000-10000 deploys/month | ⚠️ May exceed | $0-20 |

**Realistic usage:** 10-50 deploys/month = **$0** 💰

---

## Advanced: Custom Domain

If you want `deploy.yourdomain.com`:

1. Buy domain (e.g., Namecheap, $10/year)
2. Vercel Dashboard → Domains → Add
3. Add DNS records as shown
4. ✅ Custom domain active in 5 minutes

**Cost:** $10-15/year for domain only

---

## Security Best Practices

✅ **Built-in Security:**
- HTTPS by default
- Request validation
- No credentials stored
- Isolated function execution

⚠️ **User Responsibility:**
- SSH passwords sent over HTTPS
- Not logged or stored
- Use strong Raspberry Pi passwords
- Consider SSH key authentication (future enhancement)

---

## Monitoring

View deployment logs in real-time:

1. Vercel Dashboard → Your Project → Deployments
2. Click any deployment
3. View function logs
4. See errors and performance metrics

**Logs show:**
- IP addresses connecting
- Deployment success/failures
- SSH connection errors
- Response times

---

## Next Steps

After Vercel is deployed:

1. ✅ Update `setup-wizard.html` with API URL
2. ✅ Git commit and push
3. ✅ GitHub Pages auto-updates
4. ✅ Test full deployment flow
5. 🎉 Share with users!

**Total time:** 15 minutes from start to finish ⚡
