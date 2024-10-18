import os
import time
import json
from datetime import datetime
from rich.box import DOUBLE, HEAVY, HORIZONTALS, SQUARE_DOUBLE_HEAD, Box
from rich.columns import Columns
from rich.console import Console
from rich.table import Table
from rich.panel import Panel


JSON_FILE = "todo_tasks.json"

def load_tasks():
    try:
        with open(JSON_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open(JSON_FILE, 'w') as file:
        json.dump(tasks, file, indent=2)

def add_task(tasks):
    task_num = len(tasks) + 1
    task = input("Task description: ")
    due_date = input("Due date (DD MM YYYY): ")
    new_task = {
        "task_num": task_num,
        "task": task,
        "task_status": False,
        "task_due": due_date
    }
    tasks.append(new_task)
    save_tasks(tasks)
    #print("Task added.")

def list_tasks(tasks):
    console = Console()

    table = Table(
        show_header=True,
        header_style="bold red",
        show_lines=True,
        box = DOUBLE,

        )
    # Başlık sütunlarını ekleyelim
    table.add_column("")
    table.add_column("Task", style="magenta",width=20)
    table.add_column("Status", style="green", justify="center",width=7)
    table.add_column("Due Date", style="yellow", justify="center",width=10)


    for task in tasks:
        status = "✅" if task["task_status"] else "❌"
        table.add_row(
            str(task["task_num"]),
            task["task"],
            status,
            task["task_due"]
        )

    #console.print(table)
    return table

def edit_task(tasks):


    list_tasks(tasks)
    try:
        task_num = int(input("Enter the task: "))
    except ValueError:
        print("Invalid value")
        return

    selected_task = None
    selected_index = None
    for index, task in enumerate(tasks):
        if task.get("task_num") == task_num:
            selected_task = task
            selected_index = index
            break

    if selected_task is None:
        print("Task not found.")
        return

    print("1 - Set as completed")
    print("2 - Set as not completed")
    print("3 - Set as important")
    print("4 - Delete the task")
    action = input("Action: ")



    if action == "1":
        selected_task["task_status"] = True
        print("Task marked as completed.")

    elif action == "2":
        selected_task["task_status"] = False
        print("Task marked as not completed.")

    elif action == "3":
        important_task = "❗" + selected_task["task"] + "❗"
        selected_task["task"] = str(important_task)


    elif action == "4":
        del tasks[selected_index]
        for i, remaining_task in enumerate(tasks[selected_index:], start=selected_index+1):
            remaining_task["task_num"] = i
        print("Task deleted.")
    else:
        print("Invalid action.")
        return

    save_tasks(tasks)



def clear_screen():
    # for windows
    if os.name == 'nt':
        os.system('cls')
    # for Unix/Linux/macOS
    else:
        os.system('clear')

def main():
    tasks = load_tasks()
    while True:
        clear_screen()

        console = Console()
        table = Table(
            show_header=True,
            header_style="bold red",
            show_lines=True,
            box = DOUBLE,
            )

        table.add_column(" ", style="dim", width=1)
        table.add_column("TO-DO ACTIONS", width=13)


        table.add_row(
            "1",
            "Add Task"
        )
        table.add_row(
            "2",
            "Edit Task"
        )
        table.add_row(
            "3",
            "Quit"
        )


        task_table = list_tasks(tasks)

        columns = Columns([Panel(task_table), Panel(table)])
        console.print(columns)

        choice = input("Enter your choice: ")

        if choice == '1':
            add_task(tasks)
            time.sleep(0.5)
            input("Press Enter to continue...")

        elif choice == '2':
            edit_task(tasks)
            time.sleep(0.5)
            input("Press Enter to continue...")

        elif choice == '3':
            print("Exiting the application...")
            break

        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
