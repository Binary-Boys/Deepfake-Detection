import tensorflow as tf
import numpy as np
import cv2

class DeepfakeDetector:
    def __init__(self):
        self.model = self._load_model()
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    def _load_model(self):
        # Load your pre-trained model here
        # This is a simplified example - you should replace this with your actual model
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(128, 128, 3)),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])
        return model
    
    def preprocess_frame(self, frame):
        # Convert to RGB and resize
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (128, 128))
        frame = frame.astype('float32') / 255.0
        return frame
    
    def detect_faces(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        return faces
    
    def analyze_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        frames_scores = []
    
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
        
            # Detect faces
            faces = self.detect_faces(frame)
        
            for (x, y, w, h) in faces:
                # Extract and preprocess face region
                face_frame = frame[y:y+h, x:x+w]
                if face_frame.size == 0:
                    continue
                
                processed_frame = self.preprocess_frame(face_frame)
                prediction = self.model.predict(np.expand_dims(processed_frame, axis=0))[0][0]
                frames_scores.append(float(prediction))  # Convert to Python float
    
        cap.release()
    
        if not frames_scores:
            return {
                'is_deepfake': False,  # Convert to Python bool
                'confidence': 0.0,     # Convert to Python float
                'message': 'No faces detected in video'
            }
    
        # Calculate final score
        final_score = float(np.mean(frames_scores))  # Convert to Python float
        is_deepfake = bool(final_score > 0.5)        # Convert to Python bool
    
        return {
            'is_deepfake': is_deepfake,
            'confidence': final_score * 100,
            'message': 'Deepfake detected' if is_deepfake else 'No deepfake detected'
        }

