from flask import Flask, request, jsonify

app = Flask(__name__)

# Example chatbot response (can be replaced with AI/ML logic)
def chatbot_response(user_message):
    if "hello" in user_message.lower():
        return "Hi there! How can I help you today?"
    elif "bye" in user_message.lower():
        return "Goodbye! Have a great day."
    else:
        return "I can't understand"

@app.route('/chat', methods=['POST'])
def chat():
    # Get raw text from request body
    user_message = request.data.decode("utf-8")

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    # Process message
    bot_reply = chatbot_response(user_message)

    # Send back bot response
    return jsonify({"reply": bot_reply})

if __name__ == '__main__':
    app.run(debug=True)