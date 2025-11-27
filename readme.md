# Django Subscription & Payments Backend

A mini subscription management backend built using **Django** and **Django REST Framework**, as per the assignment requirements (26 NOV, 2025).  
Includes JWT authentication, subscription plans, payment webhook simulation, and admin dashboard APIs.

---

## 🚀 Features

### **1. User Authentication**
- User Signup
- User Login
- JWT Authentication using SimpleJWT

### **2. Subscription Plans**
- List all plans
- Get single plan detail

### **3. User Subscription System**
- Create a subscription (pending)
- Auto-calculate `end_date`
- Fetch active subscription
- Auto-expire old subscriptions

### **4. Webhook Simulation**
- Activate subscription using:


### **5. Admin Dashboard APIs (Superuser Only)**
- List all users with their latest subscription
- List all expired subscriptions

---

## 🛠 Tech Stack

- **Python 3**
- **Django 4+**
- **Django REST Framework**
- **SimpleJWT**
- **SQLite/PostgreSQL** (any DB works)




