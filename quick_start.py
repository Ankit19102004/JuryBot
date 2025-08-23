#!/usr/bin/env python3
"""
Quick Start Script for JuryBot
This script helps you get the JuryBot application running quickly.
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_path = Path("backend/.env")
    if not env_path.exists():
        print("❌ backend/.env file not found!")
        print("\n📝 Please create backend/.env with the following content:")
        print("=" * 50)
        print("GOOGLE_API_KEY=your_google_api_key_here")
        print("SECRET_KEY=your_secret_key_here")
        print("DEBUG=True")
        print("MAX_CONTENT_LENGTH=16777216")
        print("UPLOAD_FOLDER=temp")
        print("ALLOWED_EXTENSIONS=['pdf', 'txt', 'docx']")
        print("MODEL_NAME=gemini-pro")
        print("MAX_TOKENS=2048")
        print("TEMPERATURE=0.7")
        print("=" * 50)
        print("\n🔑 Get your Google API key from: https://makersuite.google.com/app/apikey")
        return False
    
    # Check if API key is set
    with open(env_path, 'r') as f:
        content = f.read()
        if 'your_google_api_key_here' in content:
            print("❌ Please replace 'your_google_api_key_here' with your actual Google API key in backend/.env")
            return False
    
    print("✅ Environment configuration found")
    return True


def get_venv_paths():
    """Return paths related to the local virtual environment (.venv)."""
    venv_dir = Path('.venv')
    if os.name == 'nt':
        python_path = venv_dir / 'Scripts' / 'python.exe'
        pip_path = venv_dir / 'Scripts' / 'pip.exe'
        activate_hint = str(venv_dir / 'Scripts' / 'activate')
    else:
        python_path = venv_dir / 'bin' / 'python'
        pip_path = venv_dir / 'bin' / 'pip'
        activate_hint = str(venv_dir / 'bin' / 'activate')
    return venv_dir, python_path, pip_path, activate_hint


def ensure_venv():
    """Create a local virtual environment if it doesn't exist."""
    venv_dir, python_path, _, activate_hint = get_venv_paths()
    if python_path.exists():
        print(f"✅ Using existing virtual environment at {venv_dir}")
        return True

    print("🐍 Creating virtual environment (.venv)...")
    try:
        subprocess.run([sys.executable, '-m', 'venv', str(venv_dir)], check=True)
        print("✅ Virtual environment created")
        print(f"👉 To activate later: {activate_hint}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def install_requirements():
    """Install Python requirements into the local virtual environment."""
    requirements_path = Path("backend/requirements.txt")
    if not requirements_path.exists():
        print("❌ backend/requirements.txt not found!")
        return False

    _, _, pip_path, _ = get_venv_paths()
    print("📦 Installing Python requirements into .venv...")
    try:
        subprocess.run([str(pip_path), "install", "--upgrade", "pip"], check=True)
        subprocess.run([str(pip_path), "install", "-r", str(requirements_path)], check=True)
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        print("Try running inside venv: pip install -r backend/requirements.txt")
        return False

def start_backend():
    """Start the backend server using the virtual environment Python."""
    print("🚀 Starting backend server...")
    try:
        backend_dir = Path("backend")
        if not backend_dir.exists():
            print("❌ Backend directory not found!")
            return False

        _, venv_python, _, _ = get_venv_paths()
        if not venv_python.exists():
            print("❌ Virtual environment Python not found. Did venv creation fail?")
            return False

        env = os.environ.copy()
        env.setdefault('PYTHONUTF8', '1')

        process = subprocess.Popen([str(venv_python), "app.py"],
                                   cwd=backend_dir,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE,
                                   env=env)

        time.sleep(3)

        if process.poll() is None:
            print("✅ Backend server started successfully")
            print("   API available at: http://localhost:5000")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Backend failed to start:")
            print(f"   Error: {stderr.decode()}")
            return False

    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return False

def start_frontend():
    """Start the frontend server"""
    print("🌐 Starting frontend server...")
    try:
        # Start frontend server
        process = subprocess.Popen([sys.executable, "serve_frontend.py"],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        
        # Wait a moment for the server to start
        time.sleep(2)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Frontend server started successfully")
            print("   Frontend available at: http://localhost:8080")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Frontend failed to start:")
            print(f"   Error: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
        return False

def main():
    print("🚀 JuryBot Quick Start")
    print("=" * 50)
    
    # Check prerequisites
    if not check_python_version():
        return
    
    if not check_env_file():
        return

    if not ensure_venv():
        return

    if not install_requirements():
        return
    
    print("\n🎯 Starting JuryBot application...")
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Failed to start backend. Exiting.")
        return
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ Failed to start frontend. Stopping backend.")
        backend_process.terminate()
        return
    
    print("\n🎉 JuryBot is now running!")
    print("=" * 50)
    print("📱 Frontend: http://localhost:8080")
    print("🔧 Backend API: http://localhost:5000")
    print("\n💡 Tips:")
    print("   - Upload a legal document or paste text to get started")
    print("   - Ask questions about your document")
    print("   - Select clauses to get explanations")
    print("\n🛑 Press Ctrl+C to stop both servers")
    
    # Open browser
    try:
        webbrowser.open("http://localhost:8080")
        print("🌐 Opening browser...")
    except:
        print("💡 Open your browser and go to: http://localhost:8080")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
            # Check if processes are still running
            if backend_process.poll() is not None:
                print("❌ Backend server stopped unexpectedly")
                break
            if frontend_process.poll() is not None:
                print("❌ Frontend server stopped unexpectedly")
                break
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
    finally:
        # Clean up processes
        if backend_process and backend_process.poll() is None:
            backend_process.terminate()
            print("✅ Backend server stopped")
        if frontend_process and frontend_process.poll() is None:
            frontend_process.terminate()
            print("✅ Frontend server stopped")

if __name__ == "__main__":
    main()

