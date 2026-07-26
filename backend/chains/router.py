"""
DineMind AI - Intent Router Chain
Demonstrates Zero-Shot & Few-Shot Prompting with LCEL Runnable Chain.
"""

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from backend.config import API_KEY, OPENAI_API_BASE, LLM_MODEL_NAME
from backend.prompts.system_prompts import INTENT_ROUTER_PROMPT

def get_router_chain():
    """Builds an LCEL intent router chain."""
    llm = ChatOpenAI(
        api_key=API_KEY,
        openai_api_base=OPENAI_API_BASE,
        model=LLM_MODEL_NAME,
        temperature=0.0
    )
    prompt = PromptTemplate.from_template(INTENT_ROUTER_PROMPT)
    chain = prompt | llm | StrOutputParser()
    return chain

def classify_intent(query: str) -> str:
    """Classifies user intent into 'restaurant_query' or 'chitchat'."""
    try:
        chain = get_router_chain()
        result = chain.invoke({"question": query}).strip().lower()
        if "restaurant" in result:
            return "restaurant_query"
        return "chitchat"
    except Exception as e:
        print(f"Router fallback due to error: {e}")
        return "restaurant_query"
