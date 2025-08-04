# backend/pipelines/stream_processor.py
import cv2
import threading
import time
from datetime import datetime

# --- Shared data structures and lock for thread-safe access ---
# These are global to the application and are used to share data
# between the main FastAPI thread and the StreamProcessor threads.
active_streams = {}
stream_results = {}
alerts = []
data_lock = threading.Lock()

# --- Placeholder for AI model loading ---
def load_ai_model():
    """
    A placeholder function to simulate loading an AI model.
    In a real application, this would load a pre-trained PyTorch or TensorFlow model.
    """
    class MockModel:
        def predict(self, frame):
            # Simulate a prediction result
            import random
            if random.random() > 0.95:
                # Mock a detection of a person with high confidence
                return {"detected": "person", "confidence": 0.99}
            return {"detected": "none"}
    return MockModel()

# --- The StreamProcessor class with full implementation ---
class StreamProcessor(threading.Thread):
    """
    A thread that processes a single video stream.
    """
    def __init__(self, stream_id, source):
        super().__init__()
        self.stream_id = stream_id
        self.source = source
        self.running = True
        self.model = load_ai_model()
        
    def run(self):
        """
        The main loop of the thread. It reads frames, processes them,
        and saves results and alerts.
        """
        cap = cv2.VideoCapture(self.source)
        if not cap.isOpened():
            print(f"Error: Could not open video source {self.source}")
            with data_lock:
                if self.stream_id in active_streams:
                    del active_streams[self.stream_id]
            return

        print(f"Stream {self.stream_id} started processing.")
        
        while self.running:
            ret, frame = cap.read()
            if not ret:
                print(f"Stream {self.stream_id} ended.")
                break
                
            # 1. Pre-process the frame (e.g., resize for faster processing)
            frame_resized = cv2.resize(frame, (640, 480))
            
            # 2. Pass the frame to your AI model
            results = self.model.predict(frame_resized)
            
            # 3. Store the latest results in a thread-safe manner
            with data_lock:
                stream_results[self.stream_id] = {
                    "timestamp": datetime.now().isoformat(),
                    "status": "running",
                    "latest_prediction": results
                }
                
            # 4. Check for alerts and save them
            if self.is_alert(results):
                self.save_alert(self.stream_id, results)
                
            time.sleep(0.1) # Simulate a processing delay, adjust as needed
            
        cap.release()
        with data_lock:
            if self.stream_id in active_streams:
                active_streams[self.stream_id]['status'] = 'stopped'
                # Optionally, remove the stream from the active list
            print(f"Stream {self.stream_id} processing thread terminated.")

    def stop(self):
        """
        Stops the processing thread gracefully.
        """
        self.running = False

    def is_alert(self, results):
        """
        Determines if a prediction result constitutes an alert.
        """
        # Simple example: an alert is triggered if a "person" is detected
        return results.get("detected") == "person"
        
    def save_alert(self, stream_id, results):
        """
        Saves a new alert in a thread-safe manner.
        """
        with data_lock:
            alerts.append({
                "timestamp": datetime.now().isoformat(),
                "stream_id": stream_id,
                "alert_type": "person_detected",
                "prediction_data": results
            })
