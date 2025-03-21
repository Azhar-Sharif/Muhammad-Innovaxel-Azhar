from flask import Flask, request, render_template, redirect, jsonify
from service import generate_short_code
import sqlite3
from datetime import datetime
from create_database import create_table

app = Flask(__name__)

# Home Page 
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")  


# Shorten URL
@app.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()

    if not data or "url" not in data:
        return jsonify({"error": "Missing 'url' in request body"}), 400

    original_url = data["url"]
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()

    #  Check if the URL already exists
    cursor.execute("SELECT id, short_code, created_at, updated_at FROM short_urls WHERE url = ?", (original_url,))
    existing_entry = cursor.fetchone()

    if existing_entry:
        # Return existing short URL details
        conn.close()
        return jsonify({
            "id": existing_entry[0],
            "url": original_url,
            "shortCode": existing_entry[1],
            "createdAt": existing_entry[2],
            "updatedAt": existing_entry[3]
        }), 200  
    # Return 200 OK (URL already exists)

    #  If the URL does not exist, create a new short URL
    short_code = generate_short_code()
    timestamp = datetime.utcnow().isoformat()

    cursor.execute("INSERT INTO short_urls (url, short_code, created_at, updated_at) VALUES (?, ?, ?, ?)", 
                   (original_url, short_code, timestamp, timestamp))
    conn.commit()
    url_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "id": url_id,
        "url": original_url,
        "shortCode": short_code,
        "createdAt": timestamp,
        "updatedAt": timestamp
    }), 201  
# Return 201 Created


#  Retrieve Original URL information
@app.route("/shorten/<short_code>", methods=["GET"])
def get_original_url(short_code):
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    
    # Fetch full details of the short URL
    cursor.execute("SELECT id, url, short_code, created_at, updated_at FROM short_urls WHERE short_code = ?", (short_code,))
    result = cursor.fetchone()

    if result:
         # Increment access count
        cursor.execute("UPDATE short_urls SET access_count = access_count + 1 WHERE short_code = ?", (short_code,))
        conn.commit()
        conn.close()
        return jsonify({
            "id": result[0],
            "url": result[1],  
            "shortCode": result[2], 
            "createdAt": result[3],
            "updatedAt": result[4]
        }), 200
    else:
        return jsonify({"error": "Short URL not found"}), 404

if __name__ == "__main__":
    create_table()
    app.run(debug=True)

