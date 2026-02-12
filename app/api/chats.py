from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.chat import Chat, Message
from app.schemas.chat import ChatCreate, ChatUpdate, Chat as ChatSchema, MessageCreate, Message as MessageSchema
from app.dependencies.auth import get_current_user
from app.services.openrouter import openrouter_service
from app.utils.code_formatter import format_code_response
from datetime import datetime

router = APIRouter(prefix="/chats", tags=["chats"])

@router.post("/", response_model=ChatSchema)
async def create_chat(
    chat: ChatCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_chat = Chat(
        user_id=current_user.id,
        title=chat.title,
        model_id=chat.model_id,
        model_name=chat.model_name,
        model_type=chat.model_type
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

@router.get("/", response_model=List[ChatSchema])
async def get_user_chats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chats = db.query(Chat).filter(Chat.user_id == current_user.id).order_by(Chat.updated_at.desc()).all()
    return chats

@router.get("/{chat_id}", response_model=ChatSchema)
async def get_chat(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat

@router.put("/{chat_id}", response_model=ChatSchema)
async def update_chat(
    chat_id: int,
    chat_update: ChatUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    chat.title = chat_update.title
    chat.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(chat)
    return chat

@router.delete("/{chat_id}")
async def delete_chat(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    db.delete(chat)
    db.commit()
    return {"message": "Chat deleted successfully"}

@router.post("/{chat_id}/messages", response_model=MessageSchema)
async def send_message(
    chat_id: int,
    message: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify chat exists and belongs to user
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    # Save user message
    user_message = Message(
        chat_id=chat_id,
        role="user",
        content=message.content
    )
    db.add(user_message)
    db.commit()
    db.refresh(user_message)
    
    try:
        # Get all previous messages for context
        previous_messages = db.query(Message).filter(
            Message.chat_id == chat_id
        ).order_by(Message.created_at).all()
        
        # Format messages for OpenRouter
        messages_for_api = [
            {"role": msg.role, "content": msg.content}
            for msg in previous_messages + [user_message]
        ]
        
        # Call OpenRouter API
        reasoning_enabled = chat.model_name in ["Aurora Alpha", "Solar Pro 3", "Qwen3 VL Thinking", "GPT-OSS 120B"]
        response = await openrouter_service.chat_completion(
            model=chat.model_id,
            messages=messages_for_api,
            reasoning={"enabled": reasoning_enabled} if reasoning_enabled else None
        )
        
        # Process response
        assistant_content = response["choices"][0]["message"]["content"]
        
        # Extract code blocks
        code_blocks = []
        if chat.model_type == "text" or chat.model_type == "code":
            formatted = format_code_response(assistant_content)
            code_blocks = formatted["code_blocks"]
            assistant_content = formatted["content"]
        
        # Save assistant message
        assistant_message = Message(
            chat_id=chat_id,
            role="assistant",
            content=assistant_content,
            code_blocks=code_blocks if code_blocks else None,
            reasoning_details=response["choices"][0]["message"].get("reasoning_details")
        )
        
        db.add(assistant_message)
        
        # Update user stats
        current_user.total_generations += 1
        if response.get("usage"):
            current_user.total_tokens += response["usage"].get("total_tokens", 0)
        
        db.commit()
        db.refresh(assistant_message)
        
        return assistant_message
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@router.get("/{chat_id}/messages", response_model=List[MessageSchema])
async def get_chat_messages(
    chat_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == current_user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    messages = db.query(Message).filter(Message.chat_id == chat_id).order_by(Message.created_at).all()
    return messages