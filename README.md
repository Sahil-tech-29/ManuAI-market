# 🧠 ManuAI Market  
### GenAI Powered Manufacturer-to-Customer E-Commerce Platform

---

## 🚀 Project Overview

ManuAI Market is an AI-powered full-stack e-commerce platform that connects manufacturers directly with customers while enhancing the buying and selling experience using Generative AI. The platform eliminates intermediaries and enables manufacturers to efficiently showcase their products while helping customers make informed purchasing decisions.

Manufacturers can upload products and automatically generate optimized titles, descriptions, keywords, and pricing strategies using AI. Customers benefit from AI-powered product summaries and review insights, enabling faster and smarter decisions.

The system integrates Artificial Intelligence, full-stack development, and secure payment systems into one scalable platform.

---

## 🎯 Key Features

### 👨‍🏭 Manufacturer Module
- Upload and manage products
- AI-generated:
  - Product title  
  - Description  
  - Keywords  
  - Market analysis  
  - Smart pricing  
- Dashboard with analytics  
- Manufacturer-specific order tracking  

---

### 🧑 Customer Module
- Browse marketplace  
- Search, filter, and sort products  
- AI-powered product summaries  
- Review insights  
- Add to cart and checkout  
- View order history  

---

### 🛒 Cart System
- Add/remove items  
- Update quantity  
- Dynamic price calculation  

---

### 💳 Payment System
- Cash on Delivery (COD)  
- Razorpay integration (UPI/Card – test mode)  
- Secure payment verification (HMAC)  

---

### 📦 Order System
- Cart → Checkout → Payment → Order  
- Customer order history  
- Manufacturer order tracking  

---

## 🏗️ Tech Stack

### Backend
- Python  
- Flask  
- SQLAlchemy  
- SQLite  

### Frontend
- HTML  
- CSS (Glassmorphism UI)  
- JavaScript  

### AI Integration
- Groq API  
- LLaMA 3.1  

### Payment Gateway
- Razorpay  

---

## 🗂️ Project Structure

```bash
project/
│
├── routes/
│   ├── auth.py
│   ├── product.py
│   ├── cart.py
│   └── order.py
│
├── services/
│   ├── ai_service.py
│   ├── payment_service.py
│
├── models/
│   ├── user.py
│   ├── product.py
│   ├── order.py
│
├── utils/
│   ├── auth.py
│   └── helpers.py
│
├── static/
├── templates/
├── app.py
├── .env
├── requirements.txt
└── README.md
```

### ⚙️ Installation & Setup
1. Clone Repository
```bash
git clone https://github.com/your-username/manuai-market.git
cd manuai-market
```
2. Create Virtual Environment
```bash
python -m venv venv
```
Activate environment:

Windows
```bash
venv\Scripts\activate
```
Linux/macOS
```bash
source venv/bin/activate
```
3. Install Dependencies
```bash
pip install -r requirements.txt
```
4. Setup Environment Variables

Create a .env file in the root directory:
```bash
GROQ_API_KEY=your_api_key
RAZORPAY_KEY_ID=your_key
RAZORPAY_SECRET=your_secret
```
5. Run Application
```bash
python app.py
```
Open in browser:
```bash
http://127.0.0.1:5000
```

### 🤖 AI Features
Manufacturer Side
Automatic title generation
Description generation
Keyword extraction
Smart pricing strategy
Market insights
Customer Side
Product summaries
Review analysis

### 🔄 System Flow
Manufacturer → Upload Product → AI Enhancement → Marketplace  
Customer → Browse → Cart → Checkout → Payment → Order

### 🔐 Authentication
Session-based authentication
Role-based access:
Manufacturer
Customer

### 🗄️ Database Design
Entities
User
Product
Review
Cart
Order
OrderItem
Key Feature
manufacturer_id enables manufacturer-specific order tracking

### 🎨 UI/UX Features
Glassmorphism design
Gradient UI
Responsive layout
Smooth animations

### ⚠️ Challenges & Fixes
Issue	Fix
Database relationship error	Added ForeignKey
Cart subtotal bug	Used @property
Razorpay not opening	Fixed JS timing
SQL errors	Recreated database
AI inconsistency	Improved prompts

### 👨‍💻 Author

Sahil 
BTech CSE | AI/ML Enthusiast
