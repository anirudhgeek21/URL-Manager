from flask import Flask, request, jsonify, send_from_directory
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    print("Root route accessed!")  # Debug statement
    return send_from_directory('templates', 'index.html')

@app.route('/choose-directory', methods=['GET'])
def choose_directory():
    directory_path = os.getcwd()  # Replace with desired directory path
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
    return jsonify({'files': files})

@app.route('/save-url', methods=['POST'])
def save_url():
    data = request.get_json()
    url = data.get('url')
    file_name = data.get('file')
    if not url or not file_name:
        return jsonify({'message': 'Invalid data'}), 400

    # Get the directory path from the chosen file name
    # Assuming the chosen file name includes the path relative to the current directory
    file_path = os.path.dirname(file_name) 

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(os.path.join(file_path, file_name), 'a') as f:
        f.write(f'{timestamp} - {url}\n')

    return jsonify({'message': 'URL saved successfully'})

@app.route('/<path:path>', methods=['GET'])
def serve_file(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    app.run(debug=True)
