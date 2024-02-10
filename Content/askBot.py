from openai import OpenAI
import gradio

client = OpenAI(
    api_key = "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"
)

css_path = './Content/askBot.css'
with open(css_path, 'r') as css_file:
    custom_css = css_file.read()

messages = [{"role": "system", "content": ""}] #change content to whatever we want

def CustomChatGPT(user_input):
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model ="gpt-3.5-turbo",
        messages = messages,
        top_p=1,
        temperature=0.9,
        max_tokens=150
    )
    chatGPT_reply = response.choices[0].message.content
    return chatGPT_reply

def chatgpt_clone(input,history):
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
    clear = gradio.ClearButton([msg, chatbot])
    btn = gradio.Button("Submit")
    btn.click(fn=chatgpt_clone, inputs= [msg, state], outputs= [chatbot, state])

demo.launch()