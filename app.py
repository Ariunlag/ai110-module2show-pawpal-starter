from datetime import datetime
from pathlib import Path
import sys

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from pawpal_system import Owner, Pet, Scheduler, Task


def get_or_create_pet(owner: Owner, pet_name: str, species: str) -> Pet:
    """Return an existing pet if present or create it if missing."""
    pet_name = pet_name.strip()
    try:
        pet = owner.get_pet(pet_name)
        if (not pet.species or pet.species == "other") and species:
            pet.species = species
        return pet
    except KeyError:
        pet = Pet(name=pet_name, species=species)
        owner.add_pet(pet)
        return pet


def format_task_line(task: Task) -> str:
    """Return a consistent display line for a task."""
    return f"[{task.scheduled_time}] {task.description} ({task.frequency})"


def show_conflicts(owner: Owner, scheduler: Scheduler) -> None:
    """Display clear conflict warnings in the UI."""
    conflicts = scheduler.detect_conflicts(owner.get_all_tasks())

    if not conflicts:
        st.success("No scheduling conflicts detected.")
        return

    st.warning("Scheduling conflicts detected. Review overlapping tasks below.")

    for conflict in conflicts:
        if conflict["pet_1"] == conflict["pet_2"]:
            st.warning(
                f"Conflict at {conflict['time']}: "
                f"'{conflict['task_1']}' and '{conflict['task_2']}' "
                f"for pet '{conflict['pet_1']}'."
            )
        else:
            st.warning(
                f"Conflict at {conflict['time']}: "
                f"'{conflict['task_1']}' for {conflict['pet_1']} and "
                f"'{conflict['task_2']}' for {conflict['pet_2']}."
            )


def render_schedule(owner: Owner) -> None:
    """Render grouped tasks per pet using scheduler helpers."""
    scheduler = Scheduler(owner)
    current_time = datetime.now().strftime("%H:%M")

    st.subheader("Today's Schedule")
    st.caption(f"Current time: {current_time}")

    if not owner.pets:
        st.info("No pets yet. Add a pet to start scheduling.")
        return

    grouped_tasks = scheduler.get_tasks_grouped_by_pet()

    for pet_name in sorted(grouped_tasks.keys()):
        pet = owner.get_pet(pet_name)
        tasks = grouped_tasks[pet_name]

        st.markdown(f"### {pet.name} ({pet.species or 'unknown'})")

        if not tasks:
            st.info("No tasks assigned yet.")
            continue

        for index, task in enumerate(tasks):
            col1, col2 = st.columns([5, 1])
            task_line = format_task_line(task)

            with col1:
                if task.completed:
                    st.success(f"✓ {task_line}")
                elif hasattr(task, 'is_overdue') and task.is_overdue(current_time):
                    st.warning(f"Overdue: {task_line}")
                else:
                    st.info(f"○ {task_line}")

            with col2:
                if not task.completed:
                    button_key = f"done_{pet.name}_{task.description}_{task.scheduled_time}_{index}"
                    if st.button("Done", key=button_key):
                        scheduler.handle_task_completion(task)
                        st.rerun()

    pending_count = len(scheduler.get_pending_tasks())
    completed_count = len(scheduler.get_completed_tasks())

    st.divider()
    st.write(f"Pending tasks: {pending_count}")
    st.write(f"Completed tasks: {completed_count}")

    show_conflicts(owner, scheduler)


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("Smart pet care scheduling powered by your backend system.")

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

if "active_pet_name" not in st.session_state:
    st.session_state.active_pet_name = ""

owner: Owner = st.session_state.owner

st.subheader("Owner Setup")
owner_name_input = st.text_input("Owner name", value=owner.name)
if owner_name_input.strip():
    owner.name = owner_name_input.strip()

st.divider()
st.subheader("Pet and Task Management")

pet_name_input = st.text_input("Pet name", value=st.session_state.active_pet_name or "Mochi")
species_input = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Use / Create Pet"):
    if not pet_name_input.strip():
        st.error("Please enter a pet name.")
    else:
        pet = get_or_create_pet(owner, pet_name_input.strip(), species_input)
        st.session_state.active_pet_name = pet.name
        st.success(f"Now managing: {pet.name}")

active_pet = None
if st.session_state.active_pet_name:
    try:
        active_pet = owner.get_pet(st.session_state.active_pet_name)
    except KeyError:
        active_pet = None

task_col1, task_col2 = st.columns(2)
with task_col1:
    task_description = st.text_input("Task description", value="Morning walk")
with task_col2:
    task_time = st.text_input("Task time (HH:MM)", value=datetime.now().strftime("%H:%M"))

task_frequency = st.selectbox("Frequency", ["once", "daily", "weekly"], index=1)

if st.button("Add Task"):
    if active_pet is None:
        st.error("Select or create a pet first.")
    elif not task_description.strip():
        st.error("Task description cannot be empty.")
    else:
        new_task = Task(
            description=task_description.strip(),
            scheduled_time=task_time.strip(),
            frequency=task_frequency,
        )
        
        scheduler = Scheduler(owner)
        conflict = scheduler.check_for_conflict(new_task)
        
        if conflict:
            st.error(
                f"⚠️ Conflict detected at {conflict['time']}: "
                f"'{conflict['conflicting_task']}' for {conflict['conflicting_pet']} is already scheduled then."
            )
        else:
            added = active_pet.add_task(new_task)
            if added:
                st.success("Task added successfully.")
            else:
                st.warning("That task already exists for this pet.")

st.divider()
render_schedule(owner)