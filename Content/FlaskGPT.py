from openai import OpenAI
from flask import Flask, request, jsonify

app = Flask(__name__)

client = OpenAI(
    api_key = "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"
)

@app.route('/generate-text', methods=['POST'])

def generateChatGPT():
    data = request.json
    response = client.chat.completions.create(
        model ="gpt-3.5-turbo",
        messages = [{"role": "user", "content": data}],
        top_p=1,
        temperature=0.9,
        max_tokens=150
    )

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)