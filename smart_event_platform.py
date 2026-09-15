# ==============================================================================
# SMART EVENT PLANNING AND RESOURCE COORDINATION PLATFORM - Milestone 2
# Plain Text Version (No Emojis or Special Unicode Symbols)
# ==============================================================================

from datetime import datetime


class Product:
    """Represents a distinct product or service offered by a vendor."""
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost
        self.is_assigned = False
        self.assigned_event_name = None

    def mark_as_used(self, event_name):
        self.is_assigned = True
        self.assigned_event_name = event_name


class Vendor:
    """Represents a vendor capable of selling multiple unique products."""
    def __init__(self, vendor_id, name):
        self.id = vendor_id
        self.name = name
        self.products = {}  # {product_name_lower: Product_object}

    def add_product(self, product_name, cost):
        key = product_name.strip().lower()
        # RULE: A single vendor cannot duplicate his products
        if key in self.products:
            return False, f"Vendor '{self.name}' already offers '{product_name}'. Duplicates not allowed."
        
        self.products[key] = Product(product_name.strip(), cost)
        return True, f"Product '{product_name}' successfully added to {self.name}'s catalog."


class Attendee:
    """Represents an attendee holding an issued ticket."""
    def __init__(self, reg_id, name, email, phone, ticket_id, tier="General"):
        self.reg_id = reg_id
        self.name = name
        self.email = email
        self.phone = phone
        self.ticket_id = ticket_id
        self.tier = tier
        self.status = "Registered"
        self.checkin_time = None


class Event:
    """Represents an event with capacity limit, attendees, and vendor contracts."""
    def __init__(self, event_id, name, max_capacity=30):
        self.id = event_id
        self.name = name
        self.max_capacity = max_capacity
        self.attendees = []
        self.contracts = []  # List of dicts: {"vendor_name", "product_name", "cost"}

    def is_full(self):
        return len(self.attendees) >= self.max_capacity


# ==============================================================================
# DATA STORAGE & SEED DATA
# ==============================================================================

events = [
    Event(1, "AI Workshop and Hackathon", max_capacity=3),
    Event(2, "National Tech Symposium", max_capacity=50)
]

vendors = []
ticket_counter = 1001


def seed_demo_data():
    """Seeds initial vendors with multiple distinct products."""
    v1 = Vendor(101, "Acoustic Pro Logistics")
    v1.add_product("Wireless Microphones", 45.0)
    v1.add_product("Line Array Speakers", 150.0)
    v1.add_product("Audio Mixer Console", 80.0)

    v2 = Vendor(102, "Gourmet Catering Co")
    v2.add_product("High-Tea Snacks", 120.0)
    v2.add_product("Buffet Lunch", 350.0)

    vendors.extend([v1, v2])


seed_demo_data()


# ==============================================================================
# HELPER LOOKUP FUNCTIONS
# ==============================================================================

def find_event(event_id):
    for e in events:
        if e.id == event_id:
            return e
    return None


def find_vendor(vendor_id):
    for v in vendors:
        if v.id == vendor_id:
            return v
    return None


def view_events_brief():
    print("\n--- Available Events ---")
    for e in events:
        slots_left = e.max_capacity - len(e.attendees)
        status = "SOLD OUT" if slots_left == 0 else f"{slots_left} seats remaining"
        print(f"[{e.id}] {e.name:<30} | Capacity: {e.max_capacity:<3} | Status: {status}")


# ==============================================================================
# 1. ATTENDEE REGISTRATION & TICKET GENERATION
# ==============================================================================

def register_attendee():
    global ticket_counter
    print("\n========== ATTENDEE REGISTRATION ==========")
    view_events_brief()

    try:
        eid = int(input("\nEnter Event ID to Register: "))
    except ValueError:
        print("ERROR: Invalid event ID.")
        return

    event = find_event(eid)
    if not event:
        print("ERROR: Event not found.")
        return

    # Check 1: Capacity Guard
    if event.is_full():
        print(f"REGISTRATION CLOSED: '{event.name}' is completely SOLD OUT! (Max: {event.max_capacity})")
        return

    reg_id = input("Registration ID (e.g. REG-01) : ").strip()
    name = input("Attendee Full Name             : ").strip()
    email = input("Email Address                  : ").strip().lower()
    phone = input("Phone Number                   : ").strip()

    if not name or not email:
        print("ERROR: Name and Email are mandatory.")
        return

    # Check 2: Duplicate Email Check
    for a in event.attendees:
        if a.email == email:
            print(f"REGISTRATION FAILED: Email '{email}' is already registered for this event.")
            return

    # Select Ticket Tier
    print("\nTicket Tiers: [1] General Access  |  [2] VIP Pass")
    tier_choice = input("Select Tier (1 or 2): ").strip()
    tier = "VIP" if tier_choice == "2" else "General"

    ticket = f"TKT-{ticket_counter}"
    ticket_counter += 1

    new_attendee = Attendee(reg_id, name, email, phone, ticket, tier)
    event.attendees.append(new_attendee)

    # Output plain text confirmation pass
    print("\n" + "=" * 50)
    print("REGISTRATION CONFIRMED - DIGITAL PASS")
    print("=" * 50)
    print(f"Event   : {event.name}")
    print(f"Name    : {name} ({tier} Pass)")
    print(f"Ticket  : {ticket}")
    print(f"Seats   : {len(event.attendees)}/{event.max_capacity} Filled")
    print("=" * 50)


def view_attendees():
    print("\n========== ATTENDEE DIRECTORY ==========")
    view_events_brief()
    try:
        eid = int(input("\nEnter Event ID: "))
    except ValueError:
        return

    event = find_event(eid)
    if not event:
        print("ERROR: Event not found.")
        return

    if not event.attendees:
        print(f"No attendees registered yet for '{event.name}'.")
        return

    print(f"\nGuest List for: {event.name}")
    print(f"{'Name':<22} {'Ticket ID':<12} {'Tier':<10} {'Status':<15}")
    print("-" * 60)
    for a in event.attendees:
        print(f"{a.name:<22} {a.ticket_id:<12} {a.tier:<10} {a.status:<15}")


# ==============================================================================
# 2. ANTI-FRAUD ATTENDANCE SCANNER
# ==============================================================================

def mark_attendance():
    print("\n========== GATE CHECK-IN SCANNER ==========")
    view_events_brief()
    try:
        eid = int(input("\nEnter Event ID: "))
    except ValueError:
        return

    event = find_event(eid)
    if not event:
        print("ERROR: Event not found.")
        return

    ticket = input("Scan / Enter Ticket ID (e.g. TKT-1001): ").strip().upper()
    attendee = None
    for a in event.attendees:
        if a.ticket_id.upper() == ticket:
            attendee = a
            break

    if not attendee:
        print(f"ERROR: Invalid Ticket '{ticket}' is not registered for {event.name}.")
        return

    # Anti-Fraud check: Prevent duplicate check-in
    if attendee.status == "Checked In":
        print("\n" + "!" * 55)
        print("FRAUD ALERT: DUPLICATE ENTRY ATTEMPT!")
        print(f"Ticket '{ticket}' ({attendee.name}) was ALREADY checked in at {attendee.checkin_time}.")
        print("Entry Denied.")
        print("!" * 55)
        return

    # Check-in confirmed
    attendee.status = "Checked In"
    attendee.checkin_time = datetime.now().strftime("%I:%M %p")
    print(f"SUCCESS: Check-In Successful! Welcome, {attendee.name} [{attendee.tier} Pass] ({attendee.checkin_time})")


# ==============================================================================
# 3. VENDOR & MULTI-PRODUCT CATALOG MANAGEMENT
# ==============================================================================

def add_vendor():
    print("\n========== REGISTER NEW VENDOR ==========")
    try:
        vid = int(input("Vendor ID (e.g. 103): "))
    except ValueError:
        print("ERROR: Invalid ID.")
        return

    if find_vendor(vid):
        print("ERROR: Vendor ID already exists.")
        return

    name = input("Vendor / Business Name: ").strip()
    if not name:
        print("ERROR: Vendor name required.")
        return

    vendors.append(Vendor(vid, name))
    print(f"SUCCESS: Vendor '{name}' registered successfully.")


def add_product_to_vendor():
    """Allows a vendor to add multiple unique products without duplicates."""
    print("\n========== ADD PRODUCT TO VENDOR CATALOG ==========")
    view_vendors_and_products()
    try:
        vid = int(input("\nSelect Vendor ID: "))
    except ValueError:
        return

    vendor = find_vendor(vid)
    if not vendor:
        print("ERROR: Vendor not found.")
        return

    product_name = input("Enter Product/Service Name: ").strip()
    try:
        cost = float(input("Enter Product Contract Price ($): "))
    except ValueError:
        print("ERROR: Invalid cost.")
        return

    # Enforces: Can sell multiple different products, but cannot duplicate products
    success, msg = vendor.add_product(product_name, cost)
    if success:
        print(f"SUCCESS: {msg}")
    else:
        print(f"REJECTED: {msg}")


def view_vendors_and_products():
    print("\n========== REGISTERED VENDORS AND CATALOGS ==========")
    if not vendors:
        print("No vendors registered.")
        return

    for v in vendors:
        print(f"\nVendor [{v.id}]: {v.name}")
        if not v.products:
            print("   (No products in catalog yet)")
        else:
            for p in v.products.values():
                availability = f"[IN USE - {p.assigned_event_name}]" if p.is_assigned else "[AVAILABLE]"
                print(f"   - {p.name:<25} | Cost: ${p.cost:<7.2f} | Status: {availability}")


# ==============================================================================
# 4. VENDOR PRODUCT ASSIGNMENT (Single-Use Constraint)
# ==============================================================================

def assign_vendor_product():
    """
    Ensures:
      - A vendor can supply multiple different products.
      - A single product CANNOT be duplicated and can only be used ONCE.
    """
    print("\n========== ASSIGN VENDOR PRODUCT TO EVENT ==========")
    view_events_brief()
    try:
        eid = int(input("\nSelect Event ID: "))
    except ValueError:
        return

    event = find_event(eid)
    if not event:
        print("ERROR: Event not found.")
        return

    view_vendors_and_products()
    try:
        vid = int(input("\nSelect Vendor ID: "))
    except ValueError:
        return

    vendor = find_vendor(vid)
    if not vendor:
        print("ERROR: Vendor not found.")
        return

    # List only available products for this vendor
    available_products = [p for p in vendor.products.values() if not p.is_assigned]

    if not available_products:
        print(f"ERROR: Vendor '{vendor.name}' has no available products (all items are already in use).")
        return

    print(f"\nAvailable Products for {vendor.name}:")
    for idx, prod in enumerate(available_products, 1):
        print(f"  {idx}. {prod.name} (${prod.cost:.2f})")

    try:
        p_choice = int(input(f"Select Product (1 to {len(available_products)}): "))
        if p_choice < 1 or p_choice > len(available_products):
            print("ERROR: Invalid selection.")
            return
    except ValueError:
        return

    selected_product = available_products[p_choice - 1]

    # STRICT SINGLE-USE CHECK: Cannot duplicate or reuse a product once used
    if selected_product.is_assigned:
        print(f"CONFLICT: '{selected_product.name}' is already used in '{selected_product.assigned_event_name}'.")
        print("Rule: A vendor's product can be used ONCE ONLY and cannot be duplicated.")
        return

    # Check if event already has this product
    for c in event.contracts:
        if c["product_name"].lower() == selected_product.name.lower():
            print(f"Notice: Event '{event.name}' already has a contract for '{selected_product.name}'.")
            confirm = input("Do you still wish to add an additional contract? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Assignment cancelled.")
                return
            break

    # Lock product and bind to event
    selected_product.mark_as_used(event.name)
    event.contracts.append({
        "vendor_name": vendor.name,
        "product_name": selected_product.name,
        "cost": selected_product.cost
    })

    print(f"\nSUCCESS: '{selected_product.name}' from '{vendor.name}' assigned to '{event.name}'!")
    print("Status: This product is now locked and CANNOT be assigned to any other event.")


# ==============================================================================
# 5. MASTER REPORT
# ==============================================================================

def generate_report():
    print("\n" + "=" * 65)
    print("       SMART EVENT PLANNING PLATFORM - MASTER LOGISTICS REPORT")
    print("=" * 65)

    for e in events:
        total_registered = len(e.attendees)
        checked_in = sum(1 for a in e.attendees if a.status == "Checked In")
        turnout_pct = (checked_in / total_registered * 100) if total_registered > 0 else 0.0

        print(f"\nEVENT: {e.name}")
        print(f"   Capacity     : {total_registered}/{e.max_capacity} Seats Filled")
        print(f"   Attendance   : {checked_in}/{total_registered} Checked In ({turnout_pct:.1f}% Turnout)")

        print("   Assigned Vendor Contracts:")
        if not e.contracts:
            print("      No vendors assigned.")
        else:
            total_vendor_cost = 0.0
            for c in e.contracts:
                print(f"      - {c['product_name']:<22} by {c['vendor_name']} (${c['cost']:.2f})")
                total_vendor_cost += c['cost']
            print(f"      Total Vendor Procurement Cost: ${total_vendor_cost:.2f}")

        print("-" * 65)


# ==============================================================================
# MAIN SYSTEM MENU
# ==============================================================================

def main():
    while True:
        print("""
====================================================================
 SMART EVENT PLANNING & RESOURCE COORDINATION PLATFORM (Milestone 2)
====================================================================
 1. Register Attendee (Capacity Guard & Tiers)
 2. View Attendee Directory
 3. Mark Attendance (Gate Check-In & Fraud Scanner)
 4. Add New Vendor
 5. Add Product to Vendor Catalog (Multi-product, No duplicates)
 6. View Vendors & Catalog Status
 7. Assign Vendor Product to Event (Strict Single-Use Rule)
 8. Generate Master Logistics & Turnout Report
 9. Exit
====================================================================
""")
        ch = input("Enter Choice (1-9): ").strip()

        if ch == "1":
            register_attendee()
        elif ch == "2":
            view_attendees()
        elif ch == "3":
            mark_attendance()
        elif ch == "4":
            add_vendor()
        elif ch == "5":
            add_product_to_vendor()
        elif ch == "6":
            view_vendors_and_products()
        elif ch == "7":
            assign_vendor_product()
        elif ch == "8":
            generate_report()
        elif ch == "9":
            print("\nThank you for using Smart Event Planning Platform!")
            break
        else:
            print("ERROR: Invalid Choice. Please select 1 to 9.")


if __name__ == "__main__":
    main()
