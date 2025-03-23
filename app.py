from flask import Flask, request, render_template, redirect, jsonify, url_for
from flask_cors import CORS
from service import generate_short_code
import sqlite3
from datetime import datetime
from create_database import create_table
from crud_operations import (
    create_short_url, 
    retrieve_original_url_info, 
    update_original_url_info, 
    delete_original_url_info, 
    get_url_stats_from_db, 
    retrieve_url_for_redirect as get_redirect_url
)

app = Flask(__name__)
CORS(app) 

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/<short_code>", methods=["GET"])
def retrieve_url_for_redirect(short_code):
    original_url = get_redirect_url(short_code)  # Use the renamed function
    if original_url:
        return redirect(original_url, code=302)  # Redirect to the original URL with a 302 status code
    return jsonify({"error": "Short URL not found"}), 404

@app.route("/redirect_to_url", methods=["POST"])
def redirect_to_url():
    short_code = request.form.get("redirect_short_code")
    if not short_code:
        return jsonify({"error": "Missing short code"}), 400
        
    # Use the existing redirect function
    original_url = get_redirect_url(short_code)
    if original_url:
        return redirect(original_url, code=302)
    return jsonify({"error": "Short URL not found"}), 404

""" Create Functions"""

# this is the endpoint to create a short URL
@app.route("/shorten", methods=["POST"])
def shorten_url():
    url = None
    
    if request.is_json:
        data = request.get_json()
        url = data.get("url")
    else:
        url = request.form.get("url")
        
    if not url:
        return jsonify({"error": "Missing 'url' in request"}), 400

    return create_short_url(url), 201

""" Retriving Functions"""

# this is the endpoint to retrieve the original URL from the short code    
@app.route("/shorten/<short_code>", methods=["GET"])
def retrieve_original_url(short_code):
    # Check if the short URL exists in request body
    if not short_code:
        return jsonify({"error": "Missing 'short_code' in request body"}), 400
    # Retrieve the original URL
    result = retrieve_original_url_info(short_code)
    if result:
        return jsonify({
            "id": result[0],
            "url": result[1],
            "shortCode": result[2],
            "createdAt": result[3],
            "updatedAt": result[4],
            "accessCount": result[5]
        }), 200
    return jsonify({"error": "Short URL not found in database"}), 404 

# This function retrieves the short code from the form and redirect to the retrieve_original_url function
@app.route("/retrieve_short_code_from_form", methods=["POST"])  # Fixed typo in URL
def retrieve_short_code_from_form():
    short_code = request.form.get("short_code_for_retrieve")
    if not short_code:
        return jsonify({"error": "Missing 'short_code' in request body"}), 400
    return redirect(url_for("retrieve_original_url", short_code=short_code))

""" Update Functions"""

# This is the endpoint to update the original URL information in the database
@app.route("/shorten/<short_code>", methods=["PUT"])
def update_original_url(short_code,new_url=None):
    if not new_url:
        data = request.get_json()
        if not data or "url" not in data:
            return jsonify({"error": "Missing 'url' in request body"}), 400
        new_url = data["url"]
    result =  update_original_url_info(short_code,new_url)
    if result:
        return result, 200
    return jsonify({"error": "Short URL not found in database"}), 404

# This function get the short code and new url from the form and redirect to the update_original_url function
@app.route("/update_url_by_form", methods=["POST"])
def update_url_by_form():
    short_code = request.form.get("short_code_for_update")
    new_url = request.form.get("new_url")
    if not short_code or not new_url:
        return jsonify({"error": "Missing 'short_code' or 'new_url' in request body"}), 400
    return redirect(url_for("update_original_url", short_code=short_code, new_url=new_url))


""" Delete Functions"""

# This function deletes the original URL information from the short code
@app.route("/shorten/<short_code>", methods=["DELETE"])
def delete_original_url(short_code):
    # Check if the short URL exists
    if not short_code:
        return jsonify({"error": "Missing 'short_code' in request   body"}), 400
    
    result = delete_original_url_info(short_code)
    if not result:
        return jsonify({"error": "Short URL not found in database"}), 404
    return jsonify({"message": "Short URL deleted successfully"}), 200



# This function retrieves the short code from the form and redirect to the delete_original_url function
@app.route("/delete_url_by_form", methods=["POST"])
def delete_url_by_form():
    short_code = request.form.get("short_code_for_delete")
    if not short_code:
        return jsonify({"error": "Missing 'short_code' in request body"}), 400
    
    return redirect(url_for("delete_original_url", short_code=short_code))

""" Stats Functions"""

# This is the endpoint to retrieve the URL statistics from the database
@app.route("/shorten/<short_code>/stats", methods=["GET"])
def get_url_stats(short_code):
    result =  get_url_stats_from_db(short_code)
    if result:
        return result, 200
    return jsonify({"error": "Short URL not found in database"}), 404
    
# This function retrieves the short code from the form and redirect to the get_url_stats function
@app.route("/get_url_stats_by_form", methods=["POST"])
def get_url_stats_by_form():
    short_code = request.form.get("short_code_for_stats")
    if not short_code:
        return jsonify({"error": "Missing 'short_code' in request body"}), 400
    return redirect(url_for("get_url_stats", short_code=short_code))



if  __name__ == "__main__":
    create_table()
    app.run(debug=True)

