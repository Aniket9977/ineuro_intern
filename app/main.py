import os
import logging
from flask import Flask, request, jsonify, render_template_string
from app.audio_processing import convert_audio_to_text
import mysql.connector
from mysql.connector import Error

# Setting up logging
logging.basicConfig(filename='logs/virtual_notes.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

# Initialize Flask App
app = Flask(__name__)

# Function to connect to MySQL
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='virtual_notes',
            user='root',  # Replace with your MySQL username
            password='12345'  # Replace with your MySQL password
        )
        if connection.is_connected():
            logging.info("Successfully connected to MySQL database")
        return connection
    except Error as e:
        logging.error(f"Error while connecting to MySQL: {str(e)}")
        return None

# Home Page Route
@app.route('/')
def home():
    home_page_html = '''
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Virtual Notes Assistant</title>
    </head>
    <body>
        <h1>Welcome to the Virtual Notes Assistant</h1>
        <p>This API allows you to convert audio files into text.</p>
        <p>To use the API:</p>
        <ul>
            <li>Send a POST request to <strong>/convert</strong> with an audio file attached.</li>
        </ul>
        <p>The converted text will be saved to our MySQL database.</p>
        <p>Note: Ensure you send the audio file with the key name <strong>audio</strong>.</p>
    </body>
    </html>
    '''
    return render_template_string(home_page_html)

# API Endpoint to upload audio and convert to text
@app.route('/convert', methods=['POST'])
def convert():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio = request.files['audio']
    audio_file_path = os.path.join('uploads', audio.filename)
    audio.save(audio_file_path)

    text = convert_audio_to_text(audio_file_path)

    if text:
        # Insert text into MySQL database
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                insert_query = "INSERT INTO notes (text) VALUES (%s)"
                cursor.execute(insert_query, (text,))
                connection.commit()
                cursor.close()
                connection.close()
                logging.info("Text successfully saved to MySQL database")
                return jsonify({'text': text}), 200
            except Error as e:
                logging.error(f"Error while inserting into MySQL: {str(e)}")
                return jsonify({'error': 'Database insertion failed'}), 500
        else:
            return jsonify({'error': 'Database connection failed'}), 500
    else:
        return jsonify({'error': 'Conversion failed'}), 500

if __name__ == '__main__':
    # Make sure uploads directory exists
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
