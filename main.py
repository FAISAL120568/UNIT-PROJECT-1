import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from rich.console import Console
from rich.table import Table
from faker import Faker
from services.storage import load_cases, save_cases

console = Console()
fake = Faker()

SENDER_EMAIL = "faisalfawaz101@gmail.com"
APP_PASSWORD = "abcb djbp mldu gpgp"
RECEIVER_EMAIL = "faisalfawaz101@gmail.com"


USERS = {
    "admin": {"password": "123", "role": "Admin"},
    "analyst": {"password": "456", "role": "Analyst"}
}

def login():
    console.print("\n[bold cyan]=== SOC CONSOLE LOGIN ===[/bold cyan]")
    username = input("Enter username (admin / analyst): ").strip().lower()
    password = input("Enter password: ").strip()

    if username in USERS and USERS[username]["password"] == password:
        role = USERS[username]["role"]
        console.print(f"[bold green]Login successful! Welcome, {username.capitalize()} ({role})[/bold green]")
        return role
    else:
        console.print("[bold red]Invalid username or password. Access Denied.[/bold red]")
        return None

def send_email_alert(case_title, severity):
    if severity.strip().lower() != "high":
        return

    subject = f"🚨 [SOC ALERT] Critical Cyber Incident Detected: {case_title}"
    
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f4f4f7; margin: 0; padding: 20px; }}
            .container {{ max-width: 600px; background: #ffffff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); border-top: 5px solid #d9534f; }}
            .header {{ font-size: 22px; color: #d9534f; font-weight: bold; margin-bottom: 20px; }}
            .content {{ font-size: 16px; color: #333333; line-height: 1.6; }}
            .badge {{ display: inline-block; background-color: #d9534f; color: #ffffff; padding: 5px 12px; border-radius: 4px; font-weight: bold; font-size: 14px; }}
            .footer {{ margin-top: 30px; font-size: 12px; color: #888888; border-top: 1px solid #eeeeee; padding-top: 15px; text-align: center; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">🚨 Cybercrime SOC Alert System</div>
            <div class="content">
                <p>Hello Administrator,</p>
                <p>A new high-severity security incident has been logged in your system and requires immediate attention.</p>
                <hr style="border:0; border-top:1px solid #eee; margin:20px 0;">
                <p><strong>Incident Title:</strong> {case_title}</p>
                <p><strong>Severity Level:</strong> <span class="badge">{severity.strip().upper()}</span></p>
                <p><strong>Current Status:</strong> Open</p>
            </div>
            <div class="footer">
                <p>Generated automatically by Python Cyber SOC Console &bull; Do not reply to this email.</p>
            </div>
        </div>
    </body>
    </html>
    """

    msg = MIMEMultipart("alternative")
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        console.print("[bold green]📧 HTML Email alert sent successfully to Gmail![/bold green]")
    except Exception as e:
        console.print(f"[bold red]❌ Failed to send email alert: {e}[/bold red]")

def show_menu():
    console.print("\n[bold cyan]=== CYBERCRIME MANAGEMENT SYSTEM ===[/bold cyan]")
    console.print("1. View All Cases")
    console.print("2. Add New Case")
    console.print("3. Search Case")
    console.print("4. Update Case Status")
    console.print("5. Delete Case (Admin Only)")
    console.print("6. Generate Fake Cases (Admin Only)")
    console.print("7. SOC Dashboard & Statistics")
    console.print("8. Logout / Exit")

def display_cases(cases):
    if not cases:
        console.print("[yellow]No cases found.[/yellow]")
        return
    
    table = Table(title="Cybercrime Cases")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="magenta")
    table.add_column("Severity", style="green")
    table.add_column("Status", style="yellow")

    for case in cases:
        table.add_row(
            str(case.get("id")),
            case.get("title"),
            case.get("severity"),
            case.get("status", "Open")
        )

    console.print(table)

def show_dashboard(cases):
    total = len(cases)
    high = sum(1 for c in cases if c.get("severity", "").strip().lower() == "high")
    medium = sum(1 for c in cases if c.get("severity", "").strip().lower() == "medium")
    low = sum(1 for c in cases if c.get("severity", "").strip().lower() == "low")
    open_cases = sum(1 for c in cases if c.get("status", "Open").lower() == "open")
    closed_cases = sum(1 for c in cases if c.get("status", "").lower() == "closed")

    console.print("\n[bold magenta]📊 SOC ANALYTICS & DASHBOARD 📊[/bold magenta]")
    console.print(f"Total Incidents Recorded: [bold cyan]{total}[/bold cyan]")
    console.print(f"🔴 High Severity: [bold red]{high}[/bold red]")
    console.print(f"🟡 Medium Severity: [bold yellow]{medium}[/bold yellow]")
    console.print(f"🟢 Low Severity: [bold green]{low}[/bold green]")
    console.print(f"📂 Open Cases: [bold blue]{open_cases}[/bold blue]")
    console.print(f"🔒 Closed Cases: [bold white]{closed_cases}[/bold white]")

def add_case(cases):
    case_id = len(cases) + 1
    title = input("Enter case title: ")
    severity = input("Enter severity (Low/Medium/High): ")

    new_case = {
        "id": case_id,
        "title": title,
        "severity": severity,
        "status": "Open"
    }

    cases.append(new_case)
    if save_cases(cases):
        console.print("[bold green]Case added successfully![/bold green]")
        send_email_alert(title, severity)
    else:
        console.print("[bold red]Failed to save case.[/bold red]")

def search_case(cases):
    if not cases:
        console.print("[yellow]No cases available to search.[/yellow]")
        return
    
    query = input("Enter Case ID or Keyword to search: ").lower()
    results = [
        c for c in cases 
        if str(c.get("id")) == query or query in c.get("title", "").lower()
    ]
    
    if results:
        display_cases(results)
    else:
        console.print("[red]No matching cases found.[/red]")

def update_case_status(cases):
    if not cases:
        console.print("[yellow]No cases available to update.[/yellow]")
        return
    
    try:
        case_id = int(input("Enter Case ID to update: "))
    except ValueError:
        console.print("[red]Invalid Case ID.[/red]")
        return

    for case in cases:
        if case.get("id") == case_id:
            console.print(f"Current Status: [bold yellow]{case.get('status', 'Open')}[/bold yellow]")
            
            # قائمة الحالات المعتمدة
            valid_statuses = ["open", "under investigation", "closed"]
            
            while True:
                new_status = input("Enter new status (Open / Under Investigation / Closed): ").strip()
                
            
                if new_status.lower() in valid_statuses:
                    
                    case["status"] = new_status.title()
                    if save_cases(cases):
                        console.print("[bold green]Case status updated successfully![/bold green]")
                    else:
                        console.print("[bold red]Failed to save updated status.[/bold red]")
                    return
                else:
                    console.print("[bold red]❌ Invalid status! Please choose only from: Open, Under Investigation, Closed[/bold red]")

    console.print("[red]Case ID not found.[/red]")

def delete_case(cases, role):
    if role != "Admin":
        console.print("[bold red]Permission Denied: Only 'Admin' can delete cases.[/bold red]")
        return

    if not cases:
        console.print("[yellow]No cases available to delete.[/yellow]")
        return

    try:
        case_id = int(input("Enter Case ID to delete: "))
    except ValueError:
        console.print("[red]Invalid Case ID.[/red]")
        return

    for i, case in enumerate(cases):
        if case.get("id") == case_id:
            cases.pop(i)
            if save_cases(cases):
                console.print(f"[bold green]Case ID {case_id} deleted successfully![/bold green]")
            else:
                console.print("[bold red]Failed to update storage after deletion.[/bold red]")
            return

    console.print("[red]Case ID not found.[/red]")

def generate_fake_cases(cases, role):
    if role != "Admin":
        console.print("[bold red]Permission Denied: Only 'Admin' can generate fake cases.[/bold red]")
        return

    severities = ["Low", "Medium", "High"]
    attacks = ["Phishing Attack", "Ransomware", "DDoS Attack", "Data Breach", "SQL Injection"]
    statuses = ["Open", "Under Investigation", "Closed"]
    
    try:
        count = int(input("How many fake cases to generate? "))
    except ValueError:
        console.print("[red]Invalid count number.[/red]")
        return
    
    for _ in range(count):
        case_id = len(cases) + 1
        sev = fake.random_element(severities)
        title = fake.random_element(attacks)
        new_case = {
            "id": case_id,
            "title": title,
            "severity": sev,
            "status": fake.random_element(statuses)
        }
        cases.append(new_case)
        send_email_alt = send_email_alert(title, sev)
    
    if save_cases(cases):
        console.print(f"[bold green]{count} fake cases generated successfully![/bold green]")
    else:
        console.print("[bold red]Failed to save fake cases.[/bold red]")

def main():
    cases = load_cases()

    
    role = None
    while not role:
        role = login()

    while True:
        show_menu()
        choice = input("\nSelect an option (1-8): ").strip()

        if choice == "1":
            display_cases(cases)
        elif choice == "2":
            add_case(cases)
        elif choice == "3":
            search_case(cases)
        elif choice == "4":
            update_case_status(cases)
        elif choice == "5":
            delete_case(cases, role)
        elif choice == "6":
            generate_fake_cases(cases, role)
        elif choice == "7":
            show_dashboard(cases)
        elif choice == "8":
            console.print("[bold yellow]Exiting system. Goodbye![/bold yellow]")
            break
        else:
            console.print("[red]Invalid choice, please try again.[/red]")

if __name__ == "__main__":
    main()