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

# Add at least three Tasks with different times
task1 = pawpal_system.Task("Walk Joey", today, "daily", "high", (time(8, 0), time(9, 0)))
joey.add_task(task1)
task2 = pawpal_system.Task("Feed Buddy", today, "daily", "medium", (time(12, 0), time(12, 30)))
buddy.add_task(task2)
task3 = pawpal_system.Task("Play with Joey", today, "weekly", "low", (time(18, 0), time(19, 0)))
joey.add_task(task3)

# Generate today's schedule
scheduler = pawpal_system.Scheduler()
plan = scheduler.generate_daily_plan(owner, today)

# Print "Today's Schedule"
scheduler.print_daily_plan(plan)
