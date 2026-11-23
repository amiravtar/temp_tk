from turtle import ycor

from c1 import Task, TaskPriority
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


class ToDoList:
    task_list: list[Task] = []

    def __init__(self) -> None:
        self.task_list = list()

    def add_task(self, task: Task) -> bool:
        if self.find_task(task.title) is not None:
            return False
        self.task_list.append(task)
        return True

    def remove_task(self, title: str) -> bool:
        for i, y in enumerate(self.task_list):
            if title.lower() == y.title:
                self.task_list.pop(i)
                return True
        else:
            return False

    def list_tasks(self) -> list[Task]:
        return self.task_list

    def list_by_date(self, date: datetime) -> list[Task]:
        tasks = [
            i
            for i in self.task_list
            if i.due_date is not None and i.due_date.date() == date.date()
        ]
        return tasks

    def find_task(self, title: str) -> Task | None:
        for t in self.task_list:
            if t.title == title.lower():
                return t
        return None

    def mark_task_done(self, title: str) -> bool:
        for t in self.task_list:
            if t.title == title.lower():
                t.is_done = True
                return True
        return False

    def edit_task(
        self,
        title: str,
        new_title: str | None = None,
        new_priority: TaskPriority | int | None = None,
        new_due_date: datetime | None = None,
    ) -> bool:
        t: Task | None = None
        for i in self.task_list:
            if i.title == title:
                t = i
                break
        else:
            return False
        if new_title is not None:
            if self.find_task(new_title.lower()) is not None:
                return False
            t.title = new_title.lower()
        if new_priority is not None:
            if isinstance(new_priority, TaskPriority):
                t.priority = new_priority
            elif isinstance(new_priority, int):
                if new_priority not in [1, 2, 3]:
                    raise ValueError("Return a valid priority")
                t.priority = TaskPriority(new_priority)
            else:
                raise ValueError("priority must be int or TaskPriority")
        if new_due_date is not None:
            t.due_date = new_due_date
        return True

    def list_by_priority(self, priority: TaskPriority) -> list[Task]:
        return [t for t in self.task_list if t.priority == priority]

    def count_tasks(self) -> int:
        return len(self.task_list)

    def count_pending(self) -> int:
        return len([i for i in self.task_list if not i.is_done])

    def count_completed(self) -> int:
        return len([i for i in self.task_list if i.is_done])


todo = ToDoList()

task1 = Task("Study Python", TaskPriority.HIGH)
task2 = Task("Practice Tkinter", TaskPriority.MEDIUM)

assert todo.add_task(task1) is True
assert todo.add_task(task2) is True

# Duplicate title, different capitalization
assert todo.add_task(Task("study python", TaskPriority.LOW)) is False

assert todo.count_tasks() == 2
assert todo.count_completed() == 0
assert todo.count_pending() == 2

assert todo.mark_task_done("STUDY PYTHON") is True

assert todo.count_completed() == 1
assert todo.count_pending() == 1

assert todo.remove_task("practice tkinter") is True
assert todo.count_tasks() == 1
