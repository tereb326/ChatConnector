from local_openai.OpenaiClient import OpenAIConnector
import gradio as gr
import datetime

openai_client = OpenAIConnector()

messages = [
    {"role": "system", "content": "You are a helpful and kind AI Assistant"}
]

def chatbot_img(input_text):
    if input_text:
        messages.append({"role": "user", "content": input_text})
        reply = openai_client.create_image_with_gpt(input_text, True, datetime.datetime.now().strftime('%Y%m%d%H%M%S_img.png'))
        messages.append({"role": "assistant", "content": reply})

        return reply

def chatbot_text(input_text):
    if input_text:
        messages.append({"role": "user", "content": input_text})
        reply = openai_client.invoke_text_prompt(input_text)

        messages.append({"role": "assistant", "content": reply})
        return reply

# inputs = gr.Textbox(lines=7, label="Rozmawiaj z AI")
# outputs = gr.Textbox(label="Odpowiedź")
# gr.Interface(fn=chatbot_text, inputs=inputs, outputs=outputs, title="AI Chatbot", description="Zapytaj o co chcesz", theme="compact").launch(share=True)

with gr.Blocks() as demo:
    gr.Markdown("""
            # Wygeneruj interesującą Cię treść
        """)
    with gr.Tab("Informacje tekstowe"):
        with gr.Row():
            text_input = gr.Textbox(lines=7, label="Rozmawiaj z AI")
            text_output = gr.Textbox(label="Odpowiedź")
        text_button = gr.Button("Wyślij")
    with gr.Tab("Generator obrazów"):
        with gr.Row():
            desc_img_input = gr.Textbox(lines=7, label="Opisz interesujący Cię obraz")
            image_output = gr.Image()
        image_button = gr.Button("Wygeneruj obraz")

    text_button.click(chatbot_text, inputs=text_input, outputs=text_output)
    image_button.click(chatbot_img, inputs=desc_img_input, outputs=image_output)

demo.launch()