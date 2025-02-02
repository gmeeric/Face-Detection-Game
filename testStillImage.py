from fer import FER
import cv2
import face_recognition

detector = FER()

image = cv2.imread("path_to_image.jpg")

# Detect emotions
emotion_data = detector.detect_emotions(image)
print(emotion_data)