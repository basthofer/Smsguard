from flask import Flask, request, redirect, url_for, send_from_directory, jsonify, flash, render_template_string
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.secret_key = "supersecretkey"

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/meow')
def index():
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template_string('''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Image Hosting Service</title>
      </head>
      <body>
        <h1>Upload Image</h1>
        <form method="POST" action="/upload" enctype="multipart/form-data">
          <input type="file" name="file">
          <input type="submit" value="Upload">
        </form>

        <h2>Uploaded Images</h2>
        <ul>
          {% for image in images %}
          <li><a href="{{ url_for('uploaded_file', filename=image) }}">{{ image }}</a></li>
          {% endfor %}
        </ul>

        {% with messages = get_flashed_messages() %}
          {% if messages %}
            <ul>
              {% for message in messages %}
                <li>{{ message }}</li>
              {% endfor %}
            </ul>
          {% endif %}
        {% endwith %}
      </body>
    </html>
    ''', images=images)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File successfully uploaded')
        return redirect(url_for('index'))
    else:
        flash('Invalid file type')
        return redirect(request.url)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# -------- API Endpoints --------

@app.route('/api/images', methods=['GET'])
def get_images():
    """API endpoint to retrieve a list of all uploaded images"""
    images = os.listdir(app.config['UPLOAD_FOLDER'])
    image_urls = [url_for('uploaded_file', filename=image, _external=True) for image in images]
    return jsonify({'images': image_urls}), 200

@app.route('/api/upload', methods=['POST'])
def api_upload_file():
    """API endpoint to upload an image via POST request"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Return the image URL in the response
        image_url = url_for('uploaded_file', filename=filename, _external=True)
        return jsonify({
            'message': 'File successfully uploaded',
            'filename': filename,
            'url': image_url
        }), 201
    else:
        return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/uploads/<filename>', methods=['GET'])
def api_get_uploaded_file(filename):
    """API endpoint to retrieve a specific image"""
    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True,port=3223)
