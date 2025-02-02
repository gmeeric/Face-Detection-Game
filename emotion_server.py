import socket
import cv2
from fer import FER
import time

# Initialize emotion detector
detector = FER()

# Start TCP server
HOST = "127.0.0.1"  # Localhost
PORT = 6000  # Port number

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)
print(f"Server started on {HOST}:{PORT}")

# Open webcam
cap = cv2.VideoCapture(0)
conn, addr = server.accept()
print(f"Connection from {addr}")

emotion_string = f"emotion: {'happy'}, score: {0.4}"
conn.sendall(emotion_string.encode('utf-8'))

last_time = time.time()  # Keep track of the last time an image was captured

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    # Get the current time
    current_time = time.time()

    # Check if 5 seconds have passed since the last capture
    if current_time - last_time >= 5:
        # Convert frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect emotions
        emotion_data = detector.detect_emotions(rgb_frame)

        if emotion_data:
            for face_data in emotion_data:
                emotions = face_data['emotions']

                # Determine the dominant emotion based on thresholds
                dominant_emotion = None
                emotion_score = 0

                if emotions['happy'] > 0.8:
                    dominant_emotion = 'happy'
                    emotion_score = emotions['happy']
                elif emotions['sad'] > 0.2:
                    dominant_emotion = 'sad'
                    emotion_score = emotions['sad']
                elif emotions['angry'] > 0.5:
                    dominant_emotion = 'angry'
                    emotion_score = emotions['angry']
                elif emotions['surprise'] > 0.5:
                    dominant_emotion = 'surprise'
                    emotion_score = emotions['surprise']
                elif emotions['fear'] > 0.5:
                    dominant_emotion = 'fear'
                    emotion_score = emotions['fear']
                elif emotions['disgust'] > 0.5:
                    dominant_emotion = 'disgust'
                    emotion_score = emotions['disgust']
                elif emotions['neutral'] > 0.5:
                    dominant_emotion = 'neutral'
                    emotion_score = emotions['neutral']

                if dominant_emotion:
                    # Send the dominant emotion as a string to Unity
                    emotion_string = f"emotion: {dominant_emotion}, score: {emotion_score}"
                    conn.sendall(emotion_string.encode('utf-8'))

        # Update the last_time to the current time
        last_time = current_time

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
server.close()
