import face_recognition
import cv2
import os
import glob
import numpy as np

class FaceRecognition:
    def __init__(self, frame_resizing=0.25):
        self.known_face_encodings = []
        self.known_face_id = []
        self.frame_resizing = frame_resizing

    def load_encoding_images(self, images_path):
        """
        Load encoding images from the specified path.
        
        Parameters:
            images_path (str): Path to the directory containing encoding images.
        """
        images_path = glob.glob(os.path.join(images_path, "*.*"))
        print(f"{len(images_path)} encoding images found.")

        for img_path in images_path:
            filename = os.path.splitext(os.path.basename(img_path))[0]
            img_encoding = self._encode_image(img_path)
            
            if img_encoding is not None:
                self.known_face_encodings.append(img_encoding)
                self.known_face_id.append(filename)
        
        print("Encoding images loaded")

    def _encode_image(self, img_path):
        img = cv2.imread(img_path)
        if img is None:
            print(f"Unable to read image: {img_path}")
            return None
        
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(rgb_img)
        
        if not face_encodings:
            print(f"No faces found in image: {img_path}")
            return None
        
        return face_encodings[0]

    def detect_known_faces(self, frame):
        """
        Detect known faces in the provided frame.
        
        Parameters:
            frame (numpy.ndarray): Input frame to detect faces.
            
        Returns:
            Tuple: A tuple containing detected face locations and corresponding names.
        """
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_id = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                best_match_index = matches.index(True)
                name = self.known_face_id[best_match_index]

            face_id.append(name)

        face_locations = np.array(face_locations) / self.frame_resizing
        return face_locations.astype(int), face_id
