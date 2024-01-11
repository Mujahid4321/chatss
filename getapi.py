from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import spacy
from urllib.parse import quote_plus

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_USER'] = 'postgres'
app.config['SQLALCHEMY_DATABASE_PASSWORD'] = 'Sunplus@123'
app.config['SQLALCHEMY_DATABASE_HOST'] = '203.92.59.154'
app.config['SQLALCHEMY_DATABASE_PORT'] = '5482'
app.config['SQLALCHEMY_DATABASE_NAME'] = 'chikkuchatbot'
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{app.config['SQLALCHEMY_DATABASE_USER']}:{quote_plus(app.config['SQLALCHEMY_DATABASE_PASSWORD'])}@{app.config['SQLALCHEMY_DATABASE_HOST']}:{app.config['SQLALCHEMY_DATABASE_PORT']}/{app.config['SQLALCHEMY_DATABASE_NAME']}"
app.config['SECRET_KEY'] = 'your_secret_key'  # Add a secret key for session management
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Define your Intent model using SQLAlchemy with the specified schema
class Intent(db.Model):
    __tablename__ = 'chatbot_data'
    __table_args__ = {'schema': 'chikkuchatbot'}
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(50), unique=True, nullable=False)
    patterns = db.Column(db.ARRAY(db.Text), nullable=False)
    responses = db.Column(db.ARRAY(db.Text), nullable=False)

# API endpoint for getting intents
@app.route('/api/intents', methods=['GET'])
def get_intents():
    with app.app_context():
        intents = Intent.query.all()
        intent_list = []
        for intent in intents:
            intent_list.append({
                'id': intent.id,
                'tag': intent.tag,
                'patterns': intent.patterns,
                'responses': intent.responses
            })

        return jsonify({'intents': intent_list})

if __name__ == '__main__':
    # Create database tables if not exists
    with app.app_context():
        db.create_all()
    # Run the Flask application
    app.run(debug=True, port=1212)
