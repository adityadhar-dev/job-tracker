"""
Job Application Tracker
-----------------------
A command-line tool to track your job applications,
follow-ups, and interview status — all stored locally in a CSV file.

Usage:
    python tracker.py add
    python tracker.py list
    python tracker.py update
    python tracker.py stats
    python tracker.py followup
"""

import csv
import os
import sys
from datetime import datetime, date

DATA_FILE = "applications.csv"
STATUSES = ["Applied", "Recruiter Screen", "Interview", "Offer", "Rejected", "Ghosted"]

HEADER = ["ID", "Company", "Role", "Location", "Date Applied", "Status", "Follow-up Date", "Notes", "Job URL"]


def load_applications():
    """Load all applications from CSV. Returns a list of dicts."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def save_applications(apps):
    """Save all applications back to CSV."""
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADER)
        writer.writeheader()
        writer.writerows(apps)


def next_id(apps):
    """Generate the next application ID."""
    if not apps:
        return 1
    return max(int(a["ID"]) for a in apps) + 1


def add_application():
    """Interactively add a new job application."""
    print("\n--- Add New Application ---")
    apps = load_applications()

    company = input("Company name: ").strip()
    role = input("Role / Job title: ").strip()
    location = input("Location (e.g. Noida / Remote): ").strip()
    date_applied = input(f"Date applied (YYYY-MM-DD) [today = {date.today()}]: ").strip()
    if not date_applied:
        date_applied = str(date.today())

    print("\nStatus options:")
    for i, s in enumerate(STATUSES, 1):
        print(f"  {i}. {s}")
    status_choice = input("Status [1]: ").strip()
    status = STATUSES[int(status_choice) - 1] if status_choice.isdigit() else "Applied"

    followup = input("Follow-up date (YYYY-MM-DD) [leave blank to skip]: ").strip()
    notes = input("Notes (recruiter name, referral, etc.): ").strip()
    url = input("Job URL [optional]: ").strip()

    new_app = {
        "ID": next_id(apps),
        "Company": company,
        "Role": role,
        "Location": location,
        "Date Applied": date_applied,
        "Status": status,
        "Follow-up Date": followup,
        "Notes": notes,
        "Job URL": url,
    }

    apps.append(new_app)
    save_applications(apps)
    print(f"\n✓ Application to {company} saved! (ID: {new_app['ID']})")


def list_applications(filter_status=None):
    """Display all applications in a formatted table."""
    apps = load_applications()

    if filter_status:
        apps = [a for a in apps if a["Status"].lower() == filter_status.lower()]

    if not apps:
        print("\nNo applications found.")
        return

    print(f"\n{'ID':<5} {'Company':<22} {'Role':<28} {'Date':<12} {'Status':<20} {'Follow-up':<12}")
    print("-" * 102)
    for a in apps:
        print(
            f"{a['ID']:<5} {a['Company'][:21]:<22} {a['Role'][:27]:<28} "
            f"{a['Date Applied']:<12} {a['Status']:<20} {a['Follow-up Date']:<12}"
        )
    print(f"\nTotal: {len(apps)} application(s)")


def update_status():
    """Update the status of an existing application."""
    list_applications()
    apps = load_applications()
    if not apps:
        return

    app_id = input("\nEnter application ID to update: ").strip()
    app = next((a for a in apps if str(a["ID"]) == app_id), None)
    if not app:
        print("Application not found.")
        return

    print(f"\nUpdating: {app['Company']} — {app['Role']}")
    print("\nStatus options:")
    for i, s in enumerate(STATUSES, 1):
        print(f"  {i}. {s}")
    choice = input(f"New status (current: {app['Status']}): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(STATUSES):
        app["Status"] = STATUSES[int(choice) - 1]

    followup = input(f"New follow-up date (current: {app['Follow-up Date']}) [leave blank to keep]: ").strip()
    if followup:
        app["Follow-up Date"] = followup

    notes = input(f"Add notes (current: {app['Notes']}) [leave blank to keep]: ").strip()
    if notes:
        app["Notes"] = notes

    save_applications(apps)
    print(f"\n✓ Application {app_id} updated.")


def show_stats():
    """Show summary statistics of all applications."""
    apps = load_applications()
    if not apps:
        print("\nNo applications to analyse.")
        return

    total = len(apps)
    status_counts = {}
    for a in apps:
        status_counts[a["Status"]] = status_counts.get(a["Status"], 0) + 1

    print("\n--- Application Statistics ---")
    print(f"Total applications: {total}")
    print("\nBy status:")
    for status, count in sorted(status_counts.items(), key=lambda x: -x[1]):
        bar = "█" * count
        pct = round((count / total) * 100)
        print(f"  {status:<20} {count:>3}  {bar}  ({pct}%)")

    interviews = status_counts.get("Interview", 0) + status_counts.get("Offer", 0)
    response_rate = round((interviews / total) * 100) if total > 0 else 0
    print(f"\nInterview / response rate: {response_rate}%")

    if response_rate < 10:
        print("  → Tip: Response rate is low. Try tailoring your resume more to each JD.")
    elif response_rate < 25:
        print("  → Tip: Decent rate. Adding recruiter outreach can push this higher.")
    else:
        print("  → Great response rate! Keep going.")


def check_followups():
    """Show applications that are due for a follow-up today or earlier."""
    apps = load_applications()
    today = date.today()
    due = []

    for a in apps:
        if a["Follow-up Date"]:
            try:
                fu_date = datetime.strptime(a["Follow-up Date"], "%Y-%m-%d").date()
                if fu_date <= today and a["Status"] not in ["Offer", "Rejected"]:
                    due.append((fu_date, a))
            except ValueError:
                pass

    if not due:
        print("\nNo follow-ups due today.")
        return

    print(f"\n--- Follow-ups Due ({len(due)}) ---")
    for fu_date, a in sorted(due):
        days_overdue = (today - fu_date).days
        tag = "TODAY" if days_overdue == 0 else f"{days_overdue}d overdue"
        print(f"  [{tag}] {a['Company']} — {a['Role']} (Applied: {a['Date Applied']})")


def main():
    commands = {
        "add": add_application,
        "list": list_applications,
        "update": update_status,
        "stats": show_stats,
        "followup": check_followups,
    }

    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        print("\nJob Application Tracker")
        print("Usage: python tracker.py <command>")
        print("\nCommands:")
        print("  add       Add a new job application")
        print("  list      List all applications")
        print("  update    Update status or notes on an application")
        print("  stats     Show summary statistics")
        print("  followup  Show applications due for follow-up")
        return

    commands[sys.argv[1]]()


if __name__ == "__main__":
    main()
