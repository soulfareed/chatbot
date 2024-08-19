from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sqlite3

app = FastAPI()

# Connect to SQLite database
conn = sqlite3.connect('chatbot.db', check_same_thread=False)
cursor = conn.cursor()

# Create table for storing user details
cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (id INTEGER PRIMARY KEY, name TEXT, email TEXT, phone TEXT, service TEXT)''')
conn.commit()

# Define Pydantic models for request and response bodies
class UserDetails(BaseModel):
    name: str
    email: str
    phone: str
    service: str

class ServiceOption(BaseModel):
    option: str

@app.post("/user/")
async def capture_user_details(user: UserDetails):
    cursor.execute("INSERT INTO users (name, email, phone, service) VALUES (?, ?, ?, ?)", 
                   (user.name, user.email, user.phone, user.service))
    conn.commit()
    return {"message": "User details captured successfully"}

@app.post("/service/")
async def service_options(service: ServiceOption):
    options = {
        "form": "Fill in a Form",
        "call": "Call a Contractor",
        "appointment": "Set an Appointment"
    }
    return {"options": options.get(service.option.lower(), "Invalid Option")}

@app.get("/faq/")
async def faq(question: str):
    faqs = {
        "pricing": "The average cost of plumbing services is around $100-$150 per hour.",
        "availability": "Most contractors are available Monday to Friday from 8 AM to 6 PM.",
        "ratings": "All our contractors are highly rated with at least 4.5 stars."
    }
    return {"answer": faqs.get(question.lower(), "FAQ not available")}

@app.get("/")
async def root():
    return {"message": "Welcome to the Home Improvement Chatbot!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
