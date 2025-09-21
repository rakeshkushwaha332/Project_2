from flask import Flask, request, jsonify, render_template_string
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"

# Ensure data.json exists
def init_data_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)

# Load data from JSON
def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Save data to JSON
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/")
def home():
    # Simple HTML form
    html = """
    <!doctype html>
    <html>
    <head><title>Flask JSON Store</title></head>
    <body>
      <h2>Submit Data</h2>
      <form action="/submit" method="post">
        Name: <input type="text" name="name" required><br><br>
        Email: <input type="email" name="email" required><br><br>
        <button type="submit">Save</button>
      </form>

      <h2>Stored Data</h2>
      <ul>
        {% for entry in entries %}
          <li>{{ entry["name"] }} ({{ entry["email"] }})</li>
        {% endfor %}
      </ul>
    </body>
    </html>
    """
    entries = load_data()
    return render_template_string(html, entries=entries)

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")

    if not name or not email:
        return "Missing fields", 400

    data = load_data()
    data.append({"name": name, "email": email})
    save_data(data)

    return ("<p>Data saved! <a href='/'>&larr; Back</a></p>")

@app.route("/api/data")
def api_data():
    return jsonify(load_data())

if __name__ == "__main__":
    init_data_file()
    app.run(debug=True)
