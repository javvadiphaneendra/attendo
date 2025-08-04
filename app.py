from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from threading import Thread
from attendance_fetch_selenium import get_attendance
from format_attendance import format_attendance
from twilio.rest import Client
import os

app = Flask(__name__)

# Temporary storage (for production, replace with DB)
pending_registrations = {}
registered_students = {}

# Twilio credentials (keep these in environment variables)
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "YOUR_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "YOUR_AUTH_TOKEN")
TWILIO_WHATSAPP = os.getenv("TWILIO_WHATSAPP", "whatsapp:+14155238886")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def save_student(phone, student_id, password):
    registered_students[phone] = (student_id, password)

def get_student(phone):
    return registered_students.get(phone)

def send_attendance(to_number, student_id, password):
    try:
        raw_attendance = get_attendance(student_id, password)
        formatted = format_attendance(raw_attendance)
    except Exception as e:
        formatted = f"Failed to fetch attendance: {e}"

    try:
        client.messages.create(
            from_=TWILIO_WHATSAPP,
            to=to_number,
            body=formatted
        )
    except Exception as e:
        print(f"Failed to send message to {to_number}: {e}")

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From', '')  # e.g. "whatsapp:+919876543210"
    phone = from_number.replace("whatsapp:", "").strip()

    resp = MessagingResponse()
    msg = resp.message()

    # Registration flow
    if phone in pending_registrations:
        step = pending_registrations[phone].get("step")

        if step == "ask_id":
            pending_registrations[phone]["student_id"] = incoming_msg
            pending_registrations[phone]["step"] = "ask_password"
            msg.body("Please enter your College Portal password:")
            return str(resp)

        elif step == "ask_password":
            student_id = pending_registrations[phone].get("student_id")
            password = incoming_msg
            save_student(phone, student_id, password)
            del pending_registrations[phone]
            msg.body("Registration complete! You can now send 'attendance' to get your report.")
            return str(resp)

    # Check if user is registered
    student_data = get_student(phone)

    # Auto-start registration if user not registered
    if not student_data:
        pending_registrations[phone] = {"step": "ask_id"}
        msg.body("Welcome! Please enter your College Portal ID:")
        return str(resp)

    # Handle attendance request
    if incoming_msg.lower() == "attendance":
        student_id, password = student_data
        msg.body("Fetching your attendance, please wait...")
        Thread(target=send_attendance, args=(from_number, student_id, password), daemon=True).start()
        return str(resp)

    # Reset command
    if incoming_msg.lower() == "reset":
        registered_students.pop(phone, None)
        pending_registrations.pop(phone, None)
        msg.body("Your data has been reset. Please enter your College Portal ID:")
        pending_registrations[phone] = {"step": "ask_id"}
        return str(resp)

    # Default/help
    msg.body("You can type:\n- attendance (to get latest data)\n- reset (to clear your data)")
    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)
