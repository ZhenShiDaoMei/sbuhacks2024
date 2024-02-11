from openai import OpenAI
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

#global variables
count = 2
tempString = ""
words = []
mystery_blurb = ""
correct_guess = "Nice guess that was the missing word keep going!\n"
no_no_word = ""

#method finds all the words that gpt removed, and puts underscores as placeholders
def replace_first_occurrence_with_underscores(input_string, words_list):
    output_string = input_string[0]
    substring = input_string[1:]
    
    for word in words_list:
        start_index = substring.find(word)
        if start_index != -1:  # Word found
            before_word = substring[:start_index]
            after_word = substring[start_index + len(word):]
            substring = before_word + '_' * len(word) + after_word

    output_string += substring
    return output_string

#Finds underscore that corresponds to word
def replace_first_underscore_sequence(input_string, first_word):
    word_length = len(first_word)
    output_string = input_string[0]
    substring = input_string[1:] 
    underscore_sequence = '_' * word_length
    start_index = substring.find(underscore_sequence) 
    if start_index != -1:
        before_sequence = substring[:start_index]
        after_sequence = substring[start_index + word_length:]
        substring = before_sequence + first_word + after_sequence

    output_string += substring
    return output_string

# Load your API key from an environment variable or other secure location
client = OpenAI(
    api_key = "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"
)

@app.route('/generate-text', methods=['POST'])
def generateChatGPT():
    global mystery_blurb
    global count
    global tempString
    global words
    global correct_guess
    global no_no_word
    data = request.get_json()
    if count == 0:
        if data['prompt'] == words[0]:
            mystery_blurb = replace_first_underscore_sequence(mystery_blurb, words[0])
            if len(words) == 1:
                count = 2
                tempString = ""
                words = []
                no_no_word = ""
                return mystery_blurb + "\n\nCongratulations you solved the the braindrAIn!, to keep on playing type a new topic."
            words = words[1:]
            return mystery_blurb + "\n\n" + correct_guess
        try:
            messages = [{"role": "system", "content": ""}]
            messages.append({"role": "user", "content": "Give a hint that would help someone guess the the word: " + words[0]})
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages = messages,
                top_p=1,
                temperature=0.9,
                max_tokens=150
            )
            chat_reply = response.choices[0].message.content
            chat_reply = {"message": mystery_blurb + "\n\nWrong, Hint:" + chat_reply}
            return jsonify(chat_reply)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    if count == 1:
        count = 0
        try:
            messages = [{"role": "system", "content": "Previously you created this blurb: " + tempString + "(With this blurb we will play a game, listen to the rules carefully)"}]
            messages.append({"role": "user", "content": "Remove 7 key words from the blurb and add them to a list (It can't be: " + no_no_word + "). Return the list such that its in the following format: List: word1, word2, word3, ..."})
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages = messages,
                top_p=1,
                temperature=0.9,
                max_tokens=150
            )
            chat_reply = response.choices[0].message.content
            words = chat_reply.replace("List: ", "").split(", ")
            mystery_blurb = replace_first_occurrence_with_underscores(tempString, words)
            chat_reply = {"message": mystery_blurb}
            return jsonify(chat_reply)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    if count == 2:
        count = 1
        if 'prompt' not in data:
            return jsonify({"error": "No content provided"}), 400
        try:
            messages = [{"role": "system", "content": "You are a chatbot that will soon be given a topic to discuss. Provide a blurb that's  400 characters that contains some facts and random details."}]
            messages.append({"role": "user", "content": data['prompt']})
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages = messages,
                top_p=1,
                temperature=0.9,
                max_tokens=150
            )
            no_no_word = data['prompt']
            chat_reply = response.choices[0].message.content
            tempString = chat_reply
            chat_reply = {"message": chat_reply}
            return jsonify(chat_reply)
        except Exception as e:
            return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # It's not safe to deploy a Flask app in debug mode or without SSL in production.
    # You should use a WSGI server like gunicorn and serve over HTTPS.
    app.run(host='0.0.0.0', port=5000)
