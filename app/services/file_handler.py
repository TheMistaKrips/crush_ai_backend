import os
import aiofiles
import base64
from datetime import datetime
from typing import Optional
from app.config import settings

class FileHandler:
    def __init__(self):
        self.upload_dir = settings.UPLOAD_DIR
        os.makedirs(self.upload_dir, exist_ok=True)
    
    async def save_base64_image(self, base64_data: str, filename: Optional[str] = None) -> str:
        """
        Save base64 encoded image and return file path
        """
        # Remove data URL prefix if present
        if ',' in base64_data:
            base64_data = base64_data.split(',')[1]
        
        # Decode base64
        image_data = base64.b64decode(base64_data)
        
        # Generate filename if not provided
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"image_{timestamp}.png"
        
        filepath = os.path.join(self.upload_dir, filename)
        
        async with aiofiles.open(filepath, 'wb') as f:
            await f.write(image_data)
        
        return filepath
    
    async def save_audio_file(self, audio_data: str, filename: Optional[str] = None) -> str:
        """
        Save audio file from base64 data
        """
        if ',' in audio_data:
            audio_data = audio_data.split(',')[1]
        
        audio_bytes = base64.b64decode(audio_data)
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"audio_{timestamp}.wav"
        
        filepath = os.path.join(self.upload_dir, filename)
        
        async with aiofiles.open(filepath, 'wb') as f:
            await f.write(audio_bytes)
        
        return filepath

file_handler = FileHandler()