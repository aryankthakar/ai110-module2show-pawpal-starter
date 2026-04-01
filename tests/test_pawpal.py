import pytest
from datetime import date, time, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


def test_task_completion():
    """Verify that calling mark_completed() changes the task's status from False to True."""
    task = Task(
        description="Test Task",
        date_to_complete=date.today(),
        recurring_frequency="none",
        owner_preference="medium",
        specific_time=(time(10, 0), time(11, 0))
    )
    # Initially, completed should be False
    assert task.completed is False
    # Call mark_completed
    task.mark_completed()
    # Now, completed should be True
    assert task.completed is True


def test_task_addition():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet(name="Test Pet", tasks=[])
    task = Task(
        description="Test Task",
        date_to_complete=date.today(),
        recurring_frequency="daily",
        owner_preference="high",
        specific_time=(time(8, 0), time(9, 0))
    )
    # Initially, task count should be 0
    assert len(pet.tasks) == 0
    # Add the task
    pet.add_task(task)
    # Now, task count should be 1
    assert len(pet.tasks) == 1
    # Verify the task is in the list
    assert task in pet.tasks


def test_task_edit_description():
    """Verify that edit_description updates the task's description."""
    task = Task(
        description="Original",
        date_to_complete=date.today(),
        recurring_frequency="none",
        owner_preference="medium"
    )
    task.edit_description("Updated")
    assert task.description == "Updated"


def test_task_edit_owner_preference():
    """Verify that edit_owner_preference updates the preference."""
    task = Task(
        description="Test",
        date_to_complete=date.today(),
        recurring_frequency="none",
        owner_preference="low"
    )
    task.edit_owner_preference("high")
    assert task.owner_preference == "high"


def test_task_edit_time():
    """Verify that edit_time updates the specific_time tuple."""
    task = Task(
        description="Test",
        date_to_complete=date.today(),
        recurring_frequency="none",
        owner_preference="medium"
    )
    new_time = (time(14, 0), time(15, 0))
    task.edit_time(new_time)
    assert task.specific_time == new_time


def test_pet_remove_task():
    """Verify that removing a task decreases the pet's task count."""
    pet = Pet(name="Test Pet", tasks=[])
    task = Task(
        description="Test Task",
        date_to_complete=date.today(),
        recurring_frequency="daily",
        owner_preference="high"
    )
    pet.add_task(task)
    assert len(pet.tasks) == 1
    pet.remove_task(task)
    assert len(pet.tasks) == 0


def test_pet_add_duplicate_task():
    """Verify that adding a duplicate task does not increase count."""
    pet = Pet(name="Test Pet", tasks=[])
    task = Task(
        description="Test Task",
        date_to_complete=date.today(),
        recurring_frequency="daily",
        owner_preference="high"
    )
    pet.add_task(task)
    pet.add_task(task)  # Duplicate
    assert len(pet.tasks) == 1


def test_owner_add_pet():
    """Verify that adding a pet increases the owner's pet count."""
    owner = Owner()
    pet = Pet(name="Test Pet", tasks=[])
    owner.add_pet(pet)
    assert len(owner.pets) == 1


def test_owner_remove_pet():
    """Verify that removing a pet decreases the owner's pet count."""
    owner = Owner()
    pet = Pet(name="Test Pet", tasks=[])
    owner.add_pet(pet)
    owner.remove_pet(pet)
    assert len(owner.pets) == 0


def test_owner_get_all_tasks():
    """Verify get_all_tasks flattens tasks from all pets."""
    owner = Owner()
    pet1 = Pet(name="Pet1", tasks=[])
    pet2 = Pet(name="Pet2", tasks=[])
    task1 = Task("Task1", date.today(), "none", "high")
    task2 = Task("Task2", date.today(), "none", "medium")
    pet1.add_task(task1)
    pet2.add_task(task2)
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    all_tasks = owner.get_all_tasks()
    assert len(all_tasks) == 2
    assert task1 in all_tasks
    assert task2 in all_tasks


def test_scheduler_generate_daily_plan():
    """Verify generate_daily_plan filters and sorts tasks for the date."""
    owner = Owner()
    pet = Pet(name="Pet", tasks=[])
    task1 = Task("High Task", date.today(), "none", "high", (time(10, 0), time(11, 0)))
    task2 = Task("Low Task", date.today(), "none", "low", (time(9, 0), time(10, 0)))
    pet.add_task(task1)
    pet.add_task(task2)
    owner.add_pet(pet)
    scheduler = Scheduler()
    plan = scheduler.generate_daily_plan(owner, date.today())
    assert len(plan) == 2
    assert plan[0].owner_preference == "high"  # Sorted by priority
    assert plan[1].owner_preference == "low"


def test_scheduler_explain_plan():
    """Verify explain_plan returns a summary string."""
    tasks = [
        Task("Task1", date.today(), "none", "high"),
        Task("Task2", date.today(), "none", "medium")
    ]
    scheduler = Scheduler()
    explanation = scheduler.explain_plan(tasks)
    assert "2 tasks" in explanation
    assert "1 are high priority" in explanation


def test_scheduler_print_daily_plan(capsys):
    """Verify print_daily_plan outputs the schedule to stdout."""
    tasks = [
        Task("Task1", date.today(), "none", "high", (time(8, 0), time(9, 0))),
        Task("Task2", date.today(), "none", "medium")
    ]
    Scheduler.print_daily_plan(tasks)
    captured = capsys.readouterr()
    assert "Today's Schedule:" in captured.out
    assert "Task1 (high priority): 08:00:00 - 09:00:00" in captured.out
    assert "Task2 (medium priority): No time specified" in captured.out


def test_owner_filter_tasks_by_completion():
    """Verify filter_tasks filters by completion status."""
    owner = Owner()
    pet = Pet(name="Test Pet", tasks=[])
    task1 = Task("Task1", date.today(), "none", "high")
    task2 = Task("Task2", date.today(), "none", "medium")
    task2.mark_completed()
    pet.add_task(task1)
    pet.add_task(task2)
    owner.add_pet(pet)

    incomplete = owner.filter_tasks(completed=False)
    assert len(incomplete) == 1
    assert incomplete[0].description == "Task1"

    complete = owner.filter_tasks(completed=True)
    assert len(complete) == 1
    assert complete[0].description == "Task2"


def test_owner_filter_tasks_by_pet_name():
    """Verify filter_tasks filters by pet name."""
    owner = Owner()
    pet1 = Pet(name="Pet1", tasks=[])
    pet2 = Pet(name="Pet2", tasks=[])
    task1 = Task("Task1", date.today(), "none", "high")
    task2 = Task("Task2", date.today(), "none", "medium")
    pet1.add_task(task1)
    pet2.add_task(task2)
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    pet1_tasks = owner.filter_tasks(pet_name="Pet1")
    assert len(pet1_tasks) == 1
    assert pet1_tasks[0].description == "Task1"

    pet2_tasks = owner.filter_tasks(pet_name="Pet2")
    assert len(pet2_tasks) == 1
    assert pet2_tasks[0].description == "Task2"


def test_pet_mark_task_completed_recurring():
    """Verify mark_task_completed creates next occurrence for recurring tasks."""
    pet = Pet(name="Test Pet", tasks=[])
    task = Task("Daily Task", date.today(), "daily", "high", (time(8, 0), time(9, 0)))
    pet.add_task(task)
    assert len(pet.tasks) == 1
    pet.mark_task_completed(task)
    assert task.completed is True
    assert len(pet.tasks) == 2  # Original + new
    new_task = [t for t in pet.tasks if not t.completed][0]
    assert new_task.date_to_complete == date.today() + timedelta(days=1)
    assert new_task.description == "Daily Task"
    assert new_task.recurring_frequency == "daily"


def test_scheduler_detect_conflicts():
    """Verify detect_conflicts identifies overlapping tasks."""
    scheduler = Scheduler()
    task1 = Task("Task1", date.today(), "none", "high", (time(8, 0), time(9, 0)))
    task2 = Task("Task2", date.today(), "none", "medium", (time(8, 30), time(9, 30)))  # Overlaps with task1
    task3 = Task("Task3", date.today(), "none", "low", (time(10, 0), time(11, 0)))  # No overlap
    tasks = [task1, task2, task3]
    
    conflicts = scheduler.detect_conflicts(tasks)
    assert len(conflicts) == 1
    assert (task1, task2) in conflicts or (task2, task1) in conflicts


def test_scheduler_sorting_chronological_within_priority():
    """Verify tasks are sorted chronologically within the same priority level."""
    owner = Owner()
    pet = Pet(name="Pet", tasks=[])
    # All medium priority, different times
    task1 = Task("Task1", date.today(), "none", "medium", (time(14, 0), time(15, 0)))
    task2 = Task("Task2", date.today(), "none", "medium", (time(10, 0), time(11, 0)))
    task3 = Task("Task3", date.today(), "none", "medium", (time(12, 0), time(13, 0)))
    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)
    owner.add_pet(pet)
    scheduler = Scheduler()
    plan = scheduler.generate_daily_plan(owner, date.today())
    assert len(plan) == 3
    # Should be sorted by time: task2 (10:00), task3 (12:00), task1 (14:00)
    assert plan[0].description == "Task2"
    assert plan[1].description == "Task3"
    assert plan[2].description == "Task1"


def test_scheduler_sorting_tasks_without_times_at_end():
    """Verify tasks without specific times appear at the end of their priority group."""
    owner = Owner()
    pet = Pet(name="Pet", tasks=[])
    task1 = Task("Timed Task", date.today(), "none", "medium", (time(10, 0), time(11, 0)))
    task2 = Task("No Time Task", date.today(), "none", "medium")  # No specific_time
    pet.add_task(task1)
    pet.add_task(task2)
    owner.add_pet(pet)
    scheduler = Scheduler()
    plan = scheduler.generate_daily_plan(owner, date.today())
    assert len(plan) == 2
    assert plan[0].description == "Timed Task"  # Timed task first
    assert plan[1].description == "No Time Task"  # No time task at end


def test_recurrence_weekly():
    """Verify marking a weekly recurring task complete creates next week's occurrence."""
    pet = Pet(name="Test Pet", tasks=[])
    task = Task("Weekly Task", date.today(), "weekly", "high", (time(8, 0), time(9, 0)))
    pet.add_task(task)
    pet.mark_task_completed(task)
    assert len(pet.tasks) == 2
    new_task = [t for t in pet.tasks if not t.completed][0]
    assert new_task.date_to_complete == date.today() + timedelta(weeks=1)
    assert new_task.recurring_frequency == "weekly"


def test_recurrence_monthly():
    """Verify marking a monthly recurring task complete creates next month's occurrence."""
    pet = Pet(name="Test Pet", tasks=[])
    task = Task("Monthly Task", date.today(), "monthly", "high", (time(8, 0), time(9, 0)))
    pet.add_task(task)
    pet.mark_task_completed(task)
    assert len(pet.tasks) == 2
    new_task = [t for t in pet.tasks if not t.completed][0]
    # Calculate next month (simplified, assumes no year rollover issues)
    next_month = date.today().replace(month=date.today().month % 12 + 1)
    if date.today().month == 12:
        next_month = next_month.replace(year=date.today().year + 1)
    assert new_task.date_to_complete == next_month
    assert new_task.recurring_frequency == "monthly"


def test_scheduler_detect_exact_time_conflicts():
    """Verify detect_conflicts flags tasks with identical time slots."""
    scheduler = Scheduler()
    task1 = Task("Task1", date.today(), "none", "high", (time(8, 0), time(9, 0)))
    task2 = Task("Task2", date.today(), "none", "medium", (time(8, 0), time(9, 0)))  # Exact duplicate
    task3 = Task("Task3", date.today(), "none", "low", (time(10, 0), time(11, 0)))  # No conflict
    tasks = [task1, task2, task3]
    
    conflicts = scheduler.detect_conflicts(tasks)
    assert len(conflicts) == 1
    assert (task1, task2) in conflicts or (task2, task1) in conflicts


def test_scheduler_detect_multiple_conflicts():
    """Verify detect_conflicts handles multiple overlapping pairs."""
    scheduler = Scheduler()
    task1 = Task("Task1", date.today(), "none", "high", (time(8, 0), time(10, 0)))
    task2 = Task("Task2", date.today(), "none", "medium", (time(9, 0), time(11, 0)))  # Overlaps with task1
    task3 = Task("Task3", date.today(), "none", "low", (time(9, 30), time(12, 0)))  # Overlaps with task2 and task1
    tasks = [task1, task2, task3]
    
    conflicts = scheduler.detect_conflicts(tasks)
    assert len(conflicts) == 3  # (task1,task2), (task1,task3), and (task2,task3)
    # Check that all expected pairs are present (order doesn't matter)
    conflict_pairs = set()
    for t1, t2 in conflicts:
        conflict_pairs.add((t1.description, t2.description))
        conflict_pairs.add((t2.description, t1.description))  # Add both orders
    expected_pairs = {("Task1", "Task2"), ("Task1", "Task3"), ("Task2", "Task3")}
    assert expected_pairs.issubset(conflict_pairs)