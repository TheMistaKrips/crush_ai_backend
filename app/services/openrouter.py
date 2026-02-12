import httpx
from typing import Dict, Any, List, Optional
from app.config import settings
from app.utils.model_mappings import get_model_by_id

class OpenRouterService:
    def __init__(self):
        self.base_url = settings.OPENROUTER_BASE_URL
        self.api_key = settings.OPENROUTER_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": settings.SITE_URL,
            "X-Title": settings.APP_NAME
        }
    
    async def chat_completion(
        self,
        model: str,
        messages: List[Dict[str, Any]],
        reasoning: Optional[Dict[str, bool]] = None,
        modalities: Optional[List[str]] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """
        Universal chat completion method for all model types
        """
        model_info = get_model_by_id(model)
        if not model_info:
            model_info = get_model_by_id(model.split('/')[-1])
        
        payload = {
            "model": model,
            "messages": messages
        }
        
        if reasoning and model_info and model_info.get("supports_reasoning"):
            payload["reasoning"] = reasoning
        
        if modalities:
            payload["modalities"] = modalities
        
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code != 200:
                raise Exception(f"OpenRouter API error: {response.text}")
            
            return response.json()
    
    async def generate_image(self, model: str, prompt: str, num_images: int = 1) -> Dict[str, Any]:
        """
        Generate images using compatible models
        """
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        return await self.chat_completion(
            model=model,
            messages=messages,
            modalities=["image"]
        )
    
    async def generate_audio(self, model: str, prompt: str, audio_input: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate/process audio using compatible models
        """
        content = []
        
        # Add text prompt
        content.append({
            "type": "text",
            "text": prompt
        })
        
        # Add audio if provided
        if audio_input:
            content.append({
                "type": "input_audio",
                "input_audio": {
                    "data": audio_input,
                    "format": "wav"
                }
            })
        
        messages = [
            {
                "role": "user",
                "content": content
            }
        ]
        
        return await self.chat_completion(
            model=model,
            messages=messages
        )
    
    async def analyze_image(self, model: str, prompt: str, image_url: str) -> Dict[str, Any]:
        """
        Analyze images using vision models
        """
        content = [
            {
                "type": "text",
                "text": prompt
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": image_url
                }
            }
        ]
        
        messages = [
            {
                "role": "user",
                "content": content
            }
        ]
        
        return await self.chat_completion(
            model=model,
            messages=messages
        )

openrouter_service = OpenRouterService()