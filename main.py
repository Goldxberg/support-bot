#!/usr/bin/env python3
"""
support-bot: Bilingual (Hebrew/English) support bot with conversation memory.
Runs an interactive chat in the terminal using Claude AI.
"""

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.markdown import Markdown
from rich import box

from bot import get_response
from memory import new_session, load_session, save_message, list_sessions

console = Console()


def display_welcome():
    """Show the welcome banner."""
    console.print(Panel(
        "[bold]Bilingual Support Bot[/bold]\n"
        "English & Hebrew | עברית ואנגלית\n\n"
        "[dim]Type your question in either language.\n"
        "Commands: /history, /sessions, /quit[/dim]",
        title="[bold blue]Support Bot[/bold blue]",
        border_style="blue",
        padding=(1, 2),
    ))


def display_sessions():
    """Show past conversation sessions."""
    sessions = list_sessions()
    if not sessions:
        console.print("[dim]No past sessions found.[/dim]")
        return

    table = Table(
        title="Past Sessions",
        box=box.ROUNDED,
        header_style="bold",
    )
    table.add_column("Session ID", style="cyan")
    table.add_column("Date", style="dim")
    table.add_column("Messages", justify="center")
    table.add_column("Preview", style="dim")

    for s in sessions[:10]:
        table.add_row(s["id"], s["created"][:16], str(s["messages"]), s["preview"])

    console.print(table)
    console.print("[dim]Resume a session: python main.py --resume SESSION_ID[/dim]\n")


def display_history(session_data):
    """Show conversation history for current session."""
    messages = session_data.get("messages", [])
    if not messages:
        console.print("[dim]No messages yet.[/dim]")
        return

    console.print(f"\n[bold]Session: {session_data['session_id']}[/bold]")
    console.print(f"[dim]Started: {session_data['created_at'][:16]}[/dim]\n")

    for msg in messages:
        if msg["role"] == "user":
            console.print(f"[bold cyan]You:[/bold cyan] {msg['content']}")
        else:
            console.print(Panel(
                Markdown(msg["content"]),
                border_style="blue",
                padding=(0, 1),
            ))
    console.print()


def chat_loop(session_id, existing_messages=None):
    """Main interactive chat loop."""
    messages = existing_messages or []

    display_welcome()

    if messages:
        console.print(f"[dim]Resumed session {session_id} with {len(messages)} messages.[/dim]\n")

    while True:
        try:
            user_input = console.input("[bold cyan]You → [/bold cyan]")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Goodbye! להתראות![/dim]")
            break

        user_input = user_input.strip()
        if not user_input:
            continue

        # Handle commands
        if user_input.lower() == "/quit":
            console.print("[dim]Goodbye! להתראות![/dim]")
            break
        elif user_input.lower() == "/sessions":
            display_sessions()
            continue
        elif user_input.lower() == "/history":
            session_data = load_session(session_id)
            display_history(session_data)
            continue

        # Save user message
        save_message(session_id, "user", user_input)
        messages.append({"role": "user", "content": user_input})

        # Get bot response
        with console.status("[bold blue]Thinking...[/bold blue]"):
            try:
                response = get_response(messages)
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
                continue

        # Save and display response
        save_message(session_id, "assistant", response)
        messages.append({"role": "assistant", "content": response})

        console.print()
        console.print(Panel(
            Markdown(response),
            border_style="blue",
            padding=(0, 1),
        ))
        console.print()


@click.command()
@click.option("--resume", "-r", default=None, help="Resume a past session by ID.")
def main(resume):
    """Start the bilingual support bot."""
    if resume:
        session_data = load_session(resume)
        if not session_data:
            console.print(f"[red]Session '{resume}' not found.[/red]")
            display_sessions()
            return
        messages = [
            {"role": m["role"], "content": m["content"]}
            for m in session_data["messages"]
        ]
        chat_loop(resume, messages)
    else:
        session_id, _ = new_session()
        chat_loop(session_id)


if __name__ == "__main__":
    main()
