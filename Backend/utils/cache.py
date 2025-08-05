import os
import shutil

LAST_VIDEO_ID_PATH = "E:/TelliYou/Backend/last_video_id.txt"
SUBTITLES_DIR = "E:/TelliYou/fastapi_app/subtitles"
CHROMA_DB_DIR = "E:/TelliYou/fastapi_app/chroma_db"


def is_new_video(video_id: str) -> bool:
    if not os.path.exists(LAST_VIDEO_ID_PATH):
        with open(LAST_VIDEO_ID_PATH, "w") as f:
            f.write(video_id)
        return True

    with open(LAST_VIDEO_ID_PATH, "r") as f:
        last_video_id = f.read().strip()

    if video_id != last_video_id:
        with open(LAST_VIDEO_ID_PATH, "w") as f:
            f.write(video_id)

        # Delete old subtitle file
        subtitle_path = os.path.join(SUBTITLES_DIR, f"{last_video_id}.en.vtt")
        if os.path.exists(subtitle_path):
            os.remove(subtitle_path)
            print(f"🧹 Deleted subtitle: {subtitle_path}")

        # Delete old ChromaDB folder
        chroma_path = os.path.join(CHROMA_DB_DIR, last_video_id)
        if os.path.exists(chroma_path):
            shutil.rmtree(chroma_path, ignore_errors=True)
            print(f"🧹 Deleted ChromaDB folder: {chroma_path}")

        return True

    return False
