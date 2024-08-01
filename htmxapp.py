from fasthtml.common import *

app, rt = fast_app()

tasks = []


@rt("/")
def get():
    add_task_form = Form(
        Input(type="text", name="task", placeholder="Neue Aufgabe hinzufügen..."),
        Button("Hinzufügen"),
        method="post",
        action="/add-task",
        hx_post="/add-task",
        hx_target="#task-list",
        hx_swap="outerHTML",
    )

    task_list = Ul(
        *[
            Li(
                f"{task} ",
                " ",
                A(
                    "Löschen",
                    href=f"/delete/{i}",
                    hx_get=f"/delete/{i}",
                    hx_target=f"#task-{i}",
                    hx_swap="outerHTML",
                ),
                id=f"task-{i}",
            )
            for i, task in enumerate(tasks)
        ],
        id="task-list",
    )

    return Titled("ToDo App", H1("Meine Aufgaben"), add_task_form, task_list)


def task_list_partial():
    return Ul(
        *[
            Li(
                f"{task} ",
                A(
                    "Löschen",
                    href=f"/delete/{i}",
                    hx_get=f"/delete/{i}",
                    hx_target="#task-list",
                    hx_swap="outerHTML",
                ),
                id=f"task-{i}",
            )
            for i, task in enumerate(tasks)
        ],
        id="task-list",
    )


@rt("/add-task", methods=["post"])
def post(task: str):
    if task:
        tasks.append(task)
    return task_list_partial()


@rt("/delete/{index}", methods=["get"])
def delete(index: int):
    if 0 <= index < len(tasks):
        tasks.pop(index)
    return task_list_partial()


serve()
