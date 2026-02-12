from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Generation(Base):
    __tablename__ = "generations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    model_id = Column(String)
    model_name = Column(String)
    generation_type = Column(String)  # text, code, image, audio
    prompt = Column(Text)
    result = Column(JSON)  # Store generation result
    generation_metadata = Column(JSON, nullable=True)  # Renamed from 'metadata'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User")