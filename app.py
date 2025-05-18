from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

# In-memory storage for demonstration
bookings = {}
ALLOWED_CITIES = ["Delhi", "Bangalore"]

# Homepage route
@app.route('/')
def home():
    return """
    <html>
        <head>
            <title>Property Booking API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                h1 { color: #333; }
                h2 { color: #555; }
                code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }
                .api-tester { margin-top: 30px; padding: 20px; background: #f8f8f8; border-radius: 5px; }
                button { padding: 8px 16px; background: #4CAF50; color: white; border: none; cursor: pointer; }
                input, select { padding: 8px; margin: 5px 0; width: 300px; }
                #response { margin-top: 20px; padding: 10px; background: #e9e9e9; border-radius: 3px; white-space: pre-wrap; }
            </style>
            <script>
                async function testEndpoint() {
                    const endpoint = document.getElementById('endpoint').value;
                    const data = document.getElementById('jsonData').value;
                    const responseArea = document.getElementById('response');
                    
                    try {
                        const parsedData = JSON.parse(data);
                        const response = await fetch(endpoint, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify(parsedData)
                        });
                        
                        const result = await response.json();
                        responseArea.textContent = JSON.stringify(result, null, 2);
                    } catch (error) {
                        responseArea.textContent = `Error: ${error.message}`;
                    }
                }
            </script>
        </head>
        <body>
            <h1>Property Booking API</h1>
            <p>Welcome to the Property Booking API. Below are the available endpoints:</p>
            
            <h2>Endpoints:</h2>
            <ul>
                <li><code>/validate-phone</code> - Validate phone numbers</li>
                <li><code>/validate-city</code> - Validate city names</li>
                <li><code>/validate-date</code> - Validate booking dates</li>
                <li><code>/collect-name</code> - Validate customer names</li>
                <li><code>/create-booking</code> - Create a new booking</li>
                <li><code>/update-booking</code> - Update an existing booking</li>
                <li><code>/cancel-booking</code> - Cancel a booking</li>
            </ul>
            
            <div class="api-tester">
                <h2>API Tester</h2>
                <p>Use this form to test your API endpoints:</p>
                
                <select id="endpoint">
                    <option value="/validate-phone">Validate Phone</option>
                    <option value="/validate-city">Validate City</option>
                    <option value="/validate-date">Validate Date</option>
                    <option value="/collect-name">Collect Name</option>
                    <option value="/create-booking">Create Booking</option>
                    <option value="/update-booking">Update Booking</option>
                    <option value="/cancel-booking">Cancel Booking</option>
                </select>
                
                <div>
                    <p>JSON Data:</p>
                    <textarea id="jsonData" rows="5" cols="50" placeholder='{"key": "value"}'></textarea>
                </div>
                
                <button onclick="testEndpoint()">Test Endpoint</button>
                
                <div>
                    <p>Response:</p>
                    <div id="response"></div>
                </div>
            </div>
        </body>
    </html>
    """

# 1. Validate Phone Number Tool
@app.route('/validate-phone', methods=['POST', 'GET'])
def validate_phone():
    if request.method == 'GET':
        # Handle GET requests for browser testing
        return """
        <html>
            <head><title>Validate Phone</title></head>
            <body>
                <h1>Validate Phone</h1>
                <p>This endpoint requires a POST request with JSON data.</p>
                <p>Example JSON payload: <code>{"phone_number": "1234567890"}</code></p>
            </body>
        </html>
        """
    # Handle POST requests
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
    app.run(debug=True)