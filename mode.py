from flask import Flask
from flask_cors import CORS
from models import init_db
from routes.auth import auth_bp  
from routes.appointments import appointments_bp  # 1. Added missing import

app = Flask(__name__)
CORS(app)

# Run the initialization step to build your database tables
init_db()

# Plug in the routing modules directly into the app core
app.register_blueprint(auth_bp)
app.register_blueprint(appointments_bp)  # 2. Added missing registration

if __name__ == '__main__':
    app.run(debug=True, port=5000)
