import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

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
if st.button("Add Pet"):
    new_pet = Pet(name=pet_name, tasks=[], pet_details=species)
    st.session_state.owner.add_pet(new_pet)
    st.success(f"Added pet: {pet_name}")

# Display current pets
if st.session_state.owner.pets:
    st.write("Your Pets:")
    for pet in st.session_state.owner.pets:
        st.write(f"- {pet.name} ({pet.pet_details})")
else:
    st.info("No pets added yet.")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

# Select pet to add task to
if st.session_state.owner.pets:
    pet_names = [pet.name for pet in st.session_state.owner.pets]
    selected_pet_name = st.selectbox("Select pet for task", pet_names)
    selected_pet = next(pet for pet in st.session_state.owner.pets if pet.name == selected_pet_name)

    if st.button("Add task"):
        # Create Task instance (using today's date as default, adjust as needed)
        from datetime import date
        new_task = Task(
            description=task_title,
            date_to_complete=date.today(),
            recurring_frequency="none",  # Default, can be made configurable
            owner_preference=priority
        )
        selected_pet.add_task(new_task)
        st.success(f"Added task '{task_title}' to {selected_pet_name}")
else:
    st.info("Add a pet first to assign tasks.")

# Display tasks from all pets
all_tasks = st.session_state.owner.get_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    task_data = [
        {
            "Pet": next(pet.name for pet in st.session_state.owner.pets if task in pet.tasks),
            "Title": task.description,
            "Priority": task.owner_preference,
            "Completed": task.completed
        }
        for task in all_tasks
    ]
    st.table(task_data)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    from datetime import date
    scheduler = Scheduler()
    target_date = date.today()
    plan = scheduler.generate_daily_plan(st.session_state.owner, target_date)
    explanation = scheduler.explain_plan(plan)
    
    st.write("**Schedule Explanation:**")
    st.write(explanation)
    
    if plan:
        st.write("**Today's Schedule:**")
        schedule_data = [
            {
                "Task": task.description,
                "Priority": task.owner_preference,
                "Time": f"{task.specific_time[0]} - {task.specific_time[1]}" if task.specific_time else "No time specified"
            }
            for task in plan
        ]
        st.table(schedule_data)
    else:
        st.info("No tasks scheduled for today.")
