import cv2
import torch
from yolov8 import Detector

def main():
    # Initialize the detector with the yolov8 model
    detector = Detector(model_name='yolov8n')

    # Start capturing video from the default webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Detect objects in the frame
        detections = detector.predict(frame, plot=False)

        # Count objects
        object_counts = {}
        for det in detections:
            label = det['class_name']
            object_counts[label] = object_counts.get(label, 0) + 1

        # Print object counts
        print("Counts per frame:", object_counts)

        # Draw detections on the frame
        annotated_frame = detector.plot_boxes(detections, frame)

        # Display the resulting frame
        cv2.imshow('Frame', annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

