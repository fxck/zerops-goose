import os
import subprocess
from goose import Goose

# Initialize Goose with API key from environment variable
api_key = os.environ.get("LLM_API_KEY")
goose = Goose(api_key=api_key)

# Start a conversation with system prompt
system_prompt = """
You are running in a Zerops container. You can help with development tasks.
"""

# Create a simple HTTP server to handle health checks and commands
from http.server import BaseHTTPRequestHandler, HTTPServer

class GooseServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"OK")
            return
            
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Goose Agent is running")
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        # Process the request with Goose
        conversation = goose.start_conversation(system_prompt=system_prompt)
        response = conversation.send_message(post_data)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(f'{{"response": "{response}"}}'.encode())

# Run the server
server = HTTPServer(('', 8000), GooseServer)
print("Starting Goose server on port 8000")
server.serve_forever()
