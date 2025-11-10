# 💇‍♂️ SalonHub — Real-Time Salon Appointment Booking System

SalonHub is a **real-time Salon Appointment Booking Web App** built using **Python (Django)** for the backend and **React.js** for the frontend.  
This app allows users to view salon services by gender, choose subcategories (like Hair, Facial), select available time slots, and make bookings — while admins can manage all services, categories, and bookings via custom APIs.

---

## 🚀 Features

### 👤 User Side
- Register & Login using **JWT Authentication**
- View all salon services categorized by **Male / Female**
- Explore subcategories (Hair, Facial, etc.)
- View detailed services (Haircut, Hair Wash, etc.)
- Add services to cart and calculate total price
- Book appointments (date & time slot)
- View current and past bookings

### 👨‍💼 Admin Side
- Custom admin login (no Django default admin)
- Manage Gender, SubCategory, and Service via REST APIs
- Create / Read / Update / Delete (CRUD) operations
- Manage bookings and user details
- JWT-secured access with role-based permissions

---

## 🏗️ Project Structure


SalonHub/
│
├── backend/
│ ├── backend/ # Main Django settings & URLs
│ ├── accounts/ # Authentication & Role Management
│ ├── catalog/ # Gender, SubCategory, Service APIs
│ ├── bookings/ # (future) Appointment Booking Module
│ ├── manage.py
│ ├── requirements.txt



---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-------------|
| **Backend** | Python 3.13, Django 5.2, Django REST Framework |
| **Auth** | JWT (SimpleJWT) |
| **Database** | SQLite (Dev) / MySQL (Production) |
| **Frontend** | React.js |
| **Image Handling** | Pillow |
| **Environment** | Virtualenv |

---

## 🧩 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/santhokumarp/SalonHub.git
cd SalonHub
