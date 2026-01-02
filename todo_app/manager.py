"""
TaskManager - Business logic for todo task management.

This module provides the service layer for CRUD operations on tasks.
"""

from typing import List, Optional
from todo_app.models import Task


class TaskManager:
    """
    Service layer providing CRUD operations for task management.

    Manages an in-memory collection of tasks with sequential ID generation
    and creation order tracking.
    """

    def __init__(self):
        """Initialize TaskManager with empty task list and counters."""
        self._tasks: List[Task] = []
        self._next_id: int = 1
        self._creation_counter: int = 1

    def add_task(self, description: str) -> Task:
        """
        Create a new task with given description.

        Args:
            description: Task description text (will be stripped)

        Returns:
            Created Task object with assigned ID

        Raises:
            ValueError: If description is empty or exceeds 500 characters
        """
        # Strip whitespace
        description = description.strip()

        # Validate (Task.__post_init__ will also validate, but we check here for clarity)
        if not description:
            raise ValueError("Task description cannot be empty")
        if len(description) > 500:
            raise ValueError("Task description cannot exceed 500 characters")

        # Create task with assigned ID and creation counter
        task = Task(
            id=self._next_id,
            _description=description,
            completed=False,
            created_at=self._creation_counter
        )

        # Append to list
        self._tasks.append(task)

        # Increment counters
        self._next_id += 1
        self._creation_counter += 1

        return task

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks ordered by creation time.

        Returns:
            List of all tasks (empty list if no tasks)
        """
        # Return tasks maintaining creation order (list maintains insertion order)
        return self._tasks.copy()

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Find and return task with specified ID.

        Args:
            task_id: Task identifier to search for

        Returns:
            Task object if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, description: str) -> Task:
        """
        Update description of existing task.

        Args:
            task_id: ID of task to update
            description: New task description

        Returns:
            Updated Task object

        Raises:
            ValueError: If task not found or description invalid
        """
        # Find task
        task = self.get_task_by_id(task_id)
        if task is None:
            raise ValueError(f"Task #{task_id} not found")

        # Validate new description
        description = description.strip()
        if not description:
            raise ValueError("Task description cannot be empty")
        if len(description) > 500:
            raise ValueError("Task description cannot exceed 500 characters")

        # Update description
        task.description = description
        return task

    def mark_complete(self, task_id: int) -> Task:
        """
        Mark task as complete.

        Args:
            task_id: ID of task to mark complete

        Returns:
            Task object with completed=True

        Raises:
            ValueError: If task not found
        """
        # Find task
        task = self.get_task_by_id(task_id)
        if task is None:
            raise ValueError(f"Task #{task_id} not found")

        # Set completed flag (idempotent - no error if already complete)
        task.completed = True
        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Remove task from collection.

        Args:
            task_id: ID of task to delete

        Returns:
            True if task was deleted, False if not found
        """
        # Find task
        task = self.get_task_by_id(task_id)
        if task is None:
            return False

        # Remove from list
        self._tasks.remove(task)
        return True
