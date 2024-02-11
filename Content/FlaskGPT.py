from openai import OpenAI
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Load your API key from an environment variable or other secure location
client = OpenAI(
    api_key = "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"
)

@app.route('/generate-text', methods=['POST'])
def generateChatGPT():
    data = request.get_json()
    # print(data)
    # print(data['prompt'])
    # print(data.get('prompt'))
    
    if 'prompt' not in data:
        return jsonify({"error": "No content provided"}), 400
    
    try:
        messages = [{"role": "system", "content": ""}]
        messages.append({"role": "user", "content": data['prompt']})
        print(messages)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages = messages,
            top_p=1,
            temperature=0.9,
            max_tokens=150
        )
        chat_reply = response.choices[0].message.content
        chat_reply = {"message": chat_reply}
        # print(chat_reply)
        # print("-----------")
        # print(jsonify(chat_reply))
        return jsonify(chat_reply)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # It's not safe to deploy a Flask app in debug mode or without SSL in production.
    # You should use a WSGI server like gunicorn and serve over HTTPS.
    app.run(host='0.0.0.0', port=5000)
