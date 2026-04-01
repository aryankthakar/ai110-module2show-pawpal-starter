import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler
from datetime import datetime

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

# Initialize Owner in session state if not present
if 'owner' not in st.session_state:
    st.session_state.owner = Owner()

# Add Pet button
if st.button("Add Pet", type="secondary"):
    new_pet = Pet(name=pet_name, tasks=[], pet_details=species)
    st.session_state.owner.add_pet(new_pet)
    st.success(f"✅ Added pet: **{pet_name}** ({species})")

# Display current pets
if st.session_state.owner.pets:
    st.subheader("🐾 Your Pets")
    pet_cols = st.columns(min(len(st.session_state.owner.pets), 3))
    for i, pet in enumerate(st.session_state.owner.pets):
        with pet_cols[i % 3]:
            st.info(f"**{pet.name}** ({pet.pet_details})")
else:
    st.info("👤 No pets added yet. Add your first pet above!")

st.markdown("### ➕ Add Tasks")
st.caption("Create tasks for your pets with specific times to enable conflict detection.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk", key="task_title")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20, key="duration")
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2, key="priority")
with col4:
    start_time = st.time_input("Start time", value=None, key="start_time")

# Select pet to add task to
if st.session_state.owner.pets:
    pet_names = [pet.name for pet in st.session_state.owner.pets]
    selected_pet_name = st.selectbox("Select pet for task", pet_names, key="selected_pet")
    selected_pet = next(pet for pet in st.session_state.owner.pets if pet.name == selected_pet_name)

    if st.button("Add Task", type="primary"):
        # Create Task instance (using today's date as default, adjust as needed)
        from datetime import date, time, timedelta
        specific_time = None
        if start_time:
            # Calculate end time based on duration
            start_datetime = datetime.combine(date.today(), start_time)
            end_datetime = start_datetime + timedelta(minutes=duration)
            end_time = end_datetime.time()
            specific_time = (start_time, end_time)

        new_task = Task(
            description=task_title,
            date_to_complete=date.today(),
            recurring_frequency="none",  # Default, can be made configurable
            owner_preference=priority,
            specific_time=specific_time
        )
        selected_pet.add_task(new_task)

        time_msg = f" at {start_time}" if start_time else ""
        st.success(f"✅ Added **{task_title}** to {selected_pet_name}{time_msg}")
else:
    st.info("👤 Add a pet first to assign tasks.")

# Display tasks from all pets
all_tasks = st.session_state.owner.get_all_tasks()
if all_tasks:
    st.subheader("📋 Current Tasks")

    # Add filtering options
    col1, col2 = st.columns(2)
    with col1:
        show_completed = st.checkbox("Show completed tasks", value=True)
    with col2:
        if st.session_state.owner.pets:
            filter_pet = st.selectbox("Filter by pet", ["All pets"] + [pet.name for pet in st.session_state.owner.pets])
        else:
            filter_pet = "All pets"

    # Filter tasks
    filtered_tasks = all_tasks
    if not show_completed:
        filtered_tasks = [t for t in filtered_tasks if not t.completed]
    if filter_pet != "All pets":
        filtered_tasks = [t for t in filtered_tasks if any(t in pet.tasks for pet in st.session_state.owner.pets if pet.name == filter_pet)]

    if filtered_tasks:
        task_data = []
        for task in filtered_tasks:
            pet_name = next(pet.name for pet in st.session_state.owner.pets if task in pet.tasks)
            priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task.owner_preference.lower(), "⚪")
            status_icon = "✅" if task.completed else "⏳"
            time_display = f"{task.specific_time[0]} - {task.specific_time[1]}" if task.specific_time else "No time set"

            task_data.append({
                "Status": status_icon,
                "Pet": f"🐾 {pet_name}",
                "Task": task.description,
                "Priority": f"{priority_icon} {task.owner_preference.title()}",
                "Time": time_display
            })

        st.table(task_data)

        # Summary stats
        total_tasks = len(filtered_tasks)
        completed_tasks = sum(1 for t in filtered_tasks if t.completed)
        high_priority = sum(1 for t in filtered_tasks if t.owner_preference.lower() == "high" and not t.completed)

        if completed_tasks > 0:
            st.success(f"✅ {completed_tasks} of {total_tasks} tasks completed")
        if high_priority > 0:
            st.warning(f"⚠️ {high_priority} high-priority tasks remaining")
    else:
        st.info("📝 No tasks match your filters.")
else:
    st.info("📝 No tasks yet. Add your first task above!")

st.divider()

st.subheader("📅 Build Schedule")
st.caption("Generate your pet care schedule for today with intelligent conflict detection.")

# Add sorting option
sort_option = st.radio("Sort schedule by:", ["Priority (High → Low)", "Time (Chronological)"], index=0, help="Priority sorting puts high-priority tasks first, while time sorting organizes by scheduled time.")

if st.button("Generate schedule", type="primary"):
    from datetime import date
    scheduler = Scheduler()
    target_date = date.today()
    plan = scheduler.generate_daily_plan(st.session_state.owner, target_date)
    explanation = scheduler.explain_plan(plan)

    # Apply alternative sorting if selected
    if sort_option == "Time (Chronological)":
        plan = scheduler.sort_by_time(plan)
        explanation += " (Sorted chronologically by time)"

    # Check for conflicts
    conflicts = scheduler.detect_conflicts(plan)

    # Display explanation with better formatting
    st.success(f"📋 **Schedule Summary:** {explanation}")

    # Display conflicts with helpful warnings
    if conflicts:
        st.error("🚨 **Schedule Conflicts Detected!**")

        st.markdown("""
        **Conflicts occur when tasks have overlapping time slots.** Here are the issues found:
        """)

        conflict_expander = st.expander("View Conflict Details", expanded=True)
        with conflict_expander:
            for i, (task1, task2) in enumerate(conflicts, 1):
                time1 = f"{task1.specific_time[0]}-{task1.specific_time[1]}" if task1.specific_time else "No time"
                time2 = f"{task2.specific_time[0]}-{task2.specific_time[1]}" if task2.specific_time else "No time"

                st.markdown(f"""
                **Conflict #{i}:**
                - 🐾 **{task1.description}** ({time1})
                - 🐾 **{task2.description}** ({time2})

                **💡 Suggestion:** Consider rescheduling one of these tasks to avoid overlap.
                """)

        st.warning("⚠️ **Action Required:** Please review and resolve conflicts before proceeding with your schedule.")

    if plan:
        st.subheader("📅 Today's Schedule")

        # Create enhanced schedule table with conflict highlighting
        schedule_data = []
        conflicting_task_names = set()
        if conflicts:
            for task1, task2 in conflicts:
                conflicting_task_names.add(task1.description)
                conflicting_task_names.add(task2.description)

        for task in plan:
            priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task.owner_preference.lower(), "⚪")
            time_display = f"{task.specific_time[0]} - {task.specific_time[1]}" if task.specific_time else "No time specified"

            # Highlight conflicting tasks
            conflict_indicator = "⚠️" if task.description in conflicting_task_names else ""

            schedule_data.append({
                "": conflict_indicator,
                "Task": task.description,
                "Priority": f"{priority_icon} {task.owner_preference.title()}",
                "Time": time_display
            })

        st.table(schedule_data)

        if conflicts:
            st.info("💡 **Tip:** Tasks marked with ⚠️ have scheduling conflicts. Consider adjusting their times.")

    else:
        st.info("📭 No tasks scheduled for today. Add some tasks above to get started!")
