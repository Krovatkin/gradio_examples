import openai_async
import asyncio

key = "API KEY"
import gradio as gr


# Don't forget to change the key
# This example uses `demo.launch(server_name="0.0.0.0")` to launch the app
# This example also uses openai_async for better performance
# The commented parts (prints) can be used to verify that async doesn't block
# loop isn't necessary

history = ""
async def hello(message):
    response = await openai_async.complete(
        key,
        timeout=2,
        payload={
            "model": "text-davinci-003" # gpt-3.5-turbo-0613,
            "prompt": f"{message} . Use markdown to style your answer please",
            "temperature": 0.7,
        },
    )
    global history
    history += "\n\n" + response.json()["choices"][0]['text']
    return history 
    # print(f"before {id(message)}")
    # await asyncio.sleep(5)
    # print(f"after {id(message)}")
    # return "Bla bla!"

# # Create event loop
# loop = asyncio.get_event_loop()

# # Run the loop until all the tasks are finished
# loop.run_until_complete(task)

# # Close the loop
# loop.close()


#demo = gr.Interface(fn=hello, inputs="text", outputs="text")

with gr.Blocks() as demo:
    with gr.Row():
        gr.HTML("<h1>Chatbot!</h1>")
    with gr.Row():
        mk = gr.Markdown()
    with gr.Row():
        text2 = gr.Textbox(lines=2, placeholder="Name Here...")
    with gr.Row():
        greet_btn = gr.Button("Greet")
        greet_btn.click(fn=hello, inputs=text2, outputs=mk, api_name="Submit")

demo.launch(server_name="0.0.0.0")


