"""
Task data model for Todo App.

This module defines the Task dataclass representing a todo item.
"""

from dataclasses import dataclass, field


@dataclass
class Task:
    """
    Represents a todo task with description and completion status.

    Attributes:
        id: Unique sequential identifier (auto-assigned by TaskManager)
        description: Task description text (1-500 characters)
        completed: Completion status flag (default: False)
        created_at: Creation order counter (auto-assigned by TaskManager)

    Raises:
        ValueError: If description is empty or exceeds 500 characters
    """
    id: int
    _description: str = field(default="", repr=False)
    completed: bool = False
    created_at: int = field(default=0, compare=False)

    def __post_init__(self):
        """Validate task data after initialization."""
        # If description was passed, validate and set it
        if hasattr(self, 'description'):
            self._description = self._validate_description(self.description)
        elif self._description:
            self._description = self._validate_description(self._description)

    @staticmethod
    def _validate_description(desc: str) -> str:
        """
        Validate and clean description text.

        Args:
            desc: Description text to validate

        Returns:
            Cleaned description text

        Raises:
            ValueError: If description is empty or exceeds 500 characters
        """
        # Strip whitespace
        if isinstance(desc, str):
            desc = desc.strip()

        # Validate description not empty
        if not desc:
            raise ValueError("Task description cannot be empty")

        # Validate description length
        if len(desc) > 500:
            raise ValueError("Task description cannot exceed 500 characters")

        return desc

    @property
    def description(self) -> str:
        """Get task description."""
        return self._description

    @description.setter
    def description(self, value: str):
        """Set task description with validation."""
        self._description = self._validate_description(value)

    def __str__(self) -> str:
        """Human-readable string representation for display."""
        status = "[X]" if self.completed else "[ ]"
        return f"[{self.id}] {status} {self.description}"
