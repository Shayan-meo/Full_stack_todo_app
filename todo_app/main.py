"""
Main entry point for Todo App.

This module starts the CLI application.
"""

from todo_app.cli import CLI


def main():
    """Launch the Todo App CLI."""
    cli = CLI()
    cli.run()


if __name__ == "__main__":
    main()
