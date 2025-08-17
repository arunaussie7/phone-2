#!/usr/bin/env python3
"""
Phone 2 Control Interface
Phone 2 users access this web page, then Phone 1 can control Phone 2 through Telegram bot
"""

from flask import Flask, render_template_string, jsonify, request
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
phone2_connected = False

def find_control_py():
    """Find the control.py script in the current directory"""
    current_dir = Path.cwd()
    control_script = current_dir / "control.py"
    
    if control_script.exists():
        return str(control_script)
    return None

def start_bot():
    """Start the Telegram bot on Phone 2"""
    global bot_process, bot_running
    
    if bot_running:
        return True, "Bot already running"
    
    control_script = find_control_py()
    if not control_script:
        return False, "Control script not found"
    
    try:
        # Start the bot
        bot_process = subprocess.Popen(
            [sys.executable, control_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
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
    """Main control interface for Phone 2"""
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Phone 2 Control Interface</title>
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
            }
            
            .container {
                background: rgba(255, 255, 255, 0.1);
                padding: 40px;
                border-radius: 25px;
                backdrop-filter: blur(20px);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
                text-align: center;
                max-width: 600px;
                width: 100%;
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
                font-size: 2.5rem;
                margin-bottom: 20px;
                font-weight: 700;
            }
            
            .status {
                background: rgba(255, 255, 255, 0.2);
                padding: 20px;
                border-radius: 15px;
                margin: 20px 0;
                font-size: 16px;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            
            .connect-btn {
                background: #4CAF50;
                color: white;
                padding: 20px 40px;
                border: none;
                border-radius: 25px;
                font-size: 18px;
                font-weight: 600;
                margin: 20px 0;
                cursor: pointer;
                transition: all 0.3s;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            }
            
            .connect-btn:hover {
                background: #45a049;
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0,0,0,0.3);
            }
            
            .connect-btn:disabled {
                background: #cccccc;
                cursor: not-allowed;
                transform: none;
            }
            
            .instructions {
                background: rgba(255, 255, 255, 0.1);
                padding: 20px;
                border-radius: 15px;
                margin: 20px 0;
                text-align: left;
            }
            
            .instructions h3 {
                margin-bottom: 15px;
                text-align: center;
            }
            
            .instructions ol {
                padding-left: 20px;
            }
            
            .instructions li {
                margin: 10px 0;
                line-height: 1.6;
            }
            
            .connected-status {
                display: none;
                background: rgba(76, 175, 80, 0.2);
                border: 1px solid rgba(76, 175, 80, 0.4);
                padding: 20px;
                border-radius: 15px;
                margin: 20px 0;
            }
            
            .loading {
                display: none;
                margin: 20px 0;
            }
            
            .spinner {
                border: 4px solid rgba(255, 255, 255, 0.3);
                border-top: 4px solid white;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="icon">📱</div>
            <h1>Phone 2 Control Interface</h1>
            
            <div class="status" id="status">
                Ready to connect...
            </div>
            
            <button class="connect-btn" id="connectBtn" onclick="connectPhone()">
                🔌 Connect Phone 2
            </button>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>Connecting...</p>
            </div>
            
            <div class="connected-status" id="connectedStatus">
                ✅ Phone 2 is now connected and ready to be controlled!
                <br><br>
                <strong>Phone 1 can now control this device through Telegram!</strong>
            </div>
            
            <div class="instructions">
                <h3>📋 How This Works:</h3>
                <ol>
                    <li><strong>Click "Connect Phone 2"</strong> button above</li>
                    <li><strong>Phone 2</strong> will start the Telegram bot</li>
                    <li><strong>Phone 1</strong> can then control Phone 2 through Telegram</li>
                    <li><strong>Commands</strong> like /screen, /webcam, /sys will work on Phone 2</li>
                </ol>
            </div>
            
            <div style="margin-top: 30px; font-size: 14px; opacity: 0.8;">
                <p>💡 Keep this page open to maintain connection</p>
                <p>🔒 Phone 1 will have full control access</p>
            </div>
        </div>

        <script>
            let isConnected = false;
            
            async function connectPhone() {
                if (isConnected) return;
                
                const connectBtn = document.getElementById('connectBtn');
                const status = document.getElementById('status');
                const loading = document.getElementById('loading');
                const connectedStatus = document.getElementById('connectedStatus');
                
                connectBtn.disabled = true;
                loading.style.display = 'block';
                status.innerHTML = '🔌 Connecting Phone 2...';
                
                try {
                    // Start the bot
                    const response = await fetch('/start_bot', {
                        method: 'POST'
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        isConnected = true;
                        status.innerHTML = '✅ Phone 2 connected successfully!';
                        loading.style.display = 'none';
                        connectedStatus.style.display = 'block';
                        connectBtn.innerHTML = '✅ Connected';
                        connectBtn.style.background = '#4CAF50';
                        
                        // Show success message
                        setTimeout(() => {
                            status.innerHTML = '🎉 Phone 2 is now ready to be controlled by Phone 1!';
                        }, 2000);
                        
                    } else {
                        status.innerHTML = `❌ Connection failed: ${data.message}`;
                        loading.style.display = 'none';
                        connectBtn.disabled = false;
                    }
                    
                } catch (error) {
                    status.innerHTML = '❌ Connection failed. Please try again.';
                    loading.style.display = 'none';
                    connectBtn.disabled = false;
                }
            }
            
            // Check connection status on page load
            window.addEventListener('load', async () => {
                try {
                    const response = await fetch('/bot_status');
                    const data = await response.json();
                    
                    if (data.running) {
                        isConnected = true;
                        document.getElementById('status').innerHTML = '✅ Phone 2 is already connected!';
                        document.getElementById('connectBtn').innerHTML = '✅ Connected';
                        document.getElementById('connectBtn').style.background = '#4CAF50';
                        document.getElementById('connectedStatus').style.display = 'block';
                    }
                } catch (error) {
                    // Ignore errors on status check
                }
            });
            
            // Keep connection alive
            setInterval(async () => {
                if (isConnected) {
                    try {
                        await fetch('/health');
                    } catch (error) {
                        console.log('Keeping connection alive');
                    }
                }
            }, 30000); // Every 30 seconds
        </script>
    </body>
    </html>
    ''')

@app.route('/start_bot', methods=['POST'])
def start_bot_endpoint():
    """Start the bot to allow Phone 1 to control Phone 2"""
    success, message = start_bot()
    return jsonify({
        'success': success,
        'message': message,
        'running': bot_running
    })

@app.route('/bot_status')
def bot_status():
    """Check if bot is running"""
    return jsonify({
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
    print("📱 Phone 2 Control Interface")
    print("=" * 50)
    
    # Check if control.py exists
    control_script = find_control_py()
    if control_script:
        print(f"✅ Found control.py: {control_script}")
    else:
        print("❌ Could not find control.py script")
        print("   Make sure control.py is in the same directory")
        sys.exit(1)
    
    # Get port from environment variable (for Railway/Heroku) or use default
    port = int(os.environ.get('PORT', 5000))
    
    print("\n🌐 Control interface available at:")
    print(f"   Local: http://localhost:{port}")
    print(f"   Network: http://[your-ip]:{port}")
    print("\n📱 Phone 2 users access this page to connect")
    print("🎮 Phone 1 can then control Phone 2 through Telegram!")
    print("\n" + "=" * 50)
    
    try:
        app.run(host='0.0.0.0', port=port, debug=False)
    except KeyboardInterrupt:
        print("\n🛑 App stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
