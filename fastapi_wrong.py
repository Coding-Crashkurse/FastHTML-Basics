from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fasthtml.common import *

app = FastAPI()
tasks = []


@app.get("/", response_class=HTMLResponse)
async def get():
    add_task_form = Form(
        Input(type="text", name="task", placeholder="Add new task..."),
        Button("Add task"),
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

    content = to_xml(Titled("ToDo App", H1("My Tasks"), add_task_form, task_list))
    print(content)
    return HTMLResponse(content=content)


def task_list_partial():
    return to_xml(
        Ul(
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
    )


@app.post("/add-task", response_class=HTMLResponse)
async def post(task: str = Form(...)):
    if task:
        tasks.append(task)
    return HTMLResponse(content=task_list_partial())


@app.get("/delete/{index}", response_class=HTMLResponse)
async def delete(index: int):
    if 0 <= index < len(tasks):
        tasks.pop(index)
    return HTMLResponse(content=task_list_partial())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
