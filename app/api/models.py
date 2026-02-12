from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
from app.utils.model_mappings import MODELS, get_models_by_type, get_model_by_id
from app.dependencies.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/models", tags=["models"])

@router.get("/")
async def get_all_models(current_user: User = Depends(get_current_user)):
    """Get all available models"""
    return {
        "models": [
            {
                "id": model["id"],
                "name": model["name"],
                "type": model["type"],
                "capabilities": model["capabilities"],
                "description": model["description"],
                "free": model["free"]
            }
            for model in MODELS.values()
        ]
    }

@router.get("/{model_type}")
async def get_models_by_type_endpoint(
    model_type: str,
    current_user: User = Depends(get_current_user)
):
    """Get models by type (text, image, audio, vision)"""
    models = get_models_by_type(model_type)
    return {
        "type": model_type,
        "models": [
            {
                "id": model["id"],
                "name": model["name"],
                "capabilities": model["capabilities"],
                "description": model["description"]
            }
            for model in models
        ]
    }

@router.get("/model/{model_id}")
async def get_model_info(
    model_id: str,
    current_user: User = Depends(get_current_user)
):
    """Get specific model information"""
    model = get_model_by_id(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    
    return model