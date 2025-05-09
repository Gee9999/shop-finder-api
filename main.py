from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '✅ Shop Finder API is live. Try /search?category=beads'

@app.route('/search')
def search():
    category = request.args.get('category')
    
    if not category:
        return jsonify({'error': 'Missing category parameter'}), 400

    # Dummy data
    data = [
        {"name": "Fashion World", "email": "contact@fashionworld.co.za", "location": "Cape Town"},
        {"name": "Style Hub", "email": "info@stylehub.co.za", "location": "Johannesburg"},
        {"name": "Bead Bazaar", "email": "beads@bazaar.co.za", "location": "Durban"}
    ]

    for item in data:
        item['category'] = category

    return jsonify(data)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
