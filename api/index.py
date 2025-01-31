import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs

# Get the absolute path of the JSON file
json_file_path = os.path.join(os.path.dirname(__file__), "q-vercel-python.json")

try:
    with open(json_file_path, "r") as file:
        marks_data = json.load(file)
except FileNotFoundError:
    marks_data = {}  # Empty dictionary if file is missing

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query parameters
        query = parse_qs(self.path.split('?')[-1])
        names = query.get("name", [])  # Get all "name" parameters

        # Fetch marks for requested names
        response = {"marks": {name: marks_data.get(name, 0) for name in names}}

        # Send JSON response
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode("utf-8"))
