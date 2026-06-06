from flask import Flask
from routes import main_bp
from database import init_db

# Initialize the Flask application
app = Flask(__name__)

# Security configuration for flashing messages
app.secret_key = 'oose_mini_project_secret'

# Register the routes blueprint (Controller Layer)
app.register_blueprint(main_bp)

if __name__ == '__main__':
    # Step 1: Initialize the database schema (Model Layer)
    init_db() 
    
    # Step 2: Start the Application Server
    # Running on http://127.0.0.1:5000 as per deployment notes
    app.run(debug=True, port=5000)