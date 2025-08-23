#!/usr/bin/env python3
"""
Simple HTTP server to serve the JuryBot frontend
Run this script to serve the frontend on http://localhost:8080
"""

import http.server
import socketserver
import os
import sys

def main():
    # Change to frontend directory
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    
    if not os.path.exists(frontend_dir):
        print("❌ Frontend directory not found!")
        print("Make sure you're running this script from the JuryBot project root directory.")
        sys.exit(1)
    
    os.chdir(frontend_dir)
    
    PORT = 8080
    
    # Check if port is available
    try:
        with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
            print(f"🌐 Serving JuryBot frontend at http://localhost:{PORT}")
            print("📁 Serving files from:", os.path.abspath(frontend_dir))
            print("🔄 Press Ctrl+C to stop the server")
            print("=" * 50)
            httpd.serve_forever()
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {PORT} is already in use!")
            print("Try using a different port or stop the service using port 8080")
        else:
            print(f"❌ Error starting server: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
