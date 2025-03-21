from flask import Flask

@app.route("/")
def home():
    return "Innovaxel URL Shortening"

if __name__ == "__main__":
    app.run(debug=True)