from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

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

# Add other endpoints here...

# /streams/start (POST): Accepts a video file or stream URL.

# /streams/stop (POST): Accepts a stream ID to terminate.

# /streams/status (GET): Returns the status of all active streams.

# /outputs/alerts (GET): Returns a list of the latest alerts.



active_streams = {}

@app.post("/streams/start")
async def start_stream(stream_id: str, source: str):
    if stream_id in active_streams:
        return {"message": "Stream already running."}

    processor = StreamProcessor(stream_id, source)
    processor.start() # Start the thread
    active_streams[stream_id] = processor
    return {"message": f"Stream {stream_id} started."}

# ... create other endpoints to manage active_streams
