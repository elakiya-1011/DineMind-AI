"""
DineMind AI - Conversation Memory Manager
"""
from typing import List, Dict

class ChatMemoryManager:
    """Manages conversation memory across turns."""
    
    def __init__(self, max_history: int = 10):
        self.max_history = max_history
        self.history: List[Dict[str, str]] = []
        
    def add_user_message(self, message: str):
        self.history.append({"role": "user", "content": message})
        self._truncate()
        
    def add_ai_message(self, message: str):
        self.history.append({"role": "assistant", "content": message})
        self._truncate()
        
    def get_formatted_history(self) -> str:
        """Formats conversation history as a clean transcript string."""
        if not self.history:
            return "No previous conversation history."
            
        formatted = []
        for msg in self.history[-self.max_history:]:
            role_label = "Customer" if msg["role"] == "user" else "DineMind Assistant"
            formatted.append(f"{role_label}: {msg['content']}")
            
        return "\n".join(formatted)

    def _truncate(self):
        if len(self.history) > self.max_history * 2:
            self.history = self.history[-self.max_history * 2:]

    def clear(self):
        self.history = []
