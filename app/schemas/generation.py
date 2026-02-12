from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class GenerationBase(BaseModel):
    model_id: str
    model_name: str
    generation_type: str
    prompt: str

class GenerationCreate(GenerationBase):
    user_id: int
    result: Dict[str, Any]
    generation_metadata: Optional[Dict[str, Any]] = None  # Renamed

class Generation(GenerationBase):
    id: int
    user_id: int
    result: Dict[str, Any]
    generation_metadata: Optional[Dict[str, Any]] = None  # Renamed
    created_at: datetime
    
    class Config:
        from_attributes = True

class ImageGenerationRequest(BaseModel):
    prompt: str
    model: str
    negative_prompt: Optional[str] = None
    num_images: Optional[int] = 1
    size: Optional[str] = "1024x1024"

class AudioGenerationRequest(BaseModel):
    prompt: str
    model: str
    audio_input: Optional[str] = None
    format: Optional[str] = "wav"