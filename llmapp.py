from dotenv import load_dotenv
from fasthtml.common import *
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI

load_dotenv()

app, rt = fast_app()

messages = []

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, streaming=True)

headers = [
    Script(src="https://cdn.tailwindcss.com"),
    Link(
        rel="stylesheet",
        href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css",
    ),
    Link(rel="icon", href="pirate.png", type="image/png"),
    Script(src="https://unpkg.com/htmx.org@1.6.1/dist/htmx.min.js"),
]


def ChatMessage(msg):
    bubble_class = (
        "chat-bubble-primary"
        if isinstance(msg, HumanMessage)
        else "chat-bubble-secondary"
    )
    align_class = "chat-end" if isinstance(msg, HumanMessage) else "chat-start"
    return Div(
        Div(
            Div(msg.content, cls=f"chat-bubble {bubble_class}"),
            cls=f"chat {align_class}",
        ),
        cls="mb-2",
    )


@rt("/")
def get():
    chat_form = Form(
        Input(
            type="text",
            name="user_input",
            placeholder="Enter yer message...",
            cls="input w-full",
        ),
        Button("Send", cls="btn btn-primary w-full mt-2"),
        method="post",
        action="/chat",
        hx_post="/chat",
        hx_target="#chat-history-container",
        hx_swap="innerHTML",
        cls="mt-4",
    )

    chat_history = Div(*[ChatMessage(msg) for msg in messages], id="chat-history")

    return Html(
        *headers,
        H1("Chat with Pirate Bob", cls="text-2xl"),
        Div(
            Img(src="pirate.png", cls="w-16 h-16 mx-auto"),
            cls="flex justify-center mt-4",
        ),
        Div(chat_form, cls="w-full max-w-lg mx-auto"),
        Div(
            chat_history,
            id="chat-history-container",
            cls="mt-4 w-full max-w-lg mx-auto bg-white p-4 shadow-md rounded-lg overflow-y-auto",
        ),
    )


@rt("/chat", methods=["post"])
def chat(user_input: str):
    if user_input:
        messages.append(HumanMessage(content=user_input))

        response = llm.invoke(
            [SystemMessage(content="Respond like a pirate."), *messages]
        )

        messages.append(AIMessage(content=response.content))

    return Div(*[ChatMessage(msg) for msg in messages])


serve()
