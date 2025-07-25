from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import uuid
import subprocess

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.post("/download")
async def download_video(request: Request):
    data = await request.json()
    video_url = data.get("url")

    try:
        filename = f"{uuid.uuid4()}.mp4"
        filepath = os.path.join(DOWNLOAD_FOLDER, filename)

        cmd = [
            "yt-dlp",
            "-f", "mp4",
            "-o", filepath,
            video_url
        ]

        subprocess.run(cmd, check=True)
        return {
            "status": "success",
            "file_url": f"https://video-downloader-zycn.onrender.com/video/{filename}"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/video/{filename}")
async def serve_video(filename: str):
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)
    if os.path.exists(filepath):
        return FileResponse(filepath, media_type="video/mp4", filename=filename)
    return {"status": "error", "message": "File not found"}
