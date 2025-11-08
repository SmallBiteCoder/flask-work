from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow access from Scratch, browser, etc.

# 🧠 Shared variable dictionary (RAM only)
shared_data = {}

# 🟢 POST → Add or update variables
@app.route('/update', methods=['POST'])
def update_data():
    try:
        data = request.get_json(force=True)
        if not isinstance(data, dict):
            return jsonify({"error": "Invalid JSON format"}), 400

        # Update shared variables
        for key, value in data.items():
            shared_data[key] = value

        return jsonify({"message": "Updated", "data": shared_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 🔵 GET → Get all shared variables
@app.route('/list', methods=['GET'])
def list_data():
    return jsonify(shared_data)


# 🟣 GET (specific variable) → /get/<varname>
@app.route('/get/<varname>', methods=['GET'])
def get_variable(varname):
    if varname in shared_data:
        return jsonify({varname: shared_data[varname]})
    else:
        return jsonify({"error": f"'{varname}' not found"}), 404


@app.route('/')
def home():
    return "✅ Shared Variable Server Running (No Disk Save)"


if __name__ == '__main__':
    app.run(host='0.0.0.0')