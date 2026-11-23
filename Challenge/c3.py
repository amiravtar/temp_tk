from datetime import datetime, date
from zoneinfo import ZoneInfo

from Challenge.c1 import Task


def get_current_datetime() -> datetime:
    return datetime.now(ZoneInfo("UTC"))


def format_datetime(value: datetime) -> str:
    return value.strftime("%Y/%m/%d-%H:%M:%S")


def parse_datetime(value: str) -> datetime:
    return datetime.strptime(value, ("%Y/%m/%d-%H:%M:%S"))


def is_overdue(task: Task) -> bool:
    if (
        task.due_date is not None
        and not task.is_done
        and task.due_date.date() <= datetime.now(ZoneInfo("UTC")).date()
    ):
        return True
    return False


def get_tasks_by_date(tasks: list[Task], target_date: date) -> list[Task]:
    return [
        t for t in tasks if t.due_date is not None and t.due_date.date() == target_date
    ]


def get_tasks_in_range(
    tasks: list[Task],
    start_date: date,
    end_date: date,
) -> list[Task]:
    if start_date > end_date:
        raise ValueError("date ranges incorrect")
    return [
        t
        for t in tasks
        if t.due_date is not None and start_date <= t.due_date.date() <= end_date
    ]


def get_overdue_tasks(tasks: list[Task]) -> list[Task]:
    return [t for t in tasks if is_overdue(t)]
