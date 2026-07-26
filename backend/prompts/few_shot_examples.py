"""
DineMind AI - Few-Shot Exemplars
Demonstrating Few-Shot Prompting for Intent Routing and ReAct reasoning tuning.
"""

FEW_SHOT_ROUTER_EXAMPLES = [
    {"question": "What time do you open on Fridays?", "intent": "restaurant_query"},
    {"question": "Hi there! How are you?", "intent": "chitchat"},
    {"question": "Is the Mushroom Risotto gluten free?", "intent": "restaurant_query"},
    {"question": "Thank you so much for your help!", "intent": "chitchat"},
    {"question": "Do you deliver to downtown?", "intent": "restaurant_query"},
    {"question": "Good evening", "intent": "chitchat"}
]

FEW_SHOT_REACT_EXAMPLES = [
    {
        "input": "Which dishes contain peanuts?",
        "thought": "I need to check the Ingredients CSV for any dish where Contains Peanuts is 'Yes' or Allergens list 'Peanuts'.",
        "action": "Search Ingredients.csv for peanuts",
        "observation": "Checked all 11 dishes in Ingredients.csv. All rows list Contains Peanuts as 'No'.",
        "final_answer": "None of our dishes contain peanuts. All menu items are 100% peanut-free according to our official ingredients documentation."
    }
]
