# ============================================================
# SMART EVENT PLANNER AND RESOURCE MANAGEMENT SYSTEM
# Milestone 1 - Unique Version
# ============================================================


# ---------------- Event Class ----------------

class Event:
    def __init__(self, event_id, event_name, event_date, event_time):
        self.event_id = event_id
        self.event_name = event_name
        self.event_date = event_date
        self.event_time = event_time
        self.venue = "Not Assigned"
        self.resources = []
        self.status = "Planning"


# ---------------- Data Storage ----------------

event_list = []
venue_list = []
resource_stock = {}


# ---------------- Common Functions ----------------

def get_event(event_id):
    for item in event_list:
        if item.event_id == event_id:
            return item
    return None


def get_integer(message):
    try:
        return int(input(message))
    except ValueError:
        return None


# ============================================================
# EVENT MANAGEMENT
# ============================================================

def create_event():
    print("\n========== CREATE NEW EVENT ==========")

    event_id = len(event_list) + 1

    event_name = input("Enter Event Name      : ").strip()
    event_date = input("Enter Date (DD/MM/YYYY): ").strip()
    event_time = input("Enter Time             : ").strip()

    if event_name == "" or event_date == "" or event_time == "":
        print("All event details are required.")
        return

    new_event = Event(
        event_id,
        event_name,
        event_date,
        event_time
    )

    event_list.append(new_event)

    print("\nEvent created successfully!")
    print("Event ID:", event_id)


def display_events():
    print("\n========== ALL EVENTS ==========")

    if len(event_list) == 0:
        print("No events have been created.")
        return

    for event in event_list:
        print("--------------------------------")
        print("Event ID :", event.event_id)
        print("Name     :", event.event_name)
        print("Date     :", event.event_date)
        print("Time     :", event.event_time)
        print("Venue    :", event.venue)
        print("Status   :", event.status)

        if event.resources:
            print("Resources:")
            for resource_name, amount in event.resources:
                print("  ", resource_name, "-", amount)
        else:
            print("Resources: None")

    print("--------------------------------")


def modify_event():
    display_events()

    if not event_list:
        return

    event_id = get_integer("\nEnter Event ID to modify: ")

    if event_id is None:
        print("Please enter a valid number.")
        return

    selected_event = get_event(event_id)

    if selected_event is None:
        print("Event ID does not exist.")
        return

    print("\nEnter the updated details:")

    new_name = input("New Event Name : ").strip()
    new_date = input("New Date       : ").strip()
    new_time = input("New Time       : ").strip()

    if new_name:
        selected_event.event_name = new_name

    if new_date:
        selected_event.event_date = new_date

    if new_time:
        selected_event.event_time = new_time

    print("Event details updated successfully!")


def remove_event():
    display_events()

    if not event_list:
        return

    event_id = get_integer("\nEnter Event ID to delete: ")

    if event_id is None:
        print("Invalid Event ID.")
        return

    selected_event = get_event(event_id)

    if selected_event is None:
        print("Event not found.")
        return

    event_list.remove(selected_event)

    print("Event deleted successfully.")


# ============================================================
# VENUE MANAGEMENT
# ============================================================

def register_venue():
    print("\n========== ADD VENUE ==========")

    venue_name = input("Enter Venue Name: ").strip()

    if venue_name == "":
        print("Venue name cannot be empty.")
        return

    if venue_name.lower() in [v.lower() for v in venue_list]:
        print("This venue is already registered.")
        return

    venue_list.append(venue_name)

    print("Venue added successfully.")


def display_venues():
    print("\n========== AVAILABLE VENUES ==========")

    if not venue_list:
        print("No venues registered.")
        return

    for number, venue in enumerate(venue_list, start=1):
        print(f"{number}. {venue}")


def allocate_venue():
    display_events()

    if not event_list:
        return

    event_id = get_integer("\nEnter Event ID: ")

    if event_id is None:
        print("Invalid Event ID.")
        return

    selected_event = get_event(event_id)

    if selected_event is None:
        print("Event not found.")
        return

    display_venues()

    if not venue_list:
        return

    venue_number = get_integer("\nSelect Venue Number: ")

    if venue_number is None or venue_number < 1 or venue_number > len(venue_list):
        print("Invalid venue selection.")
        return

    selected_venue = venue_list[venue_number - 1]

    # Check whether the selected venue is already occupied
    for event in event_list:

        if event.event_id == selected_event.event_id:
            continue

        if (event.venue == selected_venue and
                event.event_date == selected_event.event_date and
                event.event_time == selected_event.event_time):

            print("\nVenue conflict detected!")
            print("The selected venue is already booked.")
            return

    selected_event.venue = selected_venue

    print("Venue assigned successfully.")


# ============================================================
# RESOURCE MANAGEMENT
# ============================================================

def register_resource():
    print("\n========== ADD RESOURCE ==========")

    resource_name = input("Enter Resource Name: ").strip()

    if resource_name == "":
        print("Resource name cannot be empty.")
        return

    quantity = get_integer("Enter Quantity: ")

    if quantity is None or quantity <= 0:
        print("Quantity must be greater than zero.")
        return

    # Find existing resource without worrying about letter case
    existing_key = None

    for key in resource_stock:
        if key.lower() == resource_name.lower():
            existing_key = key
            break

    if existing_key:
        resource_stock[existing_key] += quantity
    else:
        resource_stock[resource_name] = quantity

    print("Resource stock updated successfully.")


def display_resources():
    print("\n========== RESOURCE INVENTORY ==========")

    if not resource_stock:
        print("No resources available.")
        return

    for name, quantity in resource_stock.items():
        print(f"{name} : {quantity}")


def assign_resource():
    display_events()

    if not event_list:
        return

    event_id = get_integer("\nEnter Event ID: ")

    if event_id is None:
        print("Invalid Event ID.")
        return

    selected_event = get_event(event_id)

    if selected_event is None:
        print("Event not found.")
        return

    display_resources()

    if not resource_stock:
        return

    resource_name = input("\nEnter Resource Name: ").strip()

    # Find resource ignoring uppercase/lowercase
    actual_resource = None

    for name in resource_stock:
        if name.lower() == resource_name.lower():
            actual_resource = name
            break

    if actual_resource is None:
        print("Resource is not available.")
        return

    quantity = get_integer("Enter Required Quantity: ")

    if quantity is None or quantity <= 0:
        print("Enter a valid quantity.")
        return

    if quantity > resource_stock[actual_resource]:
        print("Insufficient resource quantity.")
        print("Available:", resource_stock[actual_resource])
        return

    resource_stock[actual_resource] -= quantity

    selected_event.resources.append(
        (actual_resource, quantity)
    )

    print("Resource allocated successfully.")


# ============================================================
# EVENT REPORT
# ============================================================

def generate_report():
    print("\n")
    print("=" * 55)
    print("                 EVENT REPORT")
    print("=" * 55)

    if not event_list:
        print("No event information available.")
        return

    for event in event_list:

        print("\nEvent ID   :", event.event_id)
        print("Event Name :", event.event_name)
        print("Date       :", event.event_date)
        print("Time       :", event.event_time)
        print("Venue      :", event.venue)
        print("Status     :", event.status)

        print("Allocated Resources:")

        if len(event.resources) == 0:
            print("  No resources allocated")
        else:
            for name, quantity in event.resources:
                print(f"  {name} -> {quantity} units")

        print("-" * 55)


# ============================================================
# MAIN PROGRAM
# ============================================================

while True:

    print("\n")
    print("=" * 60)
    print("       SMART EVENT PLANNER & RESOURCE SYSTEM")
    print("=" * 60)

    print("""
    1. Create New Event
    2. Display Events
    3. Modify Event
    4. Delete Event
    5. Register Venue
    6. Display Venues
    7. Allocate Venue
    8. Add Resource
    9. Display Resources
   10. Allocate Resource
   11. Generate Event Report
   12. Exit
    """)

    print("=" * 60)

    choice = input("Choose an option: ").strip()

    if choice == "1":
        create_event()

    elif choice == "2":
        display_events()

    elif choice == "3":
        modify_event()

    elif choice == "4":
        remove_event()

    elif choice == "5":
        register_venue()

    elif choice == "6":
        display_venues()

    elif choice == "7":
        allocate_venue()

    elif choice == "8":
        register_resource()

    elif choice == "9":
        display_resources()

    elif choice == "10":
        assign_resource()

    elif choice == "11":
        generate_report()

    elif choice == "12":
        print("\nThank you for using Smart Event Planner!")
        print("Program closed successfully.")
        break

    else:
        print("\nInvalid option. Please select 1 to 12.")