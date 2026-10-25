from rich.console import Console
from rich.table import Table
from faker import Faker
from services.storage import load_cases, save_cases

console = Console()
fake = Faker()

def show_menu():
    console.print("\n[bold cyan]=== CYBERCRIME MANAGEMENT SYSTEM ===[/bold cyan]")
    console.print("1. View All Cases")
    console.print("2. Add New Case")
    console.print("3. Generate Fake Cases")
    console.print("4. Exit")

def display_cases(cases):
    if not cases:
        console.print("[yellow]No cases found.[/yellow]")
        return
    
    table = Table(title="Cybercrime Cases")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="magenta")
    table.add_column("Severity", style="green")

    for case in cases:
        table.add_row(str(case.get("id")), case.get("title"), case.get("severity"))

    console.print(table)

def add_case(cases):
    case_id = len(cases) + 1
    title = input("Enter case title: ")
    severity = input("Enter severity (Low/Medium/High): ")

    new_case = {
        "id": case_id,
        "title": title,
        "severity": severity
    }

    cases.append(new_case)
    if save_cases(cases):
        console.print("[bold green]Case added successfully![/bold green]")
    else:
        console.print("[bold red]Failed to save case.[/bold red]")

def generate_fake_cases(cases):
    severities = ["Low", "Medium", "High"]
    attacks = ["Phishing Attack", "Ransomware", "DDoS Attack", "Data Breach", "SQL Injection"]
    
    count = int(input("How many fake cases to generate? "))
    
    for _ in range(count):
        case_id = len(cases) + 1
        new_case = {
            "id": case_id,
            "title": fake.random_element(attacks),
            "severity": fake.random_element(severities)
        }
        cases.append(new_case)
    
    if save_cases(cases):
        console.print(f"[bold green]{count} fake cases generated successfully![/bold green]")
    else:
        console.print("[bold red]Failed to save fake cases.[/bold red]")

def main():
    cases = load_cases()
    
    while True:
        show_menu()
        choice = input("\nSelect an option (1-4): ")

        if choice == "1":
            display_cases(cases)
        elif choice == "2":
            add_case(cases)
        elif choice == "3":
            generate_fake_cases(cases)
        elif choice == "4":
            console.print("[bold yellow]Exiting system. Goodbye![/bold yellow]")
            break
        else:
            console.print("[red]Invalid choice, please try again.[/red]")

if __name__ == "__main__":
    main()