import re
from typing import List, Dict, Any

def extract_code_blocks(text: str) -> List[Dict[str, Any]]:
    """
    Extract code blocks from markdown text
    Returns list of dicts with language and code
    """
    pattern = r'```(\w+)?\n(.*?)```'
    matches = re.findall(pattern, text, re.DOTALL)
    
    code_blocks = []
    for match in matches:
        language = match[0] if match[0] else 'text'
        code = match[1].strip()
        code_blocks.append({
            'language': language,
            'code': code,
            'length': len(code)
        })
    
    return code_blocks

def format_code_response(content: str) -> Dict[str, Any]:
    """
    Format response with code blocks and regular text
    """
    code_blocks = extract_code_blocks(content)
    
    # Remove code blocks from content for plain text version
    plain_text = re.sub(r'```(\w+)?\n.*?```', '[Code Block]', content, flags=re.DOTALL)
    
    return {
        'content': content,
        'plain_text': plain_text,
        'code_blocks': code_blocks,
        'has_code': len(code_blocks) > 0
    }