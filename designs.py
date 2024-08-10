from fasthtml.common import *
from components import (
    with_card,
    Page,
    ConditionalCard,
    Counter,
    Template,
    create_alert,
)
import random

tlink = Script(src="https://unpkg.com/tailwindcss-cdn@3.4.3/tailwindcss.js")
dlink = Link(
    rel="stylesheet",
    href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css",
)
app, rt = fast_app(hdrs=(tlink, dlink), ws_hdr=True)


@with_card(color="lightblue", border_color="blue", padding="10")
def get_card():
    return Div(H1("Hello, World"), P("Some text"), P("Some more text"))


@rt("/card")
def get():
    return get_card()


@rt("/composition")
def get():
    return Page(
        title="Welcome Page",
        content="This is the body content.",
        footer_info="Footer Information",
    )


def get_conditional(show):
    return Div(
        ConditionalCard("This is a card", show_card=show),
        Button(
            "Generate Value",
            hx_post="/toggle-card",
            hx_target="#conditional-container",
            hx_swap="outerHTML",
            cls="btn btn-primary mt-4",
        ),
        id="conditional-container",
        cls="p-4 bg-gray-100 rounded-lg shadow-lg",
    )


@rt("/conditional")
def get():
    return get_conditional(show=False)


@rt("/toggle-card", methods=["post"])
def get():
    random_value = random.random()
    show = random_value > 0.5
    return get_conditional(show)


counter = Counter()


@rt("/counter")
def get():
    return counter.render()


@rt("/increment", methods=["post"])
def post_increment():
    return counter.increment()


@rt("/template")
def get():
    content = P("This is the dynamic content passed into the template.")
    return Template(content, title="Custom Title")


@rt("/alerts")
def get():
    InfoAlert = create_alert("info")
    WarningAlert = create_alert("warning")
    ErrorAlert = create_alert("danger")

    return Div(
        InfoAlert("This is an informational alert."),
        WarningAlert("This is a warning alert."),
        ErrorAlert("This is an error alert."),
        cls="space-y-4",
    )


serve()
