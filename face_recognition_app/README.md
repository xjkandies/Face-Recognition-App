# Face Recognition Access Control System

A desktop application that uses facial recognition to control access by comparing uploaded face images against a database of authorized faces.

## Features

- Modern and user-friendly desktop interface
- Real-time face verification
- Support for multiple authorized faces
- Clear visual feedback for access decisions
- Easy-to-use image upload system

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Operating system: Windows, macOS, or Linux
- Webcam (optional, for live capture feature)

## Installation

1. Clone or download this repository to your local machine.

2. Create a virtual environment (recommended):
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - On Windows:
   ```bash
   venv\Scripts\activate
   ```
   - On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. Install the required packages:
```bash
pip install -r requirements.txt
```

Note: On some systems, you might need to install additional system-level dependencies for the face_recognition package. Please refer to the [face_recognition installation guide](https://github.com/ageitgey/face_recognition#installation) if you encounter any issues.

## Setting Up Authorized Faces

1. Create a folder named `authorized_faces` in the application directory (if it doesn't exist already).

2. Add photos of authorized individuals to this folder:
   - Use clear, well-lit photos
   - Each photo should contain only one face
   - Supported formats: JPG, JPEG, PNG
   - Name the files descriptively (e.g., "john_doe.jpg")

## Usage

1. Run the application:
```bash
python main.py
```

2. Using the application:
   - Click "Upload Image" to select a photo for verification
   - The selected image will appear in the preview window
   - Click "Verify Face" to check if the face matches any authorized faces
   - The result will be displayed below the buttons
   - Use "Clear" to reset and try another image

## Troubleshooting

Common issues and solutions:

1. **No face detected**
   - Ensure the image is clear and well-lit
   - Make sure the face is clearly visible and not obscured
   - Try a different photo angle

2. **Multiple faces detected**
   - Use a photo containing only one face
   - Crop the image to include only the face to be verified

3. **Access denied for authorized person**
   - Check if the person's photo is in the authorized_faces folder
   - Try using a clearer or more recent photo
   - Ensure proper lighting in both the authorized and verification photos

## Security Notes

- Keep the authorized_faces folder secure and regularly backed up
- Regularly update the authorized faces database
- Monitor and audit access attempts if needed
- Consider implementing additional security measures for sensitive applications

## Technical Details

The application uses:
- face_recognition library for face detection and recognition
- Tkinter for the graphical user interface
- PIL (Python Imaging Library) for image handling
- Custom face encoding storage system

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.