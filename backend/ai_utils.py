from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_description(product_name, category):

    prompt = f"""
Write a professional ecommerce product description for:

Product: {product_name}
Category: {category}

Format the response in this structured layout using markdown:

## Product Overview
Write 2–3 lines describing the product.

## Key Features
Provide 5 bullet points describing main benefits.

## Specifications
Provide technical details such as size, material, usage, durability etc.

## Ideal For
Mention who should use this product.

Make it attractive like Amazon product listings.
Do not include any extra explanation.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content




def generate_title(product_name, category):

    prompt = f"""
Generate a professional ecommerce product title.

Product Name: {product_name}
Category: {category}

The title should:
• be SEO optimized
• sound like an Amazon product title
• be under 15 words
• highlight key benefit

Return ONLY the title.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content.strip()



def generate_keywords(product_name, category):

    prompt = f"""
Generate SEO keywords for an ecommerce product.

Product: {product_name}
Category: {category}

Return the response in this format:

## SEO Keywords

- keyword 1
- keyword 2
- keyword 3
- keyword 4
- keyword 5
- keyword 6
- keyword 7
- keyword 8

Do not include extra explanation.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content




def generate_market_analysis(product_name, category, cost):

    prompt = f"""
Analyze the ecommerce market for this product.

Product: {product_name}
Category: {category}
Manufacturing Cost: ₹{cost}

Return response in this format:

## Market Price Range
Give estimated price range of similar products.

## Common Competitor Features
List 4–5 features competitors usually provide in bullet points.

## Pricing Strategy
Suggest competitive pricing for this product.

Keep the explanation short.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content



def generate_final_price(product_name, category, cost):

    prompt = f"""
Determine the final selling price for this product.

Product: {product_name}
Category: {category}
Manufacturing Cost: ₹{cost}

Return response in this format:

## Final Selling Price
₹<price>

## Profit Margin
<percentage>%

Keep it minimal.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content