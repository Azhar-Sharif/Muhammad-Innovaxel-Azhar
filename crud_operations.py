import sqlite3
from datetime import datetime
from flask import jsonify
from service import generate_short_code


# function to create a short URL and store it in the database
def create_short_url(url):
        original_url = url
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
            })

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
        })



# Function to retrieve the original URL information from the database
def retrieve_original_url_info(short_code):
    try:
        conn = sqlite3.connect("urls.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, url, short_code, created_at, updated_at, access_count FROM short_urls WHERE short_code = ?", (short_code,))
        result = cursor.fetchone()
        conn.close()
        
        return result
    except sqlite3.Error:
        if conn:
            conn.close()
        return None

# Function to update the original URL information in the database
def update_original_url_info(short_code,new_url):
    new_url = new_url
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    # Check if the short URL exists
    cursor.execute("SELECT id FROM short_urls WHERE short_code = ?", (short_code,))
    result = cursor.fetchone()
    if not result:
        conn.close()
        return None
    
    # Update the original URL
    timestamp = datetime.utcnow().isoformat()
    cursor.execute("UPDATE short_urls SET url = ?, updated_at = ? WHERE short_code = ?", (new_url, timestamp, short_code))
    conn.commit()
    
    # Return updated short URL details
    cursor.execute("select * from short_urls where short_code = ?", (short_code,))
    result = cursor.fetchone()
    conn.close()
    return jsonify({
        "id": result[0],
        "url": result[1],
        "shortCode": result[2],
        "createdAt": result[3],
        "updatedAt": result[4],
        "accessCount": result[5]                         
    })


# Function to delete the original URL information from the database
def delete_original_url_info(short_code):
    try:
        conn = sqlite3.connect("urls.db")
        cursor = conn.cursor()
        
        # First check if URL exists
        cursor.execute("SELECT id FROM short_urls WHERE short_code = ?", (short_code,))
        result = cursor.fetchone()
        if not result:
            conn.close()
            return None
            
        # Delete the record
        cursor.execute("DELETE FROM short_urls WHERE short_code = ?", (short_code,))
        conn.commit()
        
        # Verify deletion
        cursor.execute("SELECT id FROM short_urls WHERE short_code = ?", (short_code,))
        verification = cursor.fetchone()
        
        conn.close()
        
        # Return True only if the record is actually deleted
        return verification is None
        
    except sqlite3.Error as e:
        if conn:
            conn.close()
        return None


# Function to retrieve the URL statistics from the database
def get_url_stats_from_db(short_code):
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM short_urls WHERE short_code = ?", (short_code,))
    result = cursor.fetchone()
    

    if not result:
        conn.close()
        return None

    return jsonify({
        "id": result[0],
        "url": result[1],
        "shortCode": result[2],
        "createdAt": result[3],
        "updatedAt": result[4],
        "accessCount": result[5]
    })

# Function to increment the access count of a short URL
def retrieve_url_for_redirect(short_code):
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()
    cursor.execute("SELECT url FROM short_urls WHERE short_code = ?", (short_code,))
    result = cursor.fetchone()
    if not result:
        conn.close()
        return None
    cursor.execute("UPDATE short_urls SET access_count = access_count + 1 WHERE short_code = ?", (short_code,))
    conn.commit()
    conn.close()  # Ensure the connection is closed after committing
    return result[0]  # Return the original URL