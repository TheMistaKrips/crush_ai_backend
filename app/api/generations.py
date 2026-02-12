from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import base64
from app.database import get_db
from app.models.user import User
from app.models.generation import Generation
from app.schemas.generation import GenerationCreate, Generation as GenerationSchema, ImageGenerationRequest, AudioGenerationRequest
from app.dependencies.auth import get_current_user
from app.services.openrouter import openrouter_service
from app.services.file_handler import file_handler
from app.utils.model_mappings import get_model_by_id

router = APIRouter(prefix="/generations", tags=["generations"])

@router.post("/image")
async def generate_image(
    request: ImageGenerationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify model supports image generation
    model_info = get_model_by_id(request.model)
    if not model_info or not model_info.get("supports_images"):
        raise HTTPException(status_code=400, detail="Model does not support image generation")
    
    try:
        # Generate image
        response = await openrouter_service.generate_image(
            model=request.model,
            prompt=request.prompt,
            num_images=request.num_images
        )
        
        # Process generated images
        images = []
        if response.get("choices"):
            message = response["choices"][0]["message"]
            if message.get("images"):
                for idx, img in enumerate(message["images"]):
                    image_url = img["image_url"]["url"]
                    
                    # Save image
                    filename = f"gen_{current_user.id}_{idx}_{request.model.replace('/', '_')}.png"
                    filepath = await file_handler.save_base64_image(image_url, filename)
                    
                    images.append({
                        "url": image_url,
                        "local_path": filepath,
                        "filename": filename
                    })
        
        # Save generation record
        generation = Generation(
            user_id=current_user.id,
            model_id=request.model,
            model_name=model_info["name"],
            generation_type="image",
            prompt=request.prompt,
            result={"images": images},
            generation_metadata={
                "negative_prompt": request.negative_prompt,
                "num_images": request.num_images,
                "size": request.size
            }
        )
        
        db.add(generation)
        current_user.total_generations += 1
        db.commit()
        db.refresh(generation)
        
        return {
            "generation_id": generation.id,
            "images": images,
            "model": model_info["name"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")

@router.post("/audio")
async def generate_audio(
    prompt: str = Form(...),
    model: str = Form(...),
    audio_input: Optional[str] = Form(None),
    audio_file: Optional[UploadFile] = File(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify model supports audio
    model_info = get_model_by_id(model)
    if not model_info or not model_info.get("supports_audio"):
        raise HTTPException(status_code=400, detail="Model does not support audio processing")
    
    try:
        audio_base64 = None
        if audio_file:
            # Read and encode uploaded audio
            content = await audio_file.read()
            audio_base64 = base64.b64encode(content).decode('utf-8')
        elif audio_input:
            audio_base64 = audio_input
        
        # Process audio
        response = await openrouter_service.generate_audio(
            model=model,
            prompt=prompt,
            audio_input=audio_base64
        )
        
        # Save generation record
        generation = Generation(
            user_id=current_user.id,
            model_id=model,
            model_name=model_info["name"],
            generation_type="audio",
            prompt=prompt,
            result=response,
            generation_metadata={
                "has_audio_input": bool(audio_base64)
            }
        )
        
        db.add(generation)
        current_user.total_generations += 1
        db.commit()
        db.refresh(generation)
        
        return {
            "generation_id": generation.id,
            "response": response["choices"][0]["message"]["content"] if response.get("choices") else None
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio processing failed: {str(e)}")

@router.get("/", response_model=List[GenerationSchema])
async def get_user_generations(
    generation_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Generation).filter(Generation.user_id == current_user.id)
    
    if generation_type:
        query = query.filter(Generation.generation_type == generation_type)
    
    generations = query.order_by(Generation.created_at.desc()).all()
    return generations

@router.get("/{generation_id}", response_model=GenerationSchema)
async def get_generation(
    generation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    generation = db.query(Generation).filter(
        Generation.id == generation_id,
        Generation.user_id == current_user.id
    ).first()
    
    if not generation:
        raise HTTPException(status_code=404, detail="Generation not found")
    
    return generation