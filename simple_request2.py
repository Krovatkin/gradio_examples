import openai_async
import asyncio

key = "API KEY"
import gradio as gr

# Don't forget to change the key
# This example uses `demo.launch(server_name="0.0.0.0")` to launch the app
# This example also uses openai_async for better performance
# More on maximum perf is here https://www.gradio.app/guides/setting-up-a-demo-for-maximum-performance
# gr.Chatbot component is used as both an input and output
# This is the copy of the demo (https://www.gradio.app/guides/interface-state) where user and bot are separate functions

async def user(message, history):
    return "", history + [[message, None]]

async def bot(history):
    user_message = history[-1][0]

    response = await openai_async.complete(
        key,
        timeout=2,
        payload={
            "model": "text-davinci-003", # gpt-3.5-turbo-0613,
            "prompt": f"{user_message} . Use markdown to style your answer please",
            "temperature": 0.7,
        },
    )

    answer = response.json()["choices"][0]['text']
    history[-1] = (user_message, answer)
    return history


with gr.Blocks() as demo:
    with gr.Row():
        gr.HTML("<h1>Chatbot!</h1>")
    with gr.Row():
        #mk = gr.Markdown()
        chatbot = gr.Chatbot()
    with gr.Row():
        text2 = gr.Textbox(lines=2, placeholder="Name Here...")
        text2.submit(user, [text2, chatbot], [text2, chatbot], queue=False).then(
            bot, chatbot, chatbot
        )
    with gr.Row():




        clear = gr.Button("Clear")
        clear.click(lambda: None, None, chatbot, queue=False)
demo.launch(server_name="0.0.0.0")
