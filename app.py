from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory storage for demonstration
bookings = {}
ALLOWED_CITIES = ["Delhi", "Bangalore"]

# 1. Validate Phone Number Tool
@app.route('/validate-phone', methods=['POST'])
def validate_phone():
    data = request.json
    phone = data.get('phone_number', '')
    is_valid = phone.isdigit() and len(phone) == 10
    return jsonify({"is_valid": is_valid})

# 2. Collect City Tool (Validation)
@app.route('/validate-city', methods=['POST'])
def validate_city():
    data = request.json
    city = data.get('city', '').strip().title()
    is_valid = city in ALLOWED_CITIES
    return jsonify({"is_valid": is_valid})

# 3. Validate Date Tool
@app.route('/validate-date', methods=['POST'])
def validate_date():
    data = request.json
    date_str = data.get('date', '')
    try:
        date = datetime.strptime(date_str, "%d-%m-%Y")
        today = datetime.now()
        is_valid = date.date() >= today.date()
    except Exception:
        is_valid = False
    return jsonify({"is_valid": is_valid})

# 4. Knowledge Base API Tool (Dummy Example)
@app.route('/knowledge-base', methods=['POST'])
def knowledge_base():
    data = request.json
    query = data.get('query', '')
    property_ = data.get('property', '')
    # Demo: always returns a canned response
    return jsonify({"answer": f"Sample answer for '{query}' about {property_}."})

# 5. Collect Name Tool (Validation)
@app.route('/collect-name', methods=['POST'])
def collect_name():
    data = request.json
    name = data.get('name', '')
    is_valid = isinstance(name, str) and len(name.strip()) > 0
    return jsonify({"is_valid": is_valid, "name": name.strip()})

# 6. Create Booking Tool
@app.route('/create-booking', methods=['POST'])
def create_booking():
    data = request.json
    name = data.get('name')
    phone_number = data.get('phone_number')
    property_ = data.get('property')
    date = data.get('date')
    if not (name and phone_number and property_ and date):
        return jsonify({"success": False, "message": "Missing required fields."}), 400
    booking_id = f"BN{len(bookings)+1:06d}"
    bookings[booking_id] = {
        "name": name,
        "phone_number": phone_number,
        "property": property_,
        "date": date
    }
    return jsonify({"success": True, "booking_id": booking_id})

# 7. Update Booking Tool
@app.route('/update-booking', methods=['POST'])
def update_booking():
    data = request.json
    booking_id = data.get('booking_id')
    new_date = data.get('new_date')
    if booking_id in bookings and new_date:
        bookings[booking_id]['date'] = new_date
        return jsonify({"success": True, "booking_id": booking_id, "new_date": new_date})
    return jsonify({"success": False, "message": "Booking not found or missing new date."}), 404

# 8. Cancel Booking Tool
@app.route('/cancel-booking', methods=['POST'])
def cancel_booking():
    data = request.json
    booking_id = data.get('booking_id')
    if booking_id in bookings:
        del bookings[booking_id]
        return jsonify({"success": True, "booking_id": booking_id})
    return jsonify({"success": False, "message": "Booking not found."}), 404

if __name__ == "__main__":
    app.run()
