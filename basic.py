from fasthtml.common import *

app = FastHTML()


def generate_html():
    return Div(H1("Hello, World"), P("Some text"), P("Some more text"))


@app.get("/")
def home():
    html_content = []
    for _ in range(5):
        html_content.append(generate_html())
    return Div(*html_content)


serve()
