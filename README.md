# Job Application Tracker

A lightweight command-line tool to track job applications, follow-ups, and interview status — all stored locally in a CSV file. No database, no internet required.

## Features

- Add and track job applications with company, role, location, status, and notes
- Update application status as it progresses (Applied → Screen → Interview → Offer)
- Set follow-up reminders and get alerted when they're due
- View statistics: response rate, status breakdown, application trends
- All data stored locally in a simple CSV file you fully control

## Quick Start

```bash
# Clone the repo
git clone https://github.com/adityadhar-dev/job-tracker.git
cd job-tracker

# No dependencies needed — uses Python standard library only
python tracker.py
```

## Usage

```bash
python tracker.py add        # Add a new application
python tracker.py list       # View all applications
python tracker.py update     # Update status or notes
python tracker.py stats      # View statistics and response rate
python tracker.py followup   # Check what needs a follow-up today
```

## Example Output

```
ID    Company                Role                         Date         Status               Follow-up
------------------------------------------------------------------------------------------------------
1     ideaForge              Software Engineer            2025-06-01   Interview            2025-06-08
2     Garuda Aerospace       Python Developer             2025-06-02   Applied              2025-06-09
3     KPIT Technologies      Software Engineer            2025-06-03   Recruiter Screen     2025-06-05

Total: 3 application(s)
```

## Stats Example

```
--- Application Statistics ---
Total applications: 20

By status:
  Applied              12  ████████████  (60%)
  Interview             4  ████  (20%)
  Recruiter Screen      3  ███  (15%)
  Offer                 1  █  (5%)

Interview / response rate: 25%
→ Decent rate. Adding recruiter outreach can push this higher.
```

## Tech Stack

- Python 3.x
- Standard library only (`csv`, `os`, `sys`, `datetime`) — zero external dependencies

## Why I Built This

Tracking 20+ job applications across spreadsheets and browser tabs is chaos. This tool keeps everything in one place, reminds you to follow up, and shows you honest stats on your job search progress.

---

Built by Aditya Dhar | [LinkedIn](https://www.linkedin.com/in/aditya-dhar-777921242)
