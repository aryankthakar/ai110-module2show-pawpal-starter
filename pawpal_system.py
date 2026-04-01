from dataclasses import dataclass
from typing import List, Tuple, Optional
from datetime import date, time, timedelta


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

    def mark_task_completed(self, task: Task) -> None:
        """
        Mark a task as completed and automatically create the next occurrence if recurring.

        This method handles the completion workflow for recurring tasks by automatically
        scheduling the next instance based on the recurrence pattern.

        Args:
            task: The Task object to mark as completed. Must belong to this pet.

        Behavior:
            - Marks the task as completed
            - For daily recurring tasks: Creates new task for next day
            - For weekly recurring tasks: Creates new task for next week
            - For non-recurring tasks: No additional action

        Note:
            If the task doesn't belong to this pet, no action is taken.
        """
        if task in self.tasks:
            task.mark_completed()
            if task.recurring_frequency == "daily":
                next_date = task.date_to_complete + timedelta(days=1)
                new_task = Task(task.description, next_date, task.recurring_frequency, task.owner_preference, task.specific_time)
                self.add_task(new_task)
            elif task.recurring_frequency == "weekly":
                next_date = task.date_to_complete + timedelta(weeks=1)
                new_task = Task(task.description, next_date, task.recurring_frequency, task.owner_preference, task.specific_time)
                self.add_task(new_task)
            elif task.recurring_frequency == "monthly":
                # Calculate next month
                year = task.date_to_complete.year
                month = task.date_to_complete.month + 1
                if month > 12:
                    month = 1
                    year += 1
                next_date = task.date_to_complete.replace(year=year, month=month)
                new_task = Task(task.description, next_date, task.recurring_frequency, task.owner_preference, task.specific_time)
                self.add_task(new_task)


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

    def filter_tasks(self, completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """
        Filter tasks by completion status and/or pet name.

        Provides flexible querying of tasks across all pets owned by this owner.
        Filters can be combined (e.g., incomplete tasks for a specific pet).

        Args:
            completed: Filter by completion status.
                - True: Return only completed tasks
                - False: Return only incomplete tasks
                - None: Include all tasks regardless of completion status
            pet_name: Filter by specific pet name.
                - If provided: Return only tasks for the specified pet
                - None: Include tasks from all pets

        Returns:
            List of Task objects matching the filter criteria.
            Returns all tasks if no filters are specified.

        Examples:
            >>> owner.filter_tasks(completed=False)  # Get all incomplete tasks
            >>> owner.filter_tasks(pet_name="Buddy")  # Get all tasks for Buddy
            >>> owner.filter_tasks(completed=True, pet_name="Joey")  # Completed tasks for Joey
        """
        tasks = self.get_all_tasks()

        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]

        if pet_name is not None:
            pet_tasks = []
            for pet in self.pets:
                if pet.name == pet_name:
                    pet_tasks.extend(pet.tasks)
            tasks = [t for t in tasks if t in pet_tasks]

        return tasks


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

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """
        Sort tasks by their start time, with tasks without specific times at the end.

        This method provides an alternative sorting to the priority-based sorting in
        generate_daily_plan(), useful for chronological ordering.

        Args:
            tasks: List of Task objects to sort

        Returns:
            New list of tasks sorted by start time (ascending), with tasks without
            specific_time placed at the end
        """
        return sorted(tasks, key=lambda t: t.specific_time[0] if t.specific_time else time.max)

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

    def detect_conflicts(self, tasks: List[Task]) -> List[Tuple[Task, Task]]:
        """
        Detect time conflicts between tasks with overlapping time ranges.

        Uses an optimized algorithm that sorts tasks by start time to reduce
        unnecessary comparisons. Only tasks with specific_time defined are checked.

        Args:
            tasks: List of Task objects to check for conflicts

        Returns:
            List of tuples, where each tuple contains two conflicting Task objects.
            Each pair represents tasks that have overlapping time windows.

        Algorithm:
            1. Filter tasks with specific_time
            2. Sort by start time (O(n log n))
            3. Check adjacent tasks for overlaps with early exit optimization
            4. Return list of conflicting pairs

        Time Complexity: O(n log n + k) where k is number of potential overlaps
        """
        conflicts = []
        # Sort tasks by start time for better performance (optional optimization)
        tasks_with_time = [t for t in tasks if t.specific_time]
        tasks_with_time.sort(key=lambda t: t.specific_time[0])
        
        for i in range(len(tasks_with_time)):
            for j in range(i + 1, len(tasks_with_time)):
                task1, task2 = tasks_with_time[i], tasks_with_time[j]
                # Early exit if task2 starts after task1 ends (since sorted)
                if task2.specific_time[0] >= task1.specific_time[1]:
                    break
                if self._tasks_overlap(task1, task2):
                    conflicts.append((task1, task2))
        return conflicts

    def _tasks_overlap(self, task1: Task, task2: Task) -> bool:
        """
        Check if two tasks have overlapping time ranges.

        Uses the standard interval overlap algorithm: two intervals [a,b] and [c,d]
        overlap if a < d and c < b.

        Args:
            task1: First task with specific_time defined
            task2: Second task with specific_time defined

        Returns:
            True if the tasks' time windows overlap, False otherwise

        Note:
            Assumes both tasks have specific_time defined (should be checked by caller)
        """
        start1, end1 = task1.specific_time
        start2, end2 = task2.specific_time
        return start1 < end2 and start2 < end1

    def print_conflicts(self, conflicts: List[Tuple[Task, Task]]) -> None:
        """
        Print detected conflicts to the console in a user-friendly format.

        Displays conflict information to help users identify scheduling issues
        without halting program execution.

        Args:
            conflicts: List of tuples containing conflicting task pairs,
                as returned by detect_conflicts()

        Output Format:
            If conflicts exist:
                "Schedule Conflicts Detected:"
                "- 'Task A' (start-end) conflicts with 'Task B' (start-end)"
                ...
            If no conflicts:
                "No conflicts detected."
        """
        if conflicts:
            print("Schedule Conflicts Detected:")
            for task1, task2 in conflicts:
                print(f"- '{task1.description}' ({task1.specific_time[0]}-{task1.specific_time[1]}) conflicts with '{task2.description}' ({task2.specific_time[0]}-{task2.specific_time[1]})")
        else:
            print("No conflicts detected.")
