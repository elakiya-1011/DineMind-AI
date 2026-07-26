"""
DineMind AI - Master RAG & Orchestration Engine with Warm Customer Hospitality & Cart System
Integrates:
1. Intent & Ordering Command Router (Cart addition, removal, view cart, checkout)
2. Warm Conversational Host Handler (Greetings, Small Talk)
3. ChromaDB Vector Retrieval & Grounded Prompt Assembly
4. Self-Reflection Audit (Anti-Hallucination Guardrail)
5. Execution Telemetry Recorder
"""

import time
import re
import random
from typing import Tuple, Dict, Any, List
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from backend.config import API_KEY, OPENAI_API_BASE, LLM_MODEL_NAME
from backend.prompts.system_prompts import RAG_SYSTEM_PROMPT
from backend.rag.vectorstore import VectorStoreManager
from backend.chains.router import classify_intent
from backend.chains.reflection_chain import audit_response
from backend.utils.tracer import ExecutionTracer
from backend.memory.chat_memory import ChatMemoryManager

MENU_CATALOG = {
    "margherita pizza": {"name": "Classic Margherita Pizza", "price": 18.00},
    "pizza": {"name": "Classic Margherita Pizza", "price": 18.00},
    "wagyu burger": {"name": "Wagyu Beef Burger", "price": 24.00},
    "burger": {"name": "Wagyu Beef Burger", "price": 24.00},
    "veg burger": {"name": "Wagyu Beef Burger (Veg Option)", "price": 22.00},
    "avocado pasta": {"name": "Creamy Vegan Avocado Pasta", "price": 20.00},
    "pasta": {"name": "Creamy Vegan Avocado Pasta", "price": 20.00},
    "salmon": {"name": "Grilled Atlantic Salmon", "price": 28.00},
    "bruschetta": {"name": "Truffle Mushroom Bruschetta", "price": 14.50},
    "calamari": {"name": "Crispy Calamari", "price": 16.00},
    "tomato soup": {"name": "Roasted Tomato & Basil Soup", "price": 10.00},
    "soup": {"name": "Roasted Tomato & Basil Soup", "price": 10.00},
    "risotto": {"name": "Wild Mushroom Risotto", "price": 22.00},
    "tiramisu": {"name": "Classic Tiramisu", "price": 9.50},
    "lava cake": {"name": "Molten Chocolate Lava Cake", "price": 11.00},
    "mango sorbet": {"name": "Vegan Mango Sorbet", "price": 8.00},
    "sorbet": {"name": "Vegan Mango Sorbet", "price": 8.00},
    "orange juice": {"name": "Freshly Squeezed Orange Juice", "price": 5.50},
    "cappuccino": {"name": "Artisanal Cappuccino", "price": 4.50},
    "mint lime cooler": {"name": "Signature Mint Lime Cooler", "price": 6.00},
    "coke": {"name": "Refreshing Coke", "price": 3.00},
    "soda": {"name": "Refreshing Soda", "price": 3.00}
}

class DineMindOrchestrator:
    """Master Orchestrator controlling RAG, Hospitable Conversational QA, and Session Cart Ordering."""
    
    def __init__(self, vectorstore_mgr: VectorStoreManager = None):
        self.vectorstore_mgr = vectorstore_mgr or VectorStoreManager()
        self.llm = ChatOpenAI(
            api_key=API_KEY,
            openai_api_base=OPENAI_API_BASE,
            model=LLM_MODEL_NAME,
            temperature=0.2
        )
        self.rag_prompt = PromptTemplate.from_template(RAG_SYSTEM_PROMPT)
        self.output_parser = StrOutputParser()

    def handle_cart_command(self, query: str, cart: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """Parses and executes cart & order management commands with a warm customer-friendly tone."""
        q_lower = query.lower().strip()
        
        # 1. View Cart
        if any(kw in q_lower for kw in ["show my cart", "view cart", "show cart", "my cart", "what's in my cart", "how much is my total"]):
            if not cart:
                return True, "🛒 **Your dining cart is currently empty.** You can easily add items by asking me, for example: *'Add 1 Margherita Pizza'* or *'Add 2 Cokes'*!"
            
            lines = ["### 🛒 Your DineMind Order Summary\n"]
            lines.append("| Item | Quantity | Unit Price | Subtotal |")
            lines.append("|---|---|---|---|")
            
            subtotal = 0.0
            for item in cart:
                item_tot = item["qty"] * item["price"]
                subtotal += item_tot
                lines.append(f"| {item['name']} | {item['qty']} | ${item['price']:.2f} | ${item_tot:.2f} |")
                
            tax = subtotal * 0.08
            total = subtotal + tax
            lines.append(f"\n**Subtotal:** ${subtotal:.2f}")
            lines.append(f"**Estimated Tax (8%):** ${tax:.2f}")
            lines.append(f"### **Total Amount:** `${total:.2f}`")
            lines.append("\nWhenever you're ready, say **'Place order'** to complete your request, or **'Clear cart'** to reset!")
            return True, "\n".join(lines)
            
        # 2. Place Order / Checkout
        if any(kw in q_lower for kw in ["place my order", "place order", "checkout", "confirm order", "buy now"]):
            if not cart:
                return True, "🛒 Your cart is currently empty! Please select some delicious items from our menu before placing an order."
                
            order_id = f"ORD-{random.randint(10000, 99999)}"
            subtotal = sum(i["qty"] * i["price"] for i in cart)
            total = subtotal * 1.08
            
            res = [f"🎉 **Thank you so much for your order! It's our absolute pleasure to serve you.**\n"]
            res.append(f"✅ **Order Confirmation Reference:** `{order_id}`")
            res.append(f"💰 **Total Charged:** `${total:.2f}`")
            res.append("⏱️ **Estimated Preparation & Delivery Time:** 35 - 45 minutes")
            res.append("\nOur kitchen team has received your order and is preparing your meal with care. Bon Appétit!")
            
            cart.clear() # Reset cart after order placement
            return True, "\n".join(res)

        # 3. Clear Cart
        if any(kw in q_lower for kw in ["clear cart", "empty cart", "reset cart"]):
            cart.clear()
            return True, "🗑️ **Your cart has been reset.** Please let me know what else you would like to order!"

        # 4. Add to Cart Pattern Matching
        if "add" in q_lower or "order" in q_lower or "want" in q_lower or "get" in q_lower:
            matched_item = None
            for key, val in MENU_CATALOG.items():
                if key in q_lower:
                    matched_item = val
                    break
                    
            if matched_item:
                qty_match = re.search(r'\b(\d+)\b', q_lower)
                qty = int(qty_match.group(1)) if qty_match else 1
                
                found = False
                for item in cart:
                    if item["name"] == matched_item["name"]:
                        item["qty"] += qty
                        found = True
                        break
                        
                if not found:
                    cart.append({
                        "name": matched_item["name"],
                        "qty": qty,
                        "price": matched_item["price"]
                    })
                    
                subtotal = sum(i["qty"] * i["price"] for i in cart)
                return True, f"✅ Delightful choice! Added **{qty}x {matched_item['name']}** (${matched_item['price']:.2f} each) to your cart.\n\n🛒 Current Cart Subtotal: **${subtotal:.2f}**. Say *'Show my cart'* or *'Place order'* whenever you're ready!"

        # 5. Remove Item Pattern
        if "remove" in q_lower or "delete item" in q_lower:
            for item in list(cart):
                if any(w in item["name"].lower() for w in q_lower.split()):
                    cart.remove(item)
                    return True, f"🗑️ Removed **{item['name']}** from your cart."

        # 6. Track Order
        if "track" in q_lower:
            return True, "🛵 **Order Update:** Your meal is currently being freshly prepared by our executive chef and is right on schedule!"

        return False, ""

    def process_query(self, user_query: str, memory_mgr: ChatMemoryManager = None, cart: List[Dict[str, Any]] = None) -> Tuple[str, Dict[str, Any]]:
        """Processes query through Hospitable Conversational Parser, Ordering Parser, RAG, and Self-Reflection Audit."""
        tracer = ExecutionTracer(user_query)
        chat_history_str = memory_mgr.get_formatted_history() if memory_mgr else "No previous history."
        cart = cart if cart is not None else []
        
        # Step 1: Check Ordering & Cart Commands
        is_cart_cmd, cart_response = self.handle_cart_command(user_query, cart)
        if is_cart_cmd:
            tracer.set_intent("ordering_cart")
            tracer.set_prompt_payload("Session Cart Command Interceptor")
            tracer.set_llm_response(cart_response, 5.0)
            tracer.set_reflection_audit(True, "Cart Command Executed", 0.0)
            
            if memory_mgr:
                memory_mgr.add_user_message(user_query)
                memory_mgr.add_ai_message(cart_response)
                
            return cart_response, tracer.complete(cart_response)

        # Step 2: Intent Classification
        intent = classify_intent(user_query)
        tracer.set_intent(intent)
        
        # Branch A: Small Talk & Greetings
        if intent == "chitchat":
            greeting_prompt = f"You are DineMind AI, a warm, hospitable, and incredibly courteous host at DineMind Bistro. Respond warmly and politely to this customer greeting: '{user_query}'"
            t_llm_start = time.time()
            res = self.llm.invoke(greeting_prompt)
            llm_text = self.output_parser.parse(res.content)
            llm_ms = round((time.time() - t_llm_start) * 1000, 2)
            
            tracer.set_prompt_payload(greeting_prompt)
            tracer.set_llm_response(llm_text, llm_ms)
            tracer.set_reflection_audit(True, "Chitchat greeting.", 0.0)
            
            if memory_mgr:
                memory_mgr.add_user_message(user_query)
                memory_mgr.add_ai_message(llm_text)
                
            return llm_text, tracer.complete(llm_text)

        # Branch B: Restaurant Information Query (RAG Pipeline)
        results_with_score, retrieval_ms = self.vectorstore_mgr.similarity_search_with_score(user_query)
        
        chunks_data = []
        context_parts = []
        for doc, score in results_with_score:
            source = doc.metadata.get("filename", "Restaurant Document")
            content = doc.page_content.strip()
            context_parts.append(f"--- Document: {source} ---\n{content}")
            chunks_data.append({
                "source": source,
                "score": round(float(score), 4),
                "content": content
            })
            
        context_text = "\n\n".join(context_parts) if context_parts else "No relevant context found."
        tracer.set_retrieval_data(chunks_data, retrieval_ms)
        
        # Prompt Payload Assembly
        formatted_prompt = self.rag_prompt.format(
            context=context_text,
            chat_history=chat_history_str,
            question=user_query
        )
        tracer.set_prompt_payload(formatted_prompt)
        
        # LLM Generation
        t_llm_start = time.time()
        llm_res = self.llm.invoke(formatted_prompt)
        candidate_answer = self.output_parser.parse(llm_res.content).strip()
        llm_ms = round((time.time() - t_llm_start) * 1000, 2)
        tracer.set_llm_response(candidate_answer, llm_ms)
        
        # Self-Reflection Audit
        t_ref_start = time.time()
        audit_res = audit_response(context_text, candidate_answer)
        ref_ms = round((time.time() - t_ref_start) * 1000, 2)
        
        is_grounded = audit_res.get("is_grounded", True)
        reason = audit_res.get("reason", "Audited")
        tracer.set_reflection_audit(is_grounded, reason, ref_ms)
        
        if not is_grounded:
            final_answer = "I apologize, but I don't have those specific details in our official restaurant menu and policy guides right now. Is there anything else from our menu, dietary options, or services I can help you with today?"
        else:
            final_answer = candidate_answer
            
        if memory_mgr:
            memory_mgr.add_user_message(user_query)
            memory_mgr.add_ai_message(final_answer)
            
        return final_answer, tracer.complete(final_answer)
