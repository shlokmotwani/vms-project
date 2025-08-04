# backend/main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from .pipelines.stream_processor import active_streams, stream_results, alerts, data_lock, StreamProcessor

app = FastAPI()

# Allow CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "VMS Backend is running!"}

@app.post("/streams/start")
async def start_stream(stream_id: str, source: str):
    """
    Starts a new video stream processing pipeline.
    """
    with data_lock:
        if stream_id in active_streams:
            return {"message": "Stream already running."}
        
        processor = StreamProcessor(stream_id, source)
        processor.start() # Start the thread
        active_streams[stream_id] = processor
    return {"message": f"Stream {stream_id} started."}

@app.post("/streams/stop")
async def stop_stream(stream_id: str):
    """
    Stops a running video stream processing pipeline.
    """
    with data_lock:
        if stream_id not in active_streams:
            return {"message": "Stream not found or already stopped."}
        
        processor = active_streams.pop(stream_id)
        processor.stop()
    return {"message": f"Stream {stream_id} stopped."}
    
@app.get("/streams/status")
async def get_stream_status():
    """
    Returns the status and latest results for all active streams.
    """
    with data_lock:
        status = {
            stream_id: stream_results.get(stream_id, {"status": "starting"})
            for stream_id in active_streams
        }
        return {"streams": status}
        
@app.get("/outputs/alerts")
async def get_alerts():
    """
    Returns a list of all recorded alerts.
    """
    with data_lock:
        return {"alerts": alerts}
