import cv2
import os

def choose_best_face(video_path, face_id):
    cap = cv2.VideoCapture(video_path)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    max_confidence = -1
    best_face = None

    # Skip frames for faster processing
    frame_skip = 5
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_skip == 0:
            
            # Resize frame for faster processing
            resized_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            
            # Detect faces
            gray = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                # Calculate confidence as the area of the detected face
                confidence = w * h
                if confidence > max_confidence:
                    max_confidence = confidence
                    best_face = resized_frame[y:y+h, x:x+w].copy()  # Crop the face region

        frame_count += 1

    cap.release()

    if best_face is not None:
        # Construct the file name with the provided ID
        filename = f"{face_id}.jpg"
        filepath = os.path.join("faces_database", filename)
        cv2.imwrite(filepath, best_face)
        print("Best face cropped and saved successfully as:", filename)
    else:
        print("Error: No face detected in the video.")
