from dataclasses import dataclass
from typing import List
from datetime import date, time


@dataclass
class Task:
    description: str
    date_to_complete: date
    recurring_frequency: str
    priority_level: int
    specific_time: time = None

    def edit_description(self, new_desc: str) -> None:
        pass

    def edit_priority(self, new_pri: int) -> None:
        pass

    def edit_date(self, new_date: date) -> None:
        pass

    def edit_recurring(self, new_freq: str) -> None:
        pass

    def edit_time(self, new_time: time) -> None:
        pass


@dataclass
class Pet:
    tasks: List[Task]

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass


class Owner:
    def __init__(self):
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def remove_pet(self, pet: Pet) -> None:
        pass


class Scheduler:
    def generate_daily_plan(self, owner: Owner, date: date) -> List[Task]:
        pass

    def explain_plan(self, plan: List[Task]) -> str:
        pass
