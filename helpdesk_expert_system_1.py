
# ================================================================
#   EXPERT SYSTEM — HELP DESK MANAGEMENT
#   Type   : Rule-Based Expert System
#   Author : Ubed
# ================================================================

import datetime

# ── KNOWLEDGE BASE ───────────────────────────────────────────────
# Rules: each rule has conditions (keywords) and a solution

KNOWLEDGE_BASE = [
    {
        "issue_type": "Internet / Network",
        "keywords": ["internet", "wifi", "network", "no connection", "disconnected", "slow internet", "router"],
        "priority": "High",
        "solution": [
            "1. Restart your router and modem.",
            "2. Check if other devices are also affected.",
            "3. Run: ipconfig /release and ipconfig /renew (Windows).",
            "4. Disable/enable the network adapter.",
            "5. Contact ISP if issue persists.",
        ],
        "escalate_to": "Network Team",
        "est_time": "30 minutes",
    },
    {
        "issue_type": "Password / Login",
        "keywords": ["password", "login", "locked", "can't sign in", "forgot", "access denied", "credentials"],
        "priority": "High",
        "solution": [
            "1. Use 'Forgot Password' link on the login page.",
            "2. Check CAPS LOCK is off.",
            "3. Clear browser cache and cookies.",
            "4. Try incognito/private mode.",
            "5. Contact admin if account is locked.",
        ],
        "escalate_to": "IT Security Team",
        "est_time": "15 minutes",
    },
    {
        "issue_type": "Software / Application",
        "keywords": ["software", "app", "application", "crash", "not opening", "install", "error", "freeze", "not responding"],
        "priority": "Medium",
        "solution": [
            "1. Restart the application.",
            "2. Check for pending software updates.",
            "3. Restart your computer.",
            "4. Uninstall and reinstall the software.",
            "5. Check error logs for specific error codes.",
        ],
        "escalate_to": "Software Support Team",
        "est_time": "45 minutes",
    },
    {
        "issue_type": "Hardware / Device",
        "keywords": ["hardware", "printer", "keyboard", "mouse", "monitor", "screen", "device", "usb", "not detected", "blue screen"],
        "priority": "Medium",
        "solution": [
            "1. Check all cable connections.",
            "2. Restart the device.",
            "3. Try a different USB port.",
            "4. Update or reinstall device drivers.",
            "5. Test the device on another computer.",
        ],
        "escalate_to": "Hardware Support Team",
        "est_time": "1 hour",
    },
    {
        "issue_type": "Email",
        "keywords": ["email", "mail", "outlook", "gmail", "inbox", "send", "receive", "attachment", "spam"],
        "priority": "Medium",
        "solution": [
            "1. Check your internet connection.",
            "2. Verify email account settings (SMTP/IMAP).",
            "3. Check spam/junk folder.",
            "4. Clear email cache.",
            "5. Re-add your email account if needed.",
        ],
        "escalate_to": "Email Support Team",
        "est_time": "30 minutes",
    },
    {
        "issue_type": "Performance / Speed",
        "keywords": ["slow", "performance", "speed", "lag", "hanging", "overheating", "ram", "memory", "cpu"],
        "priority": "Low",
        "solution": [
            "1. Close unused background applications.",
            "2. Run Disk Cleanup and Defragmenter.",
            "3. Check for malware/virus.",
            "4. Upgrade RAM if consistently low.",
            "5. Restart the system daily.",
        ],
        "escalate_to": "IT Support Team",
        "est_time": "1 hour",
    },
    {
        "issue_type": "Virus / Security",
        "keywords": ["virus", "malware", "hack", "phishing", "suspicious", "ransomware", "security", "infected", "spam mail"],
        "priority": "Critical",
        "solution": [
            "1. IMMEDIATELY disconnect from the network.",
            "2. Do NOT open any more suspicious files.",
            "3. Run a full antivirus scan.",
            "4. Change all passwords from a clean device.",
            "5. Report to IT Security team immediately.",
        ],
        "escalate_to": "IT Security Team (URGENT)",
        "est_time": "Immediate",
    },
    {
        "issue_type": "VPN / Remote Access",
        "keywords": ["vpn", "remote", "work from home", "access", "tunnel", "connect remotely", "remote desktop"],
        "priority": "High",
        "solution": [
            "1. Check your internet connection first.",
            "2. Restart the VPN client.",
            "3. Verify your VPN credentials.",
            "4. Try a different VPN server.",
            "5. Reinstall the VPN client if needed.",
        ],
        "escalate_to": "Network Team",
        "est_time": "20 minutes",
    },
]

# ── TICKET STORAGE ───────────────────────────────────────────────
tickets = []
ticket_counter = 1000


# ── INFERENCE ENGINE ─────────────────────────────────────────────
def diagnose(description):
    """Match issue description to knowledge base rules."""
    desc = description.lower()
    for rule in KNOWLEDGE_BASE:
        for keyword in rule["keywords"]:
            if keyword in desc:
                return rule
    return None  # No match found


# ── TICKET MANAGEMENT ────────────────────────────────────────────
def create_ticket(name, description, matched_rule):
    global ticket_counter
    ticket_counter += 1
    ticket = {
        "id": f"TKT-{ticket_counter}",
        "name": name,
        "description": description,
        "issue_type": matched_rule["issue_type"] if matched_rule else "General",
        "priority": matched_rule["priority"] if matched_rule else "Low",
        "status": "Open",
        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "escalate_to": matched_rule["escalate_to"] if matched_rule else "IT Support",
    }
    tickets.append(ticket)
    return ticket


def view_tickets():
    if not tickets:
        print("\n  No tickets found.\n")
        return
    print("\n" + "=" * 62)
    print(f"  {'ID':<12} {'Name':<14} {'Issue':<20} {'Priority':<10} {'Status'}")
    print("  " + "-" * 60)
    for t in tickets:
        print(f"  {t['id']:<12} {t['name']:<14} {t['issue_type']:<20} {t['priority']:<10} {t['status']}")
    print("=" * 62 + "\n")


def update_ticket():
    tid = input("  Enter Ticket ID to update (e.g. TKT-1001): ").strip().upper()
    for t in tickets:
        if t["id"] == tid:
            print(f"  Current status: {t['status']}")
            print("  New status options: Open / In Progress / Resolved / Closed")
            new_status = input("  Enter new status: ").strip()
            if new_status in ["Open", "In Progress", "Resolved", "Closed"]:
                t["status"] = new_status
                print(f"  Ticket {tid} updated to '{new_status}'.\n")
            else:
                print("  Invalid status.\n")
            return
    print(f"  Ticket {tid} not found.\n")


# ── DISPLAY HELPERS ──────────────────────────────────────────────
def print_solution(rule, ticket):
    priority_icons = {
        "Critical": "[!!!]",
        "High":     "[!! ]",
        "Medium":   "[!  ]",
        "Low":      "[   ]",
    }
    icon = priority_icons.get(rule["priority"], "[ ]")

    print("\n" + "=" * 62)
    print(f"  HELP DESK EXPERT SYSTEM  —  Ubed")
    print("=" * 62)
    print(f"  Ticket ID    : {ticket['id']}")
    print(f"  Issue Type   : {rule['issue_type']}")
    print(f"  Priority     : {icon} {rule['priority']}")
    print(f"  Est. Time    : {rule['est_time']}")
    print(f"  Escalate To  : {rule['escalate_to']}")
    print("-" * 62)
    print("  RECOMMENDED SOLUTION:")
    for step in rule["solution"]:
        print(f"    {step}")
    print("-" * 62)
    print(f"  Ticket logged at {ticket['time']}")
    print("=" * 62 + "\n")


def print_banner():
    print("""
╔══════════════════════════════════════════════════════════╗
║        HELP DESK EXPERT SYSTEM                          ║
║        Author : Ubed                                   ║
╚══════════════════════════════════════════════════════════╝
  Supported issues:
   Internet | Password | Software | Hardware
   Email    | Virus    | VPN      | Performance
""")


def print_menu():
    print("  ┌─────────────────────────────────┐")
    print("  │  1. Report a New Issue          │")
    print("  │  2. View All Tickets            │")
    print("  │  3. Update Ticket Status        │")
    print("  │  4. Exit                        │")
    print("  └─────────────────────────────────┘")


# ── MAIN LOOP ────────────────────────────────────────────────────
def main():
    print_banner()

    while True:
        print_menu()
        choice = input("  Choose an option (1-4): ").strip()

        # ── Option 1: Report Issue ──
        if choice == "1":
            print("\n  -- New Issue Report --")
            name = input("  Your Name : ").strip() or "User"
            print("  Describe your issue (e.g. 'my wifi is not working'):")
            description = input("  Issue     : ").strip()

            if not description:
                print("  Please describe your issue.\n")
                continue

            # Inference engine diagnoses the issue
            matched_rule = diagnose(description)
            ticket = create_ticket(name, description, matched_rule)

            if matched_rule:
                print_solution(matched_rule, ticket)
            else:
                print(f"\n  Ticket {ticket['id']} created.")
                print("  No specific rule matched. Assigning to General IT Support.")
                print("  Please call: 1800-HELP-DESK or email: helpdesk@company.com\n")

        # ── Option 2: View Tickets ──
        elif choice == "2":
            view_tickets()

        # ── Option 3: Update Ticket ──
        elif choice == "3":
            update_ticket()

        # ── Option 4: Exit ──
        elif choice == "4":
            print(f"\n  Thank you for using the Help Desk System — Ubed")
            print(f"  Total tickets logged: {len(tickets)}\n")
            break

        else:
            print("  Invalid choice. Please enter 1, 2, 3, or 4.\n")


if __name__ == "__main__":
    main()
