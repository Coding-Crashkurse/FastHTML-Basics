from fasthtml.common import Div, H1, P, Button, Script, Link


def with_card(color="blue", border_color="blue", padding="4"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            content = func(*args, **kwargs)
            tailwind_classes = f"p-{padding} rounded-lg shadow-lg bg-{color}-100 border border-{border_color}-500"
            return Div(
                Div(
                    content,
                    cls=tailwind_classes,
                ),
                cls="card border shadow-lg rounded-lg m-4",
            )

        return wrapper

    return decorator


def Header(title):
    return Div(H1(title, cls="text-2xl font-bold mb-4"), cls="header")


def Body(content):
    return Div(P(content, cls="text-lg"), cls="body mb-4")


def Footer(info):
    return Div(P(info, cls="text-sm text-gray-600"), cls="footer")


def Page(title, content, footer_info):
    return Div(
        Header(title),
        Body(content),
        Footer(footer_info),
        cls="page p-6 max-w-xl mx-auto bg-white shadow-lg rounded-lg",
    )


def ConditionalCard(content, show_card=True):
    if show_card:
        return Div(content, cls="conditional-card p-4 bg-blue-100 rounded-lg shadow-md")
    return Div(
        "Card is hidden", cls="no-card text-red-600 p-4 bg-red-100 rounded-lg shadow-md"
    )


class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1
        return self.render()

    def render(self):
        return Div(
            P(f"Current count: {self.count}", cls="text-lg font-semibold"),
            Button(
                "Increment",
                hx_post="/increment",
                hx_target="#counter-div",
                hx_swap="outerHTML",
                cls="btn btn-primary mt-2",
            ),
            id="counter-div",
            cls="counter p-4 bg-gray-100 rounded-lg shadow-lg",
        )


def Template(content, title="Default Title"):
    return Div(
        H1(title, cls="text-3xl font-bold mb-4"),
        Div(content, cls="template-body p-4 bg-gray-50 rounded-lg shadow-sm"),
        cls="template p-6 max-w-xl mx-auto bg-white shadow-lg rounded-lg",
    )


def create_alert(alert_type="info"):
    alert_classes = {
        "info": "bg-blue-100 text-blue-700 border-blue-200",
        "warning": "bg-yellow-100 text-yellow-700 border-yellow-200",
        "danger": "bg-red-100 text-red-700 border-red-200",
    }

    def alert(content):
        alert_class = alert_classes.get(
            alert_type, "bg-gray-100 text-gray-700 border-gray-200"
        )
        return Div(content, cls=f"alert p-4 rounded-lg shadow-md border {alert_class}")

    return alert
