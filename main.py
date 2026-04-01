import pawpal_system
from datetime import date, time

# Create Owner
owner = pawpal_system.Owner()

# Create at least two Pets
joey = pawpal_system.Pet("joey", [], "is cute")
buddy = pawpal_system.Pet("buddy", [], "energetic pup")
owner.add_pet(joey)
owner.add_pet(buddy)

# Define today
today = date.today()

# Add at least three Tasks with different times (out of order)
task3 = pawpal_system.Task("Play with Joey", today, "weekly", "low", (time(18, 0), time(19, 0)))
joey.add_task(task3)
task1 = pawpal_system.Task("Walk Joey", today, "daily", "high", (time(8, 0), time(9, 0)))
joey.add_task(task1)
task2 = pawpal_system.Task("Feed Buddy", today, "daily", "medium", (time(12, 0), time(12, 30)))
buddy.add_task(task2)
# Add a conflicting task for demonstration
task4 = pawpal_system.Task("Groom Joey", today, "none", "medium", (time(8, 30), time(9, 30)))
joey.add_task(task4)

# Generate today's schedule
scheduler = pawpal_system.Scheduler()
plan = scheduler.generate_daily_plan(owner, today)

# Print "Today's Schedule"
print("Original Schedule (sorted by priority then time):")
scheduler.print_daily_plan(plan)

# Check for conflicts
conflicts = scheduler.detect_conflicts(plan)
scheduler.print_conflicts(conflicts)

# Demonstrate sort_by_time
print("\nTasks sorted by time only:")
time_sorted = scheduler.sort_by_time(owner.get_all_tasks())
scheduler.print_daily_plan(time_sorted)

# Demonstrate filtering by pet name
print("\nTasks for Joey (sorted by time):")
joey_tasks = owner.filter_tasks(pet_name="joey")
joey_sorted = scheduler.sort_by_time(joey_tasks)
scheduler.print_daily_plan(joey_sorted)

# Mark a task completed and demonstrate filtering by completion
joey.mark_task_completed(task1)
print("\nCompleted tasks (sorted by time):")
completed_tasks = owner.filter_tasks(completed=True)
completed_sorted = scheduler.sort_by_time(completed_tasks)
scheduler.print_daily_plan(completed_sorted)

print("\nIncomplete tasks (sorted by time):")
incomplete_tasks = owner.filter_tasks(completed=False)
incomplete_sorted = scheduler.sort_by_time(incomplete_tasks)
scheduler.print_daily_plan(incomplete_sorted)
