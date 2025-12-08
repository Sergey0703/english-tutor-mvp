# Quick Reference - English Tutor MVP

## 🚀 Deploy Commands

```bash
# Check status
git status

# Commit changes
git add .
git commit -m "Your message"

# Push to both remotes
git push github main && git push hf main

# Force push (if needed)
git push --force hf main
```

---

## 🔍 Monitoring

### HF Spaces Status
```bash
# Health check
curl -I https://sergey0703-english-tutor-mvp.hf.space

# Open Space dashboard
start https://huggingface.co/spaces/sergey070373/english-tutor-mvp
```

### GitHub Actions
```bash
# Open actions page
start https://github.com/Sergey0703/english-tutor-mvp/actions
```

---

## 🧪 Testing

### LiveKit Playground
1. Open: https://agents-playground.livekit.io
2. Enter:
   - URL: `wss://first-aaelw7kf.livekit.cloud`
   - API Key: `APICpeSck5jt2Rm`
   - API Secret: `t4jZk0X3wGLvLAwh0d4iigxmrWLkrdEsmwe7FkDVYLT`
3. Click "Connect"
4. Enable microphone
5. Say: "Hello" or wait for agent greeting

---

## 📝 Environment Variables (HF Secrets)

```bash
LIVEKIT_URL=wss://first-aaelw7kf.livekit.cloud
LIVEKIT_API_KEY=APICpeSck5jt2Rm
LIVEKIT_API_SECRET=t4jZk0X3wGLvLAwh0d4iigxmrWLkrdEsmwe7FkDVYLT
GOOGLE_API_KEY=AIzaSyAl-tyw_n8fKEnBO87_BINP1EHPaUeHhrg
```

**Optional (N8N):**
```bash
N8N_WEBHOOK_URL=http://localhost:5678/webhook/get-news
```

---

## 🔄 Switch Between Dockerfiles

### Use N8N version (current):
```bash
# Already active
# See: Dockerfile
```

### Switch to Simple version (no N8N):
```bash
# Backup current
mv Dockerfile Dockerfile.with-n8n

# Use simple
mv Dockerfile.simple Dockerfile

# Deploy
git add Dockerfile
git commit -m "Switch to simple Dockerfile (no N8N)"
git push github main && git push hf main
```

### Switch back to N8N:
```bash
# Restore N8N version
mv Dockerfile Dockerfile.simple
mv Dockerfile.with-n8n Dockerfile

# Deploy
git add Dockerfile
git commit -m "Restore N8N Dockerfile"
git push github main && git push hf main
```

---

## 📊 Logs Analysis

### What to look for in HF Spaces logs:

**✅ Good signs:**
```
[supervisord] INFO Entered RUNNING state
[n8n] INFO n8n ready on http://0.0.0.0:5678
[livekit-agent] INFO 🚀 Starting English Tutor Agent
[livekit-agent] INFO Worker registered with LiveKit
[livekit-agent] INFO ✅ Got news from N8N
```

**❌ Bad signs:**
```
[supervisord] FATAL Exited too quickly
[n8n] ERROR Cannot find module
[livekit-agent] ERROR Failed to connect to LiveKit
[livekit-agent] ERROR Google API error: 401
[livekit-agent] ❌ Cannot connect to N8N webhook
```

---

## 🛠️ Troubleshooting

### Build timeout (>30 min)
**Cause:** Docker image too large
**Fix:** Switch to Dockerfile.simple

### N8N not starting
**Cause:** Node.js install failed or OOM
**Fix:** Check logs, or remove N8N

### Agent can't connect to LiveKit
**Cause:** Wrong credentials or network issue
**Fix:** Check Secrets in HF Spaces

### Audio choppy/slow
**Cause:** CPU throttling or cold start
**Fix:** Wait 2-3 minutes, or upgrade HF tier

---

## 📦 File Structure

```
c:\projects\aijarvis\
├── agent.py                    # Main agent code
├── requirements.txt            # Python deps
├── Dockerfile                  # Current (with N8N)
├── Dockerfile.simple           # Fallback (no N8N)
├── supervisord.conf            # Process manager
├── .env.example                # Env template
├── .gitignore                  # Git ignore
├── README.md                   # Project overview
├── CLAUDE.md                   # AI instructions
├── STATUS.md                   # Current status
├── QUICK_REFERENCE.md          # This file
├── POST_DEPLOY_CHECKLIST.md   # After deploy steps
├── N8N_HF_SPACES_SETUP.md     # N8N limitations
├── N8N_WORKFLOWS_IMPORT.md    # Import guide
├── .github/workflows/
│   └── keep_alive.yml         # Keep-alive job
└── n8n_workflows/
    ├── README.md              # Workflows docs
    ├── rss_news_scraper.json  # RSS workflow (gitignored)
    └── get_random_news_api.json # API workflow (gitignored)
```

---

## 🔗 Important URLs

### Project:
- **GitHub:** https://github.com/Sergey0703/english-tutor-mvp
- **HF Space:** https://huggingface.co/spaces/sergey070373/english-tutor-mvp
- **Live URL:** https://sergey0703-english-tutor-mvp.hf.space

### External Services:
- **LiveKit Cloud:** https://cloud.livekit.io/
- **Google AI Studio:** https://aistudio.google.com/apikey
- **LiveKit Playground:** https://agents-playground.livekit.io

### Documentation:
- **LiveKit Agents:** https://docs.livekit.io/agents/
- **N8N Docs:** https://docs.n8n.io/
- **HF Spaces Docs:** https://huggingface.co/docs/hub/spaces

---

## ⚡ Common Tasks

### Update Google API Key
1. Create new key: https://aistudio.google.com/apikey
2. Open HF Space settings: https://huggingface.co/spaces/sergey070373/english-tutor-mvp/settings
3. Tab "Variables and secrets"
4. Update `GOOGLE_API_KEY`
5. Restart Space

### Check if Space is sleeping
```bash
curl -I https://sergey0703-english-tutor-mvp.hf.space

# If returns 503 → sleeping
# Click "Restart Space" on HF dashboard
```

### Force rebuild
```bash
# Make dummy change
echo "# rebuild" >> README.md
git add README.md
git commit -m "Force rebuild"
git push hf main

# Then revert
git revert HEAD
git push hf main
```

---

## 📅 Maintenance Schedule

### Daily:
- ✅ Check HF Spaces status (automated via GitHub Actions)

### Weekly:
- ✅ Review logs for errors
- ✅ Test voice agent functionality
- ✅ Check Google API quota usage

### Monthly:
- ✅ Update dependencies (pip, npm)
- ✅ Review and optimize Docker image size
- ✅ Backup N8N workflows (if using)

---

**Last Updated:** 2025-12-08 06:40 UTC
