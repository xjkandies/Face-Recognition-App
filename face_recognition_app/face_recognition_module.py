import os
import numpy
import face_recognition
from PIL import Image
from typing import List, Tuple, Optional
from config import AUTHORIZED_FACES_DIR, ALLOWED_EXTENSIONS, FACE_MATCH_TOLERANCE

def is_allowed_file(filename: str) -> bool:
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_image_file(file_path: str) -> Optional[numpy.ndarray]:
    """
    Load an image file safely and return it as a numpy array.
    
    Args:
        file_path: Path to the image file
    Returns:
        numpy array of the image or None if loading fails
    """
    try:
        return face_recognition.load_image_file(file_path)
    except Exception as e:
        print(f"Error loading image: {str(e)}")
        return None

def get_face_encodings(image: numpy.ndarray) -> Tuple[List, int]:
    """
    Get face encodings from an image.
    
    Args:
        image: numpy array of the image
    Returns:
        Tuple containing list of face encodings and number of faces detected
    """
    try:
        face_encodings = face_recognition.face_encodings(image)
        return face_encodings, len(face_encodings)
    except Exception as e:
        print(f"Error getting face encodings: {str(e)}")
        return [], 0

def load_authorized_faces() -> List:
    """
    Load and encode all authorized faces from the authorized_faces directory.
    
    Returns:
        List of face encodings for all authorized faces
    """
    authorized_encodings = []
    
    # Ensure the authorized faces directory exists
    if not os.path.exists(AUTHORIZED_FACES_DIR):
        print(f"Warning: Authorized faces directory not found at {AUTHORIZED_FACES_DIR}")
        return authorized_encodings

    # Process each image in the authorized faces directory
    for filename in os.listdir(AUTHORIZED_FACES_DIR):
        if is_allowed_file(filename):
            image_path = os.path.join(AUTHORIZED_FACES_DIR, filename)
            try:
                # Load the image
                image = load_image_file(image_path)
                if image is None:
                    continue

                # Get face encodings
                face_encodings, num_faces = get_face_encodings(image)
                
                # Verify exactly one face is present in the authorized image
                if num_faces == 0:
                    print(f"Warning: No face found in authorized image {filename}")
                elif num_faces > 1:
                    print(f"Warning: Multiple faces found in authorized image {filename}")
                else:
                    authorized_encodings.append(face_encodings[0])
                    
            except Exception as e:
                print(f"Error processing authorized face {filename}: {str(e)}")
                continue

    return authorized_encodings

def verify_face(image_path: str, authorized_encodings: List) -> Tuple[bool, str]:
    """
    Verify if the face in the uploaded image matches any authorized face.
    
    Args:
        image_path: Path to the image to verify
        authorized_encodings: List of encodings of authorized faces
    Returns:
        Tuple of (is_authorized: bool, message: str)
    """
    if not is_allowed_file(image_path):
        return False, "Unsupported file format"

    # Load the image
    image = load_image_file(image_path)
    if image is None:
        return False, "Failed to load image"

    # Get face encodings
    face_encodings, num_faces = get_face_encodings(image)

    # Check number of faces detected
    if num_faces == 0:
        return False, "No face detected in the image"
    elif num_faces > 1:
        return False, "Multiple faces detected. Please upload an image with a single face"

    # Compare with authorized faces
    if not authorized_encodings:
        return False, "No authorized faces available for comparison"

    # Check if the face matches any authorized face
    matches = face_recognition.compare_faces(authorized_encodings, 
                                          face_encodings[0], 
                                          tolerance=FACE_MATCH_TOLERANCE)
    
    if True in matches:
        return True, "Access Granted"
    else:
        return False, "Access Denied"