from fasthtml.common import *
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app, rt = fast_app()
DATABASE_URL = "sqlite:///./todo.db"

# Datenbank-Setup mit SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Datenbankmodell
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, index=True)


# Erstelle die Datenbanktabellen
Base.metadata.create_all(bind=engine)


# CRUD-Operationen mit SQLAlchemy
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def add_task_to_db(db, task: str):
    db_task = Task(task=task)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks_from_db(db):
    return db.query(Task).all()


def update_task_in_db(db, task_id: int, new_task: str):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db_task.task = new_task
        db.commit()
        db.refresh(db_task)
    return db_task


def delete_task_from_db(db, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()


@rt("/")
def get():
    db = next(get_db())
    tasks = get_tasks_from_db(db)

    add_task_form = Form(
        Input(type="text", name="task", placeholder="Neue Aufgabe hinzufügen..."),
        Button("Hinzufügen"),
        method="post",
        action="/add-task",
    )

    task_list = Ul(
        *[
            Li(
                f"{task.task} ",
                A("Bearbeiten", href=f"/edit/{task.id}"),
                " ",
                A("Löschen", href=f"/delete/{task.id}"),
            )
            for task in tasks
        ],
        id="task-list",
    )

    return Titled("ToDo App", H1("Meine Aufgaben"), add_task_form, task_list)


@rt("/add-task", methods=["post"])
def post(task: str):
    db = next(get_db())
    if task:
        add_task_to_db(db, task)
    return RedirectResponse(url="/", status_code=303)


@rt("/edit/{task_id}", methods=["get", "post"])
def edit(task_id: int, task: str = None):
    db = next(get_db())
    if task is not None:
        update_task_in_db(db, task_id, task)
        return RedirectResponse(url="/", status_code=303)

    db_task = db.query(Task).filter(Task.id == task_id).first()
    task_text = db_task.task if db_task else ""

    edit_form = Form(
        Input(type="text", name="task", value=task_text),
        Button("Aktualisieren"),
        method="post",
        action=f"/edit/{task_id}",
    )

    return Titled("Aufgabe Bearbeiten", edit_form)


@rt("/delete/{task_id}", methods=["get"])
def delete(task_id: int):
    db = next(get_db())
    delete_task_from_db(db, task_id)
    return RedirectResponse(url="/", status_code=303)


serve()
