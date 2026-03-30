"""
Unit tests for PawPal+ System (pawpal_system.py)

Tests core functionality of Task, Pet, Owner, and Scheduler classes.
"""

import sys
from pathlib import Path

import pytest

# Add parent directory to path to import pawpal_system
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from pawpal_system import Task, Pet, Owner, Scheduler


class TestTask:
    """Test suite for Task class."""
    
    def test_task_mark_complete(self):
        """Test that mark_complete() sets completed to True."""
        task = Task("Feed", "09:00", frequency="daily", completed=False)
        assert task.completed is False
        
        task.mark_complete()
        assert task.completed is True
    
    def test_task_mark_incomplete(self):
        """Test that mark_incomplete() sets completed to False."""
        task = Task("Feed", "09:00", frequency="daily", completed=True)
        assert task.completed is True
        
        task.mark_incomplete()
        assert task.completed is False
    
    def test_task_is_due(self):
        """Test that is_due() correctly identifies due tasks."""
        task = Task("Walk", "10:00", frequency="daily")
        
        # Task is not due before scheduled time
        assert task.is_due("09:00") is False
        
        # Task is due at exactly scheduled time
        assert task.is_due("10:00") is True
        
        # Task is due after scheduled time
        assert task.is_due("11:00") is True
    
    def test_task_repr(self):
        """Test that __repr__ returns a readable string."""
        task = Task("Grooming", "14:00", frequency="weekly", completed=True)
        repr_str = repr(task)
        
        assert "Task" in repr_str
        assert "Grooming" in repr_str
        assert "14:00" in repr_str
        assert "weekly" in repr_str


class TestPet:
    """Test suite for Pet class."""
    
    def test_pet_add_task(self):
        """Test that add_task() adds a task to a pet's task list."""
        pet = Pet("Buddy", "Dog")
        task = Task("Walk", "08:00", frequency="daily")
        
        assert len(pet.get_tasks()) == 0
        
        pet.add_task(task)
        
        assert len(pet.get_tasks()) == 1
        assert task in pet.get_tasks()
    
    def test_pet_add_duplicate_task(self):
        """Test that duplicate tasks are not added."""
        pet = Pet("Luna", "Cat")
        task = Task("Feed", "09:00", frequency="daily")
        
        pet.add_task(task)
        pet.add_task(task)  # Add same task again
        
        assert len(pet.get_tasks()) == 1
    
    def test_pet_remove_task(self):
        """Test that remove_task() removes a task from the pet's list."""
        pet = Pet("Max", "Dog")
        task1 = Task("Walk", "08:00", frequency="daily")
        task2 = Task("Feed", "12:00", frequency="daily")
        
        pet.add_task(task1)
        pet.add_task(task2)
        assert len(pet.get_tasks()) == 2
        
        pet.remove_task(task1)
        
        assert len(pet.get_tasks()) == 1
        assert task1 not in pet.get_tasks()
        assert task2 in pet.get_tasks()
    
    def test_pet_get_due_tasks(self):
        """Test that get_due_tasks() returns only tasks due at a given time."""
        pet = Pet("Buddy", "Dog")
        task1 = Task("Morning Walk", "08:00", frequency="daily")
        task2 = Task("Feed", "12:00", frequency="daily")
        task3 = Task("Evening Walk", "18:00", frequency="daily")
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        
        # At 13:00, morning walk and feed should be due
        due_tasks = pet.get_due_tasks("13:00")
        assert len(due_tasks) == 2
        assert task1 in due_tasks
        assert task2 in due_tasks
        assert task3 not in due_tasks
        
        # At 19:00, all tasks should be due
        due_tasks = pet.get_due_tasks("19:00")
        assert len(due_tasks) == 3
    
    def test_pet_repr(self):
        """Test that __repr__ returns a readable string."""
        pet = Pet("Fluffy", "Cat")
        repr_str = repr(pet)
        
        assert "Pet" in repr_str
        assert "Fluffy" in repr_str
        assert "Cat" in repr_str


class TestOwner:
    """Test suite for Owner class."""
    
    def test_owner_add_pet(self):
        """Test that add_pet() adds a pet to the owner's collection."""
        owner = Owner("Alice")
        pet = Pet("Buddy", "Dog")
        
        owner.add_pet(pet)
        
        assert "Buddy" in owner.pets
        assert owner.pets["Buddy"] == pet
    
    def test_owner_add_duplicate_pet(self):
        """Test that adding a pet with duplicate name raises ValueError."""
        owner = Owner("Bob")
        pet1 = Pet("Max", "Dog")
        pet2 = Pet("Max", "Cat")
        
        owner.add_pet(pet1)
        
        with pytest.raises(ValueError):
            owner.add_pet(pet2)
    
    def test_owner_get_pet(self):
        """Test that get_pet() retrieves a pet by name."""
        owner = Owner("Carol")
        pet = Pet("Luna", "Cat")
        
        owner.add_pet(pet)
        retrieved_pet = owner.get_pet("Luna")
        
        assert retrieved_pet == pet
    
    def test_owner_get_nonexistent_pet(self):
        """Test that get_pet() raises KeyError for nonexistent pet."""
        owner = Owner("Dave")
        
        with pytest.raises(KeyError):
            owner.get_pet("Nonexistent")
    
    def test_owner_remove_pet(self):
        """Test that remove_pet() removes a pet from collection."""
        owner = Owner("Eve")
        pet = Pet("Buddy", "Dog")
        
        owner.add_pet(pet)
        assert "Buddy" in owner.pets
        
        owner.remove_pet("Buddy")
        assert "Buddy" not in owner.pets
    
    def test_owner_remove_nonexistent_pet(self):
        """Test that remove_pet() raises KeyError for nonexistent pet."""
        owner = Owner("Frank")
        
        with pytest.raises(KeyError):
            owner.remove_pet("Nonexistent")
    
    def test_owner_get_all_tasks(self):
        """Test that get_all_tasks() retrieves tasks from all pets."""
        owner = Owner("Grace")
        pet1 = Pet("Buddy", "Dog")
        pet2 = Pet("Luna", "Cat")
        
        task1 = Task("Walk", "08:00", frequency="daily")
        task2 = Task("Feed", "09:00", frequency="daily")
        task3 = Task("Play", "15:00", frequency="daily")
        
        pet1.add_task(task1)
        pet1.add_task(task2)
        pet2.add_task(task3)
        
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        
        all_tasks = owner.get_all_tasks()
        
        assert len(all_tasks) == 3
        assert task1 in all_tasks
        assert task2 in all_tasks
        assert task3 in all_tasks
    
    def test_owner_get_all_due_tasks(self):
        """Test that get_all_due_tasks() retrieves due tasks from all pets."""
        owner = Owner("Henry")
        pet1 = Pet("Max", "Dog")
        pet2 = Pet("Whiskers", "Cat")
        
        task1 = Task("Morning Walk", "08:00", frequency="daily")
        task2 = Task("Feed", "12:00", frequency="daily")
        task3 = Task("Play", "15:00", frequency="daily")
        
        pet1.add_task(task1)
        pet1.add_task(task2)
        pet2.add_task(task3)
        
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        
        due_tasks = owner.get_all_due_tasks("13:00")
        
        assert len(due_tasks) == 2
        assert task1 in due_tasks
        assert task2 in due_tasks
        assert task3 not in due_tasks


class TestScheduler:
    """Test suite for Scheduler class."""
    
    def test_scheduler_initialization(self):
        """Test that Scheduler initializes with an Owner."""
        owner = Owner("Iris")
        scheduler = Scheduler(owner)
        
        assert scheduler.owner == owner
    
    def test_scheduler_get_daily_schedule(self):
        """Test that get_daily_schedule() returns due tasks grouped by pet."""
        owner = Owner("Jack")
        pet = Pet("Buddy", "Dog")
        
        task1 = Task("Walk", "08:00", frequency="daily")
        task2 = Task("Feed", "12:00", frequency="daily")
        task3 = Task("Play", "18:00", frequency="daily")
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        
        owner.add_pet(pet)
        scheduler = Scheduler(owner)
        
        schedule = scheduler.get_daily_schedule("13:00")
        
        assert "Buddy" in schedule
        assert len(schedule["Buddy"]) == 2
        assert task1 in schedule["Buddy"]
        assert task2 in schedule["Buddy"]
    
    def test_scheduler_get_pending_tasks(self):
        """Test that get_pending_tasks() returns incomplete tasks."""
        owner = Owner("Kate")
        pet = Pet("Luna", "Cat")
        
        task1 = Task("Feed", "09:00", frequency="daily", completed=False)
        task2 = Task("Play", "15:00", frequency="daily", completed=True)
        task3 = Task("Groom", "17:00", frequency="weekly", completed=False)
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        
        owner.add_pet(pet)
        scheduler = Scheduler(owner)
        
        pending = scheduler.get_pending_tasks()
        
        assert len(pending) == 2
        assert task1 in pending
        assert task3 in pending
        assert task2 not in pending
    
    def test_scheduler_get_completed_tasks(self):
        """Test that get_completed_tasks() returns completed tasks."""
        owner = Owner("Liam")
        pet = Pet("Max", "Dog")
        
        task1 = Task("Walk", "08:00", frequency="daily", completed=True)
        task2 = Task("Feed", "12:00", frequency="daily", completed=False)
        task3 = Task("Train", "16:00", frequency="daily", completed=True)
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)
        
        owner.add_pet(pet)
        scheduler = Scheduler(owner)
        
        completed = scheduler.get_completed_tasks()
        
        assert len(completed) == 2
        assert task1 in completed
        assert task3 in completed
        assert task2 not in completed
    
    def test_scheduler_get_tasks_grouped_by_pet(self):
        """Test that get_tasks_grouped_by_pet() organizes tasks by pet."""
        owner = Owner("Mia")
        pet1 = Pet("Buddy", "Dog")
        pet2 = Pet("Luna", "Cat")
        
        task1 = Task("Walk", "08:00", frequency="daily")
        task2 = Task("Feed", "09:00", frequency="daily")
        task3 = Task("Play", "15:00", frequency="daily")
        
        pet1.add_task(task1)
        pet1.add_task(task2)
        pet2.add_task(task3)
        
        owner.add_pet(pet1)
        owner.add_pet(pet2)
        scheduler = Scheduler(owner)
        
        grouped = scheduler.get_tasks_grouped_by_pet()
        
        assert "Buddy" in grouped
        assert "Luna" in grouped
        assert len(grouped["Buddy"]) == 2
        assert len(grouped["Luna"]) == 1
        assert task1 in grouped["Buddy"]
        assert task2 in grouped["Buddy"]
        assert task3 in grouped["Luna"]
