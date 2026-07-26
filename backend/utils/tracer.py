"""
DineMind AI - Execution Tracer & Telemetry Logger
Captures backend pipeline telemetry for the interactive Developer Visual Tracer Dashboard.
"""

import time
from typing import Dict, Any, List

class ExecutionTracer:
    """Records step-by-step execution details for every request."""
    
    def __init__(self, user_query: str):
        self.user_query = user_query
        self.start_time = time.time()
        self.intent = "Unknown"
        self.retrieval_ms = 0.0
        self.llm_ms = 0.0
        self.reflection_ms = 0.0
        self.total_ms = 0.0
        self.retrieved_chunks: List[Dict[str, Any]] = []
        self.formatted_prompt = ""
        self.raw_llm_response = ""
        self.is_grounded = True
        self.reflection_reason = "Self-reflection audit passed."
        self.final_response = ""
        
    def set_intent(self, intent: str):
        self.intent = intent
        
    def set_retrieval_data(self, chunks_data: List[Dict[str, Any]], elapsed_ms: float):
        self.retrieved_chunks = chunks_data
        self.retrieval_ms = elapsed_ms
        
    def set_prompt_payload(self, prompt_text: str):
        self.formatted_prompt = prompt_text
        
    def set_llm_response(self, response_text: str, elapsed_ms: float):
        self.raw_llm_response = response_text
        self.llm_ms = elapsed_ms
        
    def set_reflection_audit(self, is_grounded: bool, reason: str, elapsed_ms: float):
        self.is_grounded = is_grounded
        self.reflection_reason = reason
        self.reflection_ms = elapsed_ms
        
    def complete(self, final_output: str) -> Dict[str, Any]:
        self.final_response = final_output
        self.total_ms = round((time.time() - self.start_time) * 1000, 2)
        return self.to_dict()
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "user_query": self.user_query,
            "intent": self.intent,
            "retrieval_ms": self.retrieval_ms,
            "llm_ms": self.llm_ms,
            "reflection_ms": self.reflection_ms,
            "total_ms": self.total_ms,
            "chunk_count": len(self.retrieved_chunks),
            "retrieved_chunks": self.retrieved_chunks,
            "formatted_prompt": self.formatted_prompt,
            "raw_llm_response": self.raw_llm_response,
            "is_grounded": self.is_grounded,
            "reflection_reason": self.reflection_reason,
            "final_response": self.final_response
        }
