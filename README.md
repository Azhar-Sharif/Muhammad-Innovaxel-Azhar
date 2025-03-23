# Innovaxel URL Shortener  

A RESTful API for shortening URLs, retrieving original URLs, updating, deleting, and tracking access statistics.  

## Table of Contents  
- [Overview](#overview)  
- [Features](#features)  
- [Tech Stack](#tech-stack)  
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Sample Response Format](#sample-response-format)

## Overview  
This project is a URL Shortening Service that allows users to:  

- Create a short URL for a given long URL.  
- Retrieve the original URL from the short version.  
- Update or delete an existing short URL.  
- Track the number of times a short URL has been accessed.  

## Features  
- ✔️ RESTful API with CRUD operations  
- ✔️ Unique short code generation  
- ✔️ URL redirection feature  
- ✔️ URL statistics tracking  
- ✔️ Error handling for invalid requests  
 

## Tech Stack  
- **Backend:** Python (Flask)  
- **Database:** SQLite   
- **Tools:** Git, Vs Code 


## Installation  

Follow these steps to set up the project on your local machine:  

1. **Clone the repository**  
   ```git clone https://github.com/Azhar-Sharif/Muhammad-innovaxel-Azhar.git ```
2.  **Move to Directory**
   ```cd Muhammad-innovaxel-Azhar```
3.  **Install Dependencies**  
   ```pip install -r requirements.txt```
4.  **Run Application**
    ```python app.py```

## API Endpoints

### Create Shortened URL
- **POST** `/shorten`
- Body: `{"url": "https://example.com"}`
- Response: Returns shortened URL details

### Retrieve Original URL
- **GET** `/shorten/<short_code>`
- Response: Returns original URL and stats

### Visit Original Website
- **GET** `/<short_code>`
- Response: Redirects to original URL

### Update URL
- **PUT** `/shorten/<short_code>`
- Body: `{"url": "https://new-example.com"}`
- Response: Returns updated URL details

### Delete URL
- **DELETE** `/shorten/<short_code>`
- Response: Confirmation message

### Get URL Statistics
- **GET** `/shorten/<short_code>/stats`
- Response: Returns URL access statistics
