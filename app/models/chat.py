from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, default="New Chat")
    model_id = Column(String, nullable=False)  # OpenRouter model ID
    model_name = Column(String, nullable=False)  # Display name
    model_type = Column(String, nullable=False)  # text, image, audio
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User")
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    role = Column(String)  # user, assistant
    content = Column(Text)
    
    # For code blocks - store as JSON array of code blocks
    code_blocks = Column(JSON, nullable=True)
    
    # For images generation
    images = Column(JSON, nullable=True)  # List of image URLs/base64
    
    # For audio generation
    audio_url = Column(String, nullable=True)
    
    # Reasoning details (for models that support it)
    reasoning_details = Column(JSON, nullable=True)
    
    # Created at timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    tokens = Column(Integer, default=0)
    
    # Relationships
    chat = relationship("Chat", back_populates="messages")