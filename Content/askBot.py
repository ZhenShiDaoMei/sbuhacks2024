from openai import OpenAI
import gradio

count = 2
tempString = ""
actual_input = ""
words = []
mystery_blurb = ""
correct_guess = "Nice guess that was the missing word keep going!\n"
no_no_word = ""

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

client = OpenAI(
    api_key = "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"
)

messages = [{"role": "system", "content": ""}] #change content to whatever we want

def CustomChatGPT(user_input):
    global mystery_blurb
    global count
    global tempString
    global words
    global correct_guess
    global no_no_word
    if count == 0:  
        if actual_input == words[0]:
            mystery_blurb = replace_first_underscore_sequence(mystery_blurb, words[0])
            if len(words)== 1:
                count = 2
                tempString = ""
                words = []
                no_no_word = ""
                return mystery_blurb + "\nCongratulations you solved the the braindrAIn!, to keep on playing type a new topic."
            words = words[1:]
            return mystery_blurb + "\n" + correct_guess
        else:
            messages = [{"role": "system", "content": ""}]
            messages.append({"role": "user", "content": "Give a hint that would help someone guess the the word: " + words[0]})
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages = messages,
                top_p=1,
                temperature=0.9,
                max_tokens=150
            )
            chatGPT_reply = response.choices[0].message.content
            return mystery_blurb + "\nWrong, Hint:" + chatGPT_reply 
        
    if count == 1:
        count = 0
        messages = [{"role": "system", "content": "Previously you created this blurb: " + tempString + "(With this blurb we will play a game, listen to the rules carefully)"}]
        messages.append({"role": "user", "content": "Remove 7 key words from the blurb and add them to a list (It can't be: " + no_no_word + "). Return the list such that its in the following format: List: word1, word2, word3, ..."})
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages = messages,
            top_p=1,
            temperature=0.9,
            max_tokens=150
        )
        chatGPT_reply = response.choices[0].message.content
        words = chatGPT_reply.replace("List: ", "").split(", ")
        mystery_blurb = replace_first_occurrence_with_underscores(tempString, words)
        return mystery_blurb + "\n" + chatGPT_reply + words[0] + words[1]+words[2]+words[3]+words[4]
    
    if count == 2:
        mystery_blurb = ""
        count = 1
        message = [{"role": "system", "content": "You are a chatbot that will soon be given a topic to discuss. Provide a blurb that's  400 characters that contains some facts and random details."}]
        message.append({"role": "user", "content": user_input})
        response = client.chat.completions.create(
            model ="gpt-3.5-turbo",
            messages = message,
            top_p=1,
            temperature=0.9,
            max_tokens=150
        )
        no_no_word = user_input
        chatGPT_reply = response.choices[0].message.content
        tempString = chatGPT_reply
        return chatGPT_reply

def chatgpt_clone(input,history):
    global actual_input 
    actual_input = input
    history = history or []
    s = list(sum(history, ()))
    s.append(input)
    inp = ' '.join(s)
    output = CustomChatGPT(inp)
    history.append((input, output))
    return history, history

with gradio.Blocks() as demo:
    chatbot = gradio.Chatbot()
    msg = gradio.Textbox(placeholder="prompt")
    state = gradio.State() 
    clear = gradio.ClearButton(msg)
    btn = gradio.Button("Submit")
    btn.click(fn=chatgpt_clone, inputs= [msg, state], outputs= [chatbot, state])

demo.launch()
