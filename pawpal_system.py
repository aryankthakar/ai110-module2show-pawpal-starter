from dataclasses import dataclass
from typing import List, Tuple
from datetime import date, time


@dataclass
class Task:
    """
    Represents a single pet care task.

    Attributes:
        description (str): A brief description of the task (e.g., "Walk the dog").
        date_to_complete (date): The date when the task should be completed.
        recurring_frequency (str): How often the task repeats ("none", "daily", "weekly", "monthly").
        owner_preference (str): The owner's priority level for the task ("high", "medium", "low").
        specific_time (Tuple[time, time], optional): Start and end times for the task. Defaults to None.
        completed (bool): Whether the task has been completed. Defaults to False.
    """
    description: str
    date_to_complete: date
    recurring_frequency: str
    owner_preference: str
    specific_time: Tuple[time, time] = None
    completed: bool = False

    def edit_description(self, new_desc: str) -> None:
        """Update the task's description."""
        self.description = new_desc

    def edit_owner_preference(self, new_pref: str) -> None:
        """Update the owner's preference for the task."""
        self.owner_preference = new_pref

    def edit_date(self, new_date: date) -> None:
        """Update the date to complete the task."""
        self.date_to_complete = new_date

    def edit_recurring(self, new_freq: str) -> None:
        """Update the recurring frequency of the task."""
        self.recurring_frequency = new_freq

    def edit_time(self, new_time: Tuple[time, time]) -> None:
        """Update the specific time window for the task."""
        self.specific_time = new_time

    def mark_completed(self) -> None:
        """Mark the task as completed."""
        self.completed = True


@dataclass
class Pet:
    """
    Represents a pet and its associated care tasks.

    Attributes:
        name (str): The name of the pet.
        tasks (List[Task]): A list of tasks assigned to this pet.
        pet_details (str): Additional details about the pet (e.g., breed, age). Defaults to empty string.
    """
    name: str
    tasks: List[Task]
    pet_details: str = ""

    def add_task(self, task: Task) -> None:
        """Add a task to the pet's task list if not already present."""
        if task not in self.tasks:
            self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from the pet's task list if present."""
        if task in self.tasks:
            self.tasks.remove(task)


class Owner:
    """
    Represents the pet owner who manages multiple pets.

    Attributes:
        pets (List[Pet]): A list of pets owned by this owner.
    """

    def __init__(self):
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list if not already present."""
        if pet not in self.pets:
            self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from the owner's pet list if present."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_all_tasks(self) -> List[Task]:
        """Retrieve a flattened list of all tasks from all pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """
    Handles scheduling and organizing pet care tasks.

    This class provides methods to generate daily plans, explain plans, and print schedules.
    """

    @staticmethod
    def _is_task_due(task: Task, target_date: date) -> bool:
        """Check if a task is due on the target date based on its recurrence."""
        if task.recurring_frequency in ("none", ""):
            return task.date_to_complete == target_date
        elif task.recurring_frequency == "daily":
            return True
        elif task.recurring_frequency == "weekly":
            return task.date_to_complete.weekday() == target_date.weekday()
        elif task.recurring_frequency == "monthly":
            return task.date_to_complete.day == target_date.day
        return False

    @staticmethod
    def _priority_value(pref: str) -> int:
        """Convert preference string to a numeric value for sorting."""
        mapping = {"high": 1, "medium": 2, "low": 3}
        return mapping.get(pref.lower(), 4)

    def generate_daily_plan(self, owner: Owner, target_date: date) -> List[Task]:
        """
        Generate a sorted list of due tasks for the target date.

        Filters tasks that are due and not completed, then sorts by priority and start time.
        """
        all_tasks = owner.get_all_tasks()
        due_tasks = [task for task in all_tasks if not task.completed and self._is_task_due(task, target_date)]
        due_tasks.sort(key=lambda t: (self._priority_value(t.owner_preference), t.specific_time[0] if t.specific_time else time.max))
        return due_tasks

    def explain_plan(self, plan: List[Task]) -> str:
        """Provide a textual summary of the daily plan."""
        if not plan:
            return "No tasks scheduled for this day."
        total = len(plan)
        high_priority = sum(1 for t in plan if t.owner_preference.lower() == "high")
        explanation = f"Daily plan includes {total} tasks. "
        if high_priority:
            explanation += f"{high_priority} are high priority. "
        return explanation

    @staticmethod
    def print_daily_plan(plan: List[Task]) -> None:
        """Print the daily plan to the console."""
        print("Today's Schedule:")
        if plan:
            for task in plan:
                start, end = task.specific_time or (None, None)
                time_str = f"{start} - {end}" if start else "No time specified"
                print(f"- {task.description} ({task.owner_preference} priority): {time_str}")
        else:
            print("No tasks scheduled.")
