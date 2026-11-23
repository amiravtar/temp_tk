from enum import IntEnum
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


class TaskPriority(IntEnum):
    """Docstring for TaskPriority."""

    HIGH = 3
    MEDIUM = 2
    LOW = 1

    @property
    def label(self) -> str:
        return _label[self]


_label: dict[TaskPriority, str] = {
    TaskPriority.HIGH: "بالا",
    TaskPriority.MEDIUM: "متوسط",
    TaskPriority.LOW: "کم",
}


def get_now_date_time_aware(
    zone: ZoneInfo | None = ZoneInfo("Asia/Tehran"),
) -> datetime:
    return datetime.now(zone)


class Task:
    title: str
    is_done: bool
    priority: TaskPriority
    created_date: datetime
    due_date: datetime | None = None

    def __init__(
        self,
        title: str,
        priority: TaskPriority | int,
        due_date: datetime | None = None,
    ) -> None:
        if title.strip()=="":
            raise ValueError("Enter a valid title")
        self.title = title.lower()
        self.is_done = False
        if isinstance(priority, TaskPriority):
            self.priority = priority
        elif isinstance(priority, int):
            if priority not in [1,2,3]:
                raise ValueError("Return a valid priority")
            self.priority = TaskPriority(priority)
        else:
            raise ValueError("priority must be int or TaskPriority")
        self.created_date = get_now_date_time_aware()
        self.due_date = due_date

    def mark_done(self):
        self.is_done = True

    def __str__(self) -> str:
        return f"{self.title}:{self.priority.label}:{self.due_date if self.due_date else ''}"

    def __repr__(self) -> str:
        return self.__str__()
