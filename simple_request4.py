import openai_async
import asyncio


from fastapi import FastAPI
import gradio as gr

# Don't forget to change the key
# This example uses FastAPI to embed Gradio api with `mount_gradio_app`
# This example also uses openai_async for better performance
# gr.Chatbot component is used as both an input and output
# The state is maintained via `history` more at https://www.gradio.app/guides/interface-state
# This app can be run with `uvicorn` like this: `uvicorn simple_request4:app --host 0.0.0.0` 
CUSTOM_PATH = "/gradio"

app = FastAPI()

@app.get("/")
def read_main():
    return {"message": "This is your main app"}


key = "API_KEY"


async def bot(message, history):

    response = await openai_async.complete(
        key,
        timeout=2,
        payload={
            "model": "text-davinci-003", # gpt-3.5-turbo-0613,
            "prompt": f"{message} . Use markdown to style your answer please",
            "temperature": 0.7,
        },
    )

    answer = response.json()["choices"][0]['text']
    history.append((message, answer))
    return "", history


with gr.Blocks() as demo:
    with gr.Row():
        gr.HTML("<h1>Chatbot!</h1>")
    with gr.Row():
        #mk = gr.Markdown()
        chatbot = gr.Chatbot()
    with gr.Row():
        text2 = gr.Textbox(lines=2, placeholder="Name Here...")
        text2.submit(bot, [text2, chatbot], [text2, chatbot], queue=False)
    with gr.Row():
        # greet_btn = gr.Button("Submit")
        # greet_btn.click(fn=hello, inputs=text2, outputs=mk, api_name="Submit")



        clear = gr.Button("Clear")
        clear.click(lambda: None, None, chatbot, queue=False)

app = gr.mount_gradio_app(app, demo, path=CUSTOM_PATH)

# <gradio-app src="http://127.0.0.1:7680/app1/"></gradio-app>
