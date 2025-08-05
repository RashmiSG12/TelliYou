import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Backend.main import main  
def process_video_query(youtube_url: str, query: str) -> str:
    result = main(youtube_url, query)
    if not result:
        result = "Sorry, no answer could be generated."
    return result

