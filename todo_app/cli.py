"""
CLI - Command-line interface for Todo App.

This module provides the interactive menu system for user interaction.
"""

import sys
from todo_app.manager import TaskManager


class CLI:
    """
    Interactive command-line interface for task management.

    Provides numbered menu for CRUD operations on tasks.
    """

    def __init__(self):
        """Initialize CLI with TaskManager instance."""
        self.manager = TaskManager()

        # Detect terminal capability for ANSI colors
        if sys.stdout.isatty():
            self.GREEN = '\033[92m'
            self.YELLOW = '\033[93m'
            self.RESET = '\033[0m'
        else:
            self.GREEN = self.YELLOW = self.RESET = ''

    def display_menu(self):
        """Display main menu with numbered options."""
        print("\n" + "=" * 30)
        print("=== Todo List Manager ===")
        print("=" * 30)
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Mark Complete")
        print("5. Delete Task")
        print("6. Exit")
        print("=" * 30)

    def view_tasks(self):
        """Display all tasks with formatting."""
        tasks = self.manager.get_all_tasks()

        if not tasks:
            print(f"\n{self.YELLOW}No tasks found. Add a task to get started!{self.RESET}")
            return

        print("\nYour Tasks:")
        for task in tasks:
            print(task)
        print(f"\nLegend: [ ] = Incomplete, [X] = Complete")

    def add_task(self):
        """Prompt user and add new task."""
        try:
            description = input("\nEnter task description: ").strip()
            task = self.manager.add_task(description)
            print(f"{self.GREEN}✓ Task added successfully (ID: {task.id}){self.RESET}")
        except ValueError as e:
            print(f"{self.YELLOW}⚠ {e}{self.RESET}")

    def update_task(self):
        """Prompt user and update existing task."""
        try:
            # Get task ID
            task_id_str = input("\nEnter task ID to update: ").strip()
            if not task_id_str:
                print(f"{self.YELLOW}⚠ Task ID cannot be empty{self.RESET}")
                return

            try:
                task_id = int(task_id_str)
            except ValueError:
                print(f"{self.YELLOW}⚠ Task ID must be a number{self.RESET}")
                return

            # Get existing task to show current description
            existing_task = self.manager.get_task_by_id(task_id)
            if existing_task is None:
                print(f"{self.YELLOW}⚠ Task #{task_id} not found{self.RESET}")
                return

            # Show current description
            print(f"\nCurrent description: {existing_task.description}")

            # Get new description
            new_description = input("Enter new description: ").strip()

            # Update task
            task = self.manager.update_task(task_id, new_description)
            print(f"{self.GREEN}✓ Task #{task.id} updated successfully{self.RESET}")

            # Automatically display updated task list
            print(f"\n{self.GREEN}Updated task list:{self.RESET}")
            self.view_tasks()
        except ValueError as e:
            print(f"{self.YELLOW}⚠ {e}{self.RESET}")

    def mark_task_complete(self):
        """Prompt user and mark task as complete."""
        try:
            # Get task ID
            task_id_str = input("\nEnter task ID to mark complete: ").strip()
            if not task_id_str:
                print(f"{self.YELLOW}⚠ Task ID cannot be empty{self.RESET}")
                return

            try:
                task_id = int(task_id_str)
            except ValueError:
                print(f"{self.YELLOW}⚠ Task ID must be a number{self.RESET}")
                return

            # Check if task exists
            existing_task = self.manager.get_task_by_id(task_id)
            if existing_task is None:
                print(f"{self.YELLOW}⚠ Task #{task_id} not found{self.RESET}")
                return

            # Mark complete
            task = self.manager.mark_complete(task_id)

            if task.completed:
                print(f"{self.GREEN}✓ Task #{task.id} marked as complete{self.RESET}")

                # Automatically display updated task list
                print(f"\n{self.GREEN}Updated task list:{self.RESET}")
                self.view_tasks()
        except ValueError as e:
            print(f"{self.YELLOW}⚠ {e}{self.RESET}")

    def delete_task(self):
        """Prompt user and delete task."""
        try:
            # Get task ID
            task_id_str = input("\nEnter task ID to delete: ").strip()
            if not task_id_str:
                print(f"{self.YELLOW}⚠ Task ID cannot be empty{self.RESET}")
                return

            try:
                task_id = int(task_id_str)
            except ValueError:
                print(f"{self.YELLOW}⚠ Task ID must be a number{self.RESET}")
                return

            # Delete task
            success = self.manager.delete_task(task_id)

            if success:
                print(f"{self.GREEN}✓ Task #{task_id} deleted successfully{self.RESET}")

                # Automatically display updated task list
                print(f"\n{self.GREEN}Updated task list:{self.RESET}")
                self.view_tasks()
            else:
                print(f"{self.YELLOW}⚠ Task #{task_id} not found{self.RESET}")
        except Exception as e:
            print(f"{self.YELLOW}⚠ Error: {e}{self.RESET}")

    def run(self):
        """Main application loop - display menu and handle user choices."""
        print(f"\n{self.GREEN}Welcome to Todo List Manager!{self.RESET}")

        while True:
            self.display_menu()

            try:
                choice = input("\nEnter choice (1-6): ").strip()

                if choice == '1':
                    self.add_task()
                elif choice == '2':
                    self.view_tasks()
                elif choice == '3':
                    self.update_task()
                elif choice == '4':
                    self.mark_task_complete()
                elif choice == '5':
                    self.delete_task()
                elif choice == '6':
                    print(f"\n{self.GREEN}Goodbye!{self.RESET}\n")
                    break
                else:
                    print(f"{self.YELLOW}⚠ Invalid choice. Please enter 1-6{self.RESET}")

            except KeyboardInterrupt:
                print(f"\n\n{self.GREEN}Goodbye!{self.RESET}\n")
                break
            except Exception as e:
                print(f"{self.YELLOW}⚠ An error occurred: {e}{self.RESET}")
