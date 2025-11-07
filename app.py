from flask import Flask, request, jsonify
import json, os

app = Flask(__name__)

# File to store permanent variables
SAVE_FILE = "permanent_data.json"

# In-memory temp storage
temporary_data = {}

# Load permanent data if exists
if os.path.exists(SAVE_FILE):
    with open(SAVE_FILE, "r") as f:
        permanent_data = json.load(f)
else:
    permanent_data = {}

def save_permanent_data():
    """Save permanent variables to disk (max 100 MB)."""
    data_str = json.dumps(permanent_data)
    if len(data_str.encode("utf-8")) <= 100 * 1024 * 1024:  # 100 MB
        with open(SAVE_FILE, "w") as f:
            f.write(data_str)
    else:
        print("⚠️ Permanent data exceeds 100 MB, skipping save!")

@app.route("/")
def home():
    return "✅ Scratch Cloud Server Running!"

@app.route("/get", methods=["GET"])
def get_variable():
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "missing name"}), 400
    if name.startswith("_"):
        value = permanent_data.get(name)
    else:
        value = temporary_data.get(name)
    return jsonify({"name": name, "value": value})

@app.route("/set", methods=["POST"])
def set_variable():
    data = request.json
    name = data.get("name")
    value = data.get("value")

    if not name:
        return jsonify({"error": "missing name"}), 400

    if name.startswith("_"):
        permanent_data[name] = value
        save_permanent_data()
    else:
        temporary_data[name] = value

    return jsonify({"success": True, "name": name, "value": value})

@app.route("/list", methods=["GET"])
def list_variables():
    """For debugging — shows all current data."""
    return jsonify({
        "permanent": list(permanent_data.keys()),
        "temporary": list(temporary_data.keys())
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0")