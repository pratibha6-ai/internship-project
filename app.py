
from flask import Flask, request, jsonify
from model import CodeGeneratorApp# Assuming main is the function to process the input
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
main=CodeGeneratorApp()  # Initialize the main function from model.py

# Example chatbot response (can be replaced with AI/ML logic)


@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        return "Use POST with JSON: {\"message\": \"your message\"}"
    
    data = request.get_json()
    user_message = data.get('message', '')
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    bot_reply = main.process_query(user_message)
    return jsonify({"reply": bot_reply})



if __name__ == "__main__":
    app.run(debug=True)
