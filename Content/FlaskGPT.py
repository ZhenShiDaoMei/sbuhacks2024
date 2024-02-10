from openai import OpenAI
from flask import Flask, request, jsonify

app = Flask(__name__)

client = OpenAI(
    api_key = "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"
)

@app.route('/generate-text', methods=['POST'])

def generateChatGPT():
    data = request.json
    
    if 'content' not in data:
        return jsonify({"error": "No content provided"}), 400
    try:
        response = client.chat.completions.create(
            model ="gpt-3.5-turbo",
            messages = [{"role": "user", "content": data}],
            top_p=1,
            temperature=0.9,
            max_tokens=150
        )    
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)