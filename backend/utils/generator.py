import os
import csv
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from backend.config import DOCUMENTS_DIR

def create_pdf(filename: str, title: str, content_paragraphs: list):
    """Generates a structured PDF file using ReportLab."""
    filepath = DOCUMENTS_DIR / filename
    doc = SimpleDocTemplate(str(filepath), pagesize=letter)
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=12,
        textColor='#FF6B6B'
    )
    
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        spaceAfter=8
    )
    
    story = [Paragraph(title, title_style), Spacer(1, 10)]
    for p_text in content_paragraphs:
        story.append(Paragraph(p_text, body_style))
        story.append(Spacer(1, 4))
        
    doc.build(story)

def generate_default_documents():
    """Generates all 6 required default restaurant documents if missing."""
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Menu.pdf
    menu_pdf = DOCUMENTS_DIR / "Menu.pdf"
    if not menu_pdf.exists():
        content = [
            "<b>Appetizers:</b>",
            "• Truffle Mushroom Bruschetta - $14.50 (Vegetarian)",
            "• Crispy Calamari with Lemon Aioli - $16.00",
            "• Roasted Tomato & Basil Soup - $10.00 (Vegan, Gluten-Free)",
            "<br/><b>Main Courses:</b>",
            "• Grilled Atlantic Salmon with Herb Butter & Asparagus - $28.00 (Gluten-Free)",
            "• Classic Margherita Pizza with Fresh Mozzarella - $18.00 (Vegetarian)",
            "• Wild Mushroom Risotto - $22.00 (Vegetarian, Gluten-Free option)",
            "• Wagyu Beef Burger with Truffle Fries - $24.00",
            "• Creamy Vegan Avocado Pasta - $20.00 (Vegan)",
            "<br/><b>Desserts:</b>",
            "• Classic Tiramisu - $9.50 (Contains Dairy & Eggs)",
            "• Molten Chocolate Lava Cake with Vanilla Gelato - $11.00",
            "• Vegan Mango Sorbet - $8.00 (Vegan, Dairy-Free)",
            "<br/><b>Beverages:</b>",
            "• Freshly Squeezed Orange Juice - $5.50",
            "• Artisanal Cappuccino - $4.50",
            "• Signature Mint Lime Cooler - $6.00"
        ]
        create_pdf("Menu.pdf", "DineMind Bistro - Official Menu", content)

    # 2. Restaurant_FAQ.pdf
    faq_pdf = DOCUMENTS_DIR / "Restaurant_FAQ.pdf"
    if not faq_pdf.exists():
        content = [
            "<b>Q: What are your operating hours?</b>",
            "A: We are open Monday through Thursday from 11:00 AM to 10:00 PM, Friday and Saturday from 11:00 AM to 11:00 PM, and Sunday from 10:00 AM to 9:00 PM.",
            "<br/><b>Q: Do you accept reservations?</b>",
            "A: Yes, table reservations can be made online via our website or by calling us at (555) 123-4567 up to 30 days in advance.",
            "<br/><b>Q: What payment methods do you accept?</b>",
            "A: We accept Cash, Major Credit Cards (Visa, MasterCard, Amex), Apple Pay, Google Pay, and DineMind Gift Cards.",
            "<br/><b>Q: Do you cater to dietary restrictions?</b>",
            "A: Yes! We offer extensive Vegetarian, Vegan, Gluten-Free, and Nut-Free options clearly marked on our menu.",
            "<br/><b>Q: Is parking available?</b>",
            "A: Complimentary valet parking is available every evening starting from 5:00 PM."
        ]
        create_pdf("Restaurant_FAQ.pdf", "DineMind Bistro - Frequently Asked Questions", content)

    # 3. Restaurant_Policies.pdf
    pol_pdf = DOCUMENTS_DIR / "Restaurant_Policies.pdf"
    if not pol_pdf.exists():
        content = [
            "<b>Table Reservation & Cancellation Policy:</b>",
            "Reservations must be cancelled at least 2 hours prior to the reserved time slot. Parties larger than 6 require a 24-hour advance cancellation to avoid a $20 per-person fee.",
            "<br/><b>Dress Code Policy:</b>",
            "We maintain a Smart Casual dress code. Athletic wear, beachwear, and flip-flops are prohibited in the dining room.",
            "<br/><b>Outside Food & Beverage Policy:</b>",
            "No outside food or drinks are allowed, except for celebratory birthday cakes, subject to a $15 corkage/plating fee.",
            "<br/><b>Pet Policy:</b>",
            "Service animals are welcome indoors. Pets are strictly restricted to our outdoor patio area."
        ]
        create_pdf("Restaurant_Policies.pdf", "DineMind Bistro - General Policies", content)

    # 4. Delivery_Policy.pdf
    del_pdf = DOCUMENTS_DIR / "Delivery_Policy.pdf"
    if not del_pdf.exists():
        content = [
            "<b>Delivery Coverage & Timing:</b>",
            "We provide home delivery within a 7-mile radius of the restaurant. Estimated delivery time is 35-50 minutes.",
            "<br/><b>Minimum Order & Fees:</b>",
            "Minimum order amount for home delivery is $25.00. Delivery fee is $3.99 for orders under $50, and FREE for orders over $50.",
            "<br/><b>Packaging & Food Safety:</b>",
            "All delivery items are packed in eco-friendly tamper-evident thermal containers to maintain peak heat and freshness.",
            "<br/><b>Delivery Partners:</b>",
            "Orders can be placed directly on our app or via DoorDash, UberEats, and Grubhub."
        ]
        create_pdf("Delivery_Policy.pdf", "DineMind Bistro - Delivery Policy", content)

    # 5. Offers.pdf
    off_pdf = DOCUMENTS_DIR / "Offers.pdf"
    if not off_pdf.exists():
        content = [
            "<b>Active Promotional Offers & Discounts:</b>",
            "1. <b>Happy Hour Special:</b> 30% OFF all appetizers and mocktails Monday to Thursday between 4:00 PM and 6:30 PM.",
            "2. <b>Weekend Brunch Bundle:</b> Free mimosa or specialty smoothie with any breakfast entree on Saturdays & Sundays.",
            "3. <b>First Order Discount:</b> Use promo code 'DINEMIND15' to get 15% OFF your first online delivery order.",
            "4. <b>Student & Senior Discount:</b> 10% discount available upon presentation of valid ID (Monday to Wednesday only)."
        ]
        create_pdf("Offers.pdf", "DineMind Bistro - Active Offers & Discounts", content)

    # 6. Ingredients.csv
    csv_file = DOCUMENTS_DIR / "Ingredients.csv"
    if not csv_file.exists():
        rows = [
            ["Dish Name", "Category", "Is Vegetarian", "Is Vegan", "Is Gluten Free", "Contains Peanuts", "Allergens"],
            ["Truffle Mushroom Bruschetta", "Appetizer", "Yes", "No", "No", "No", "Gluten, Dairy"],
            ["Crispy Calamari", "Appetizer", "No", "No", "No", "No", "Seafood, Gluten"],
            ["Roasted Tomato Soup", "Appetizer", "Yes", "Yes", "Yes", "No", "None"],
            ["Grilled Atlantic Salmon", "Main Course", "No", "No", "Yes", "No", "Fish, Dairy"],
            ["Margherita Pizza", "Main Course", "Yes", "No", "No", "No", "Gluten, Dairy"],
            ["Wild Mushroom Risotto", "Main Course", "Yes", "No", "Yes", "No", "Dairy"],
            ["Wagyu Beef Burger", "Main Course", "No", "No", "No", "No", "Gluten, Dairy"],
            ["Creamy Vegan Avocado Pasta", "Main Course", "Yes", "Yes", "No", "No", "Gluten"],
            ["Classic Tiramisu", "Dessert", "Yes", "No", "No", "No", "Dairy, Eggs, Gluten"],
            ["Molten Chocolate Lava Cake", "Dessert", "Yes", "No", "No", "No", "Dairy, Eggs, Gluten"],
            ["Vegan Mango Sorbet", "Dessert", "Yes", "Yes", "Yes", "No", "None"]
        ]
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(rows)
