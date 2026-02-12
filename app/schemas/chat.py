from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class MessageBase(BaseModel):
    role: str
    content: str
    code_blocks: Optional[List[Dict[str, Any]]] = None
    images: Optional[List[str]] = None
    audio_url: Optional[str] = None
    reasoning_details: Optional[Dict[str, Any]] = None

class MessageCreate(MessageBase):
    chat_id: int
    tokens: int = 0

class Message(MessageBase):
    id: int
    chat_id: int
    created_at: datetime
    tokens: int
    
    class Config:
        from_attributes = True

class ChatBase(BaseModel):
    title: str
    model_id: str
    model_name: str
    model_type: str

class ChatCreate(ChatBase):
    pass

class ChatUpdate(BaseModel):
    title: Optional[str] = None

class Chat(ChatBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    messages: List[Message] = []
    
    class Config:
        from_attributes = True

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[Dict[str, Any]]
    reasoning: Optional[Dict[str, bool]] = None
    modalities: Optional[List[str]] = None
    stream: Optional[bool] = False

class ChatCompletionResponse(BaseModel):
    id: str
    choices: List[Dict[str, Any]]
    usage: Optional[Dict[str, int]] = None