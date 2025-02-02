from fer import FER
import cv2

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Create an emotion detector
detector = FER()

while True:
    # Read a frame from the camera
    ret, frame = cap.read()

    # Convert the image from BGR to RGB
    rgb_frame = frame[:, :, ::-1]

    # Get the emotions and faces directly using FER
    emotion_data = detector.detect_emotions(rgb_frame)

    # Print the emotion data for debugging
    print(emotion_data)

    if emotion_data:
        # Process each face and its emotion data
        for face_data in emotion_data:
            x, y, w, h = face_data['box']  # Correct box format
            emotions = face_data['emotions']

            # Compute proper bounding box
            right = x + w
            bottom = y + h

            # Draw rectangle around the face
            cv2.rectangle(frame, (x, y), (right, bottom), (0, 255, 0), 2)

            # Display each emotion and its score
            y_offset = y - 10  # Start drawing text above the face
            for emotion, score in emotions.items():
                cv2.putText(frame, f"{emotion}: {score:.2f}", (x, y_offset),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                y_offset -= 30  # Space out the emotion labels

    # Show the frame with face locations and emotions
    cv2.imshow("Camera Feed", frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()