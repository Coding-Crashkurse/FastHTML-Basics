from fasthtml.common import *

app, rt = fast_app()

tasks = []


@rt("/")
def get():
    add_task_form = Form(
        Input(type="text", name="task", placeholder="Add a new task..."),
        Button("Add"),
        method="post",
        action="/add-task",
    )

    task_list = Ul(
        *[
            Li(
                f"{task} ",
                " ",
                A("Delete", href=f"/delete/{i}"),
            )
            for i, task in enumerate(tasks)
        ],
        id="task-list",
    )

    return Titled("ToDo App", H1("My Tasks"), add_task_form, task_list)


@rt("/add-task", methods=["post"])
def post(task: str):
    if task:
        tasks.append(task)
    return RedirectResponse(url="/", status_code=303)


@rt("/delete/{index}", methods=["get"])
def delete(index: int):
    if 0 <= index < len(tasks):
        tasks.pop(index)
    return RedirectResponse(url="/", status_code=303)


serve()
