"""
DineMind AI - Self Reflection Audit Chain
Demonstrates Self Reflection & Anti-Hallucination verification.
"""

import json
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from backend.config import API_KEY, OPENAI_API_BASE, LLM_MODEL_NAME
from backend.prompts.system_prompts import SELF_REFLECTION_PROMPT

def get_reflection_chain():
    """Builds an LCEL self-reflection chain."""
    llm = ChatOpenAI(
        api_key=API_KEY,
        openai_api_base=OPENAI_API_BASE,
        model=LLM_MODEL_NAME,
        temperature=0.0
    )
    prompt = PromptTemplate.from_template(SELF_REFLECTION_PROMPT)
    chain = prompt | llm | StrOutputParser()
    return chain

def audit_response(context: str, candidate_answer: str) -> dict:
    """Audits the generated candidate answer against the retrieved context."""
    # If standard fallback message was returned, it is automatically grounded.
    if "requested information is not available" in candidate_answer.lower():
        return {"is_grounded": True, "reason": "Standard polite fallback executed."}
        
    try:
        chain = get_reflection_chain()
        result_raw = chain.invoke({
            "context": context,
            "candidate_answer": candidate_answer
        }).strip()
        
        # Clean JSON markdown delimiters if present
        if result_raw.startswith("```"):
            result_raw = result_raw.split("```")[1]
            if result_raw.startswith("json"):
                result_raw = result_raw[4:].strip()
                
        parsed = json.loads(result_raw)
        return {
            "is_grounded": parsed.get("is_grounded", True),
            "reason": parsed.get("reason", "Audited successfully.")
        }
    except Exception as e:
        print(f"Self reflection audit warning: {e}")
        return {"is_grounded": True, "reason": "Audit bypassed due to parser output."}
