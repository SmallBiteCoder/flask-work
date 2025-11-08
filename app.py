from flask import Flask, request, jsonify
from flask_cors import CORS
import json, os

app = Flask(__name__)
CORS(app)  # allow access from Scratch / web

SAVE_FILE = "shared_data.json"

# Load saved shared data
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r") as f:
        try:
            shared_data = json.load(f)
        except:
            shared_data = {}
else:
    shared_data = {}

# 🔵 GET: return all shared variables
@app.route('/list', methods=['GET'])
def get_shared_data():
    return jsonify(shared_data)

# 🟢 POST: update or add a variable
@app.route('/update', methods=['POST'])
def update_shared_data():
    try:
        data = request.get_json(force=True)
        for key, value in data.items():
            shared_data[key] = value  # add or update variable

        # save to file
        with open(SAVE_FILE, "w") as f:
            json.dump(shared_data, f, indent=2)

        return jsonify({"message": "Updated", "data": shared_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return "✅ Shared Variable Server Running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)