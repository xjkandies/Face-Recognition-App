from flask import Flask, render_template, request, jsonify, send_file
import face_recognition_module as frm
import os
from gtts import gTTS
import base64
import tempfile
from werkzeug.utils import secure_filename
import shutil

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load authorized faces on startup
authorized_encodings = frm.load_authorized_faces()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test_authorized')
def test_authorized():
    """Test route for authorized face"""
    try:
        # Copy the authorized face to uploads
        src = os.path.join('authorized_faces', 'sample_authorized.jpg')
        dst = os.path.join(app.config['UPLOAD_FOLDER'], 'test_auth.jpg')
        shutil.copy2(src, dst)
        
        # Verify the face
        is_authorized, message = frm.verify_face(dst, authorized_encodings)
        
        # Generate speech
        speech_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
        tts = gTTS(text="Access Granted" if is_authorized else "Access Denied", 
                  lang='en', slow=False)
        tts.save(speech_file.name)
        
        # Read the audio file and convert to base64
        with open(speech_file.name, 'rb') as audio_file:
            audio_data = base64.b64encode(audio_file.read()).decode('utf-8')
        
        # Clean up
        os.unlink(speech_file.name)
        os.unlink(dst)
        
        return jsonify({
            'success': True,
            'is_authorized': is_authorized,
            'message': message,
            'audio': audio_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test_unauthorized')
def test_unauthorized():
    """Test route for unauthorized face"""
    try:
        # Copy the unauthorized face to uploads
        src = 'test_image.jpg'  # This is Obama's photo
        dst = os.path.join(app.config['UPLOAD_FOLDER'], 'test_unauth.jpg')
        shutil.copy2(src, dst)
        
        # Verify the face
        is_authorized, message = frm.verify_face(dst, authorized_encodings)
        
        # Generate speech
        speech_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
        tts = gTTS(text="Access Granted" if is_authorized else "Access Denied", 
                  lang='en', slow=False)
        tts.save(speech_file.name)
        
        # Read the audio file and convert to base64
        with open(speech_file.name, 'rb') as audio_file:
            audio_data = base64.b64encode(audio_file.read()).decode('utf-8')
        
        # Clean up
        os.unlink(speech_file.name)
        os.unlink(dst)
        
        return jsonify({
            'success': True,
            'is_authorized': is_authorized,
            'message': message,
            'audio': audio_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/verify', methods=['POST'])
def verify():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file:
        # Save the uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Verify the face
            is_authorized, message = frm.verify_face(filepath, authorized_encodings)
            
            # Generate speech
            speech_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False)
            tts = gTTS(text="Access Granted" if is_authorized else "Access Denied", 
                      lang='en', slow=False)
            tts.save(speech_file.name)
            
            # Read the audio file and convert to base64
            with open(speech_file.name, 'rb') as audio_file:
                audio_data = base64.b64encode(audio_file.read()).decode('utf-8')
            
            # Clean up
            os.unlink(speech_file.name)
            os.unlink(filepath)
            
            return jsonify({
                'success': True,
                'is_authorized': is_authorized,
                'message': message,
                'audio': audio_data
            })
            
        except Exception as e:
            if os.path.exists(filepath):
                os.unlink(filepath)
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)