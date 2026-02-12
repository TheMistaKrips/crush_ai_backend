from typing import Dict, List, Any

# Полный список моделей OpenRouter (бесплатные)
MODELS: Dict[str, Dict[str, Any]] = {
    # Text/Code модели с reasoning
    "aurora-alpha": {
        "id": "openrouter/aurora-alpha",
        "name": "Aurora Alpha",
        "type": "text",
        "capabilities": ["text", "code", "reasoning"],
        "supports_reasoning": True,
        "supports_images": False,
        "supports_audio": False,
        "supports_vision": False,
        "free": True,
        "description": "Advanced reasoning model with chain-of-thought"
    },
    "solar-pro-3": {
        "id": "upstage/solar-pro-3:free",
        "name": "Solar Pro 3",
        "type": "text",
        "capabilities": ["text", "code", "reasoning"],
        "supports_reasoning": True,
        "supports_images": False,
        "supports_audio": False,
        "supports_vision": False,
        "free": True,
        "description": "Efficient reasoning model"
    },
    "liquid-lfm-thinking": {
        "id": "liquid/lfm-2.5-1.2b-thinking:free",
        "name": "LiquidAI LFM 2.5 Thinking",
        "type": "text",
        "capabilities": ["text", "code"],
        "supports_reasoning": False,
        "supports_images": False,
        "supports_audio": False,
        "supports_vision": False,
        "free": True,
        "description": "Lightweight thinking model"
    },
    "qwen3-vl": {
        "id": "qwen/qwen3-vl-30b-a3b-thinking",
        "name": "Qwen3 VL Thinking",
        "type": "vision",
        "capabilities": ["text", "code", "vision", "reasoning"],
        "supports_reasoning": True,
        "supports_images": True,
        "supports_audio": False,
        "supports_vision": True,
        "free": True,
        "description": "Vision-language model with reasoning"
    },
    "gpt-oss-120b": {
        "id": "openai/gpt-oss-120b:free",
        "name": "GPT-OSS 120B",
        "type": "text",
        "capabilities": ["text", "code", "reasoning"],
        "supports_reasoning": True,
        "supports_images": False,
        "supports_audio": False,
        "supports_vision": False,
        "free": True,
        "description": "Open source GPT with 120B parameters"
    },
    "deepseek-r1t2": {
        "id": "tngtech/deepseek-r1t2-chimera:free",
        "name": "DeepSeek R1T2 Chimera",
        "type": "text",
        "capabilities": ["text", "code"],
        "supports_reasoning": False,
        "supports_images": False,
        "supports_audio": False,
        "supports_vision": False,
        "free": True,
        "description": "Advanced reasoning model"
    },
    "deepseek-r1": {
        "id": "deepseek/deepseek-r1-0528:free",
        "name": "DeepSeek R1",
        "type": "text",
        "capabilities": ["text", "code"],
        "supports_reasoning": False,
        "supports_images": False,
        "supports_audio": False,
        "supports_vision": False,
        "free": True,
        "description": "State-of-the-art reasoning"
    },
    "hermes-3": {
        "id": "nousresearch/hermes-3-llama-3.1-405b:free",
        "name": "Hermes 3 405B",
        "type": "text",
        "capabilities": ["text", "code"],
        "supports_reasoning": False,
        "supports_images": False,
        "supports_audio": False,
        "supports_vision": False,
        "free": True,
        "description": "Powerful instruction-tuned model"
    },
    "gemma-3": {
        "id": "google/gemma-3-27b-it:free",
        "name": "Google Gemma 3",
        "type": "vision",
        "capabilities": ["text", "code", "vision"],
        "supports_reasoning": False,
        "supports_images": True,
        "supports_audio": False,
        "supports_vision": True,
        "free": True,
        "description": "Google's vision-language model"
    },
    "llama-3.3": {
        "id": "meta-llama/llama-3.3-70b-instruct:free",
        "name": "Meta Llama 3.3",
        "type": "text",
        "capabilities": ["text", "code"],
        "supports_reasoning": False,
        "supports_images": False,
        "supports_audio": False,
        "supports_vision": False,
        "free": True,
        "description": "Meta's latest instruction model"
    },
    
    # Audio модели
    "gpt-audio-mini": {
        "id": "openai/gpt-audio-mini",
        "name": "GPT Audio Mini",
        "type": "audio",
        "capabilities": ["audio", "text"],
        "supports_reasoning": False,
        "supports_images": False,
        "supports_audio": True,
        "supports_vision": False,
        "free": True,
        "description": "Audio understanding and generation"
    },
    
    # Image модели
    "riverflow-v2": {
        "id": "sourceful/riverflow-v2-pro",
        "name": "Riverflow V2 Pro",
        "type": "image",
        "capabilities": ["image"],
        "supports_reasoning": False,
        "supports_images": True,
        "supports_audio": False,
        "supports_vision": False,
        "free": True,
        "description": "Image generation model"
    },
    "seedream-4.5": {
        "id": "bytedance-seed/seedream-4.5",
        "name": "Seedream 4.5",
        "type": "image",
        "capabilities": ["image"],
        "supports_reasoning": False,
        "supports_images": True,
        "supports_audio": False,
        "supports_vision": False,
        "free": True,
        "description": "High-quality image generation"
    },
    "flux-2-max": {
        "id": "black-forest-labs/flux.2-max",
        "name": "FLUX.2 Max",
        "type": "image",
        "capabilities": ["image"],
        "supports_reasoning": False,
        "supports_images": True,
        "supports_audio": False,
        "supports_vision": False,
        "free": True,
        "description": "Professional image generation"
    },
    "flux-2-pro": {
        "id": "black-forest-labs/flux.2-pro",
        "name": "FLUX.2 Pro",
        "type": "image",
        "capabilities": ["image"],
        "supports_reasoning": False,
        "supports_images": True,
        "supports_audio": False,
        "supports_vision": False,
        "free": True,
        "description": "Professional image generation"
    }
}

def get_models_by_type(model_type: str) -> List[Dict]:
    """Get all models of a specific type"""
    return [model for model in MODELS.values() if model["type"] == model_type]

def get_model_by_id(model_id: str) -> Dict:
    """Get model info by ID"""
    for key, model in MODELS.items():
        if model["id"] == model_id or key == model_id:
            return model
    return None