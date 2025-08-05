from pydantic import BaseModel

class VideoRequest(BaseModel):
    youtube_url: str
    query: str

class QAResponse(BaseModel):
    query: str
    result: str