from flask import Flask, request, jsonify
import sqlite3
import time

app = Flask(__name__)

# Helper function to interact with SQLite database
def execute_db(query, params=(), fetch=False):
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return result

# ------------------------- INVENTORY ENDPOINTS -------------------------

# 1️⃣ Add an Item to Inventory
@app.route('/add-item', methods=['POST'])
def add_item():
    data = request.json
    name = data.get("name")
    quantity = data.get("quantity", 1)

    if not name:
        return jsonify({"error": "Item name is required"}), 400

    try:
        execute_db("INSERT INTO inventory (name, quantity) VALUES (?, ?)", (name, quantity))
        time.sleep(10)  # Delay (as required)
        return jsonify({"message": f"Added {quantity}x {name} to inventory"}), 200
    except sqlite3.IntegrityError:
        return jsonify({"error": "Item already exists"}), 400

# 2️⃣ Remove an Item from Inventory
@app.route('/remove-item', methods=['POST'])
def remove_item():
    data = request.json
    name = data.get("name")

    if not name:
        return jsonify({"error": "Item name is required"}), 400

    execute_db("DELETE FROM inventory WHERE name=?", (name,))
    time.sleep(10)
    return jsonify({"message": f"Removed {name} from inventory"}), 200

# 3️⃣ Update Item Quantity in Inventory
@app.route('/update-quantity', methods=['POST'])
def update_quantity():
    data = request.json
    name = data.get("name")
    quantity = data.get("quantity")

    if not name or quantity is None:
        return jsonify({"error": "Item name and new quantity are required"}), 400

    execute_db("UPDATE inventory SET quantity=? WHERE name=?", (quantity, name))
    time.sleep(10)
    return jsonify({"message": f"Updated {name} quantity to {quantity}"}), 200

# ------------------------- START FLASK SERVER -------------------------
if __name__ == '__main__':
    app.run(debug=True)
