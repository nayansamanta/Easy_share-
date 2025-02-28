from flask import Flask, request, jsonify, render_template, redirect, url_for, Response, abort, send_file
import os
import uuid
import mimetypes

app = Flask(__name__)
FILE_DIRECTORY = 'shared_files'  # Directory to store shared files
file_store = {}  # Dictionary to store tokens and file paths

# Ensure the directory exists
os.makedirs(FILE_DIRECTORY, exist_ok=True)


def generate_file_stream(file_path, chunk_size=4096):
    """Generator to read a file in chunks and yield each chunk."""
    try:
        with open(file_path, 'rb') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                yield chunk
    except IOError:
        abort(500, description="Error reading the file.")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/share', methods=['POST'])
def share_file():
    file = request.files.get('file')
    print(file)
    if not file:
        return jsonify({'error': 'No file provided'}), 400
    # Get the filename and extract the extension
    filename = file.filename
    _, file_extension = os.path.splitext(filename)

    # Save file with a unique name
    file_id = str(uuid.uuid4())
    new_filename = f"{file_id}.{file_extension}"
    file_path = os.path.join(FILE_DIRECTORY, new_filename)
    file.save(file_path)
    token = str(uuid.uuid4())
    file_store[token] = file_path

    # Return URL for accessing the file
    access_url = url_for('view_file', token=token, _external=True)
    return jsonify({'access_url': access_url})


@app.route('/view/<token>', methods=['GET'])
def view_file(token):
    file_path = file_store.get(token)
    if not file_path or not os.path.isfile(file_path):
        return abort(404, description="File not found or token expired.")

    mime_type, _ = mimetypes.guess_type(file_path)
    mime_type = mime_type or 'application/octet-stream'
    headers = {'Content-Disposition': 'inline'} if mime_type.startswith(
        ('image/', 'video/', 'audio/', 'application/pdf')) else {'Content-Disposition': 'attachment'}

    return Response(generate_file_stream(file_path), content_type=mime_type, headers=headers)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
