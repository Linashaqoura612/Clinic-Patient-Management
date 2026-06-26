import json
import os
import random
from datetime import datetime

# i'm storing all patients in one list, each patient is a dictionary
patients = []

# using a fixed filename so we always save/load from the same place
DATA_FILE = "patients.json"


# this function makes sure every new patient gets a unique ID
# i didn't want to use auto-increment in case patients get deleted
def generate_id():
    existing_ids = {p["id"] for p in patients}
    while True:
        new_id = random.randint(1000, 9999)
        if new_id not in existing_ids:
            return new_id


# i made this a separate function because i needed to search in multiple places
# it handles both ID search and partial name search
def find_patient(search_term):
    search_term = search_term.strip()

    # check if the user typed a number, if so search by ID
    if search_term.isdigit():
        pid = int(search_term)
        for p in patients:
            if p["id"] == pid:
                return p

    # otherwise search by name, partial match is fine
    for p in patients:
        if search_term.lower() in p["name"].lower():
            return p

    # nothing found
    return None


# just a helper to print one patient nicely
# i added the adult/child label because it looked useful
def print_patient(p):
    age_label = "Adult" if p["age"] >= 18 else "Child"
    print(f"""
  ID       : {p['id']}
  Name     : {p['name']}
  Age      : {p['age']} ({age_label})
  Phone    : {p['phone']}
  Symptoms : {p['symptoms']}
  Visits   : {len(p['visits'])} recorded
""")


# small utility so i don't keep retyping the separator line
def separator(char="─", length=46):
    print(char * length)


# shows the main menu every loop iteration
def show_menu():
    separator("═")
    print("   Clinic Patient Management System")
    separator("═")
    print("  1. Add New Patient")
    print("  2. View All Patients")
    print("  3. Search Patient")
    print("  4. Update Patient Information")
    print("  5. Add Visit Note")
    print("  6. View Patient History")
    print("  7. Save Data")
    print("  -- Advanced --")
    print("  8. Delete Patient")
    print("  9. Patient Statistics")
    print(" 10. Search by Symptom")
    print(" 11. Sort Patients by Name")
    print(" 12. Export Report to Text File")
    print("  0. Exit")
    separator("═")


# asks the user for patient details and adds them to the list
def add_patient():
    print("\n-- Add New Patient --")

    # strip and title-case the name so it looks clean
    name = input("  Enter full name       : ").strip().title()
    if not name:
        print("  Name cannot be empty.")
        return

    # keep asking for age until we get a valid number
    while True:
        try:
            age = int(input("  Enter age             : ").strip())
            if age < 0 or age > 130:
                print("  Please enter a realistic age.")
                continue
            break
        except ValueError:
            # user typed letters or something, ask again
            print("  Invalid age. Please enter a number.")

    phone = input("  Enter phone number    : ").strip()
    if not phone:
        print("  Phone cannot be empty.")
        return

    symptoms = input("  Enter main symptoms   : ").strip()
    if not symptoms:
        print("  Symptoms cannot be empty.")
        return

    # build the patient dictionary with an empty visits list to start
    patient = {
        "id": generate_id(),
        "name": name,
        "age": age,
        "phone": phone,
        "symptoms": symptoms,
        "visits": []
    }

    patients.append(patient)
    print(f"\n  Patient '{name}' added successfully! (ID: {patient['id']})")


# loops through all patients and prints them one by one
def view_patients():
    print("\n-- All Patients --")

    if not patients:
        print("  No patients found.")
        return

    print(f"  Total: {len(patients)} patient(s)\n")
    for p in patients:
        separator()
        print_patient(p)


# lets the user search by name or ID
def search_patient():
    print("\n-- Search Patient --")
    term = input("  Enter patient name or ID: ").strip()

    if not term:
        print("  Search term cannot be empty.")
        return

    p = find_patient(term)
    if p:
        print("  Patient found:")
        separator()
        print_patient(p)
    else:
        print("  No patient found matching that name or ID.")


# lets the user change one field at a time for a patient
def update_patient():
    print("\n-- Update Patient --")
    term = input("  Enter patient name or ID to update: ").strip()
    p = find_patient(term)

    if not p:
        print("  Patient not found.")
        return

    print(f"\n  Updating: {p['name']} (ID: {p['id']})")
    print("  What do you want to update?")
    print("    1. Name")
    print("    2. Age")
    print("    3. Phone")
    print("    4. Symptoms")

    choice = input("  Choose an option: ").strip()

    if choice == "1":
        new_val = input("  Enter new name: ").strip().title()
        if new_val:
            p["name"] = new_val
        else:
            print("  Name cannot be empty.")
            return

    elif choice == "2":
        try:
            new_val = int(input("  Enter new age: ").strip())
            p["age"] = new_val
        except ValueError:
            print("  Invalid age.")
            return

    elif choice == "3":
        new_val = input("  Enter new phone number: ").strip()
        if new_val:
            p["phone"] = new_val
        else:
            print("  Phone cannot be empty.")
            return

    elif choice == "4":
        new_val = input("  Enter new symptoms: ").strip()
        if new_val:
            p["symptoms"] = new_val
        else:
            print("  Symptoms cannot be empty.")
            return

    else:
        print("  Invalid choice.")
        return

    print("  Patient updated successfully.")


# adds a visit entry to a specific patient's visits list
def add_visit_note():
    print("\n-- Add Visit Note --")
    term = input("  Enter patient name or ID: ").strip()
    p = find_patient(term)

    if not p:
        print("  Patient not found.")
        return

    print(f"\n  Adding visit for: {p['name']}")

    # default to today's date if the user just hits enter
    today = datetime.today().strftime("%Y-%m-%d")
    date_input = input(f"  Visit date [{today}]: ").strip()
    date = date_input if date_input else today

    doctor = input("  Doctor name         : ").strip().title()
    if not doctor:
        print("  Doctor name cannot be empty.")
        return

    note = input("  Visit note          : ").strip()
    if not note:
        print("  Note cannot be empty.")
        return

    # advice is optional, some visits may not have a prescription
    advice = input("  Prescription/advice : ").strip()

    visit = {
        "date": date,
        "doctor": doctor,
        "note": note,
        "advice": advice if advice else "None"
    }

    p["visits"].append(visit)
    print("  Visit note added successfully.")


# shows all visit records for one patient
def view_patient_history():
    print("\n-- Patient History --")
    term = input("  Enter patient name or ID: ").strip()
    p = find_patient(term)

    if not p:
        print("  Patient not found.")
        return

    print(f"\n  Patient : {p['name']} (ID: {p['id']})")

    if not p["visits"]:
        print("  No visit history recorded yet.")
        return

    # print each visit with a number so it's easy to read
    for i, v in enumerate(p["visits"], 1):
        separator()
        print(f"  Visit {i}:")
        print(f"    Date     : {v['date']}")
        print(f"    Doctor   : {v['doctor']}")
        print(f"    Note     : {v['note']}")
        print(f"    Advice   : {v['advice']}")
    separator()


# writes all patient data to a JSON file so we don't lose anything
def save_data():
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(patients, f, indent=4, ensure_ascii=False)
        print(f"  Data saved successfully to '{DATA_FILE}'.")
    except Exception as e:
        print(f"  Failed to save data: {e}")


# runs at startup to load any previously saved data
def load_data():
    global patients

    # if the file doesn't exist yet, that's fine, just start fresh
    if not os.path.exists(DATA_FILE):
        print("  No saved data found. Starting with an empty system.")
        return

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            patients = json.load(f)
        print(f"  Loaded {len(patients)} patient(s) from saved data.")
    except (json.JSONDecodeError, Exception) as e:
        # file might be corrupted, better to start clean than crash
        print(f"  Could not load data: {e}. Starting fresh.")
        patients = []


# removes a patient from the list after asking the user to confirm
def delete_patient():
    print("\n-- Delete Patient --")
    term = input("  Enter patient name or ID to delete: ").strip()
    p = find_patient(term)

    if not p:
        print("  Patient not found.")
        return

    # always confirm before deleting, just in case
    confirm = input(f"  Delete '{p['name']}' (ID: {p['id']})? (yes/no): ").strip().lower()
    if confirm == "yes":
        patients.remove(p)
        print("  Patient deleted successfully.")
    else:
        print("  Deletion cancelled.")


# shows a quick summary of the patient data
def patient_statistics():
    print("\n-- Patient Statistics --")

    total = len(patients)
    if total == 0:
        print("  No patients in the system.")
        return

    adults = sum(1 for p in patients if p["age"] >= 18)
    children = total - adults
    no_visits = sum(1 for p in patients if not p["visits"])
    total_visits = sum(len(p["visits"]) for p in patients)

    print(f"  Total patients   : {total}")
    print(f"  Adults (18+)     : {adults}")
    print(f"  Children (<18)   : {children}")
    print(f"  With no visits   : {no_visits}")
    print(f"  Total visits     : {total_visits}")


# filters patients based on a keyword found in their symptoms
def search_by_symptom():
    print("\n-- Search by Symptom --")
    symptom = input("  Enter symptom keyword: ").strip().lower()

    if not symptom:
        print("  Keyword cannot be empty.")
        return

    # list comprehension to grab matching patients quickly
    results = [p for p in patients if symptom in p["symptoms"].lower()]

    if not results:
        print("  No patients found with that symptom.")
        return

    print(f"  Found {len(results)} patient(s):\n")
    for p in results:
        separator()
        print_patient(p)


# sorts and displays patients alphabetically by name
# note: this doesn't change the order in the actual list, just for display
def sort_by_name():
    if not patients:
        print("  No patients to sort.")
        return

    sorted_list = sorted(patients, key=lambda p: p["name"].lower())
    print("\n-- Patients Sorted by Name --")
    for p in sorted_list:
        separator()
        print_patient(p)


# writes a readable text report to a file, useful for printing or sharing
def export_report():
    if not patients:
        print("  No data to export.")
        return

    filename = "clinic_report.txt"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("=" * 46 + "\n")
            f.write("   Clinic Patient Management System - Report\n")
            f.write(f"   Generated: {datetime.today().strftime('%Y-%m-%d %H:%M')}\n")
            f.write("=" * 46 + "\n\n")
            f.write(f"Total Patients: {len(patients)}\n\n")

            for p in patients:
                f.write("-" * 46 + "\n")
                f.write(f"ID       : {p['id']}\n")
                f.write(f"Name     : {p['name']}\n")
                f.write(f"Age      : {p['age']}\n")
                f.write(f"Phone    : {p['phone']}\n")
                f.write(f"Symptoms : {p['symptoms']}\n")
                f.write(f"Visits   : {len(p['visits'])}\n")

                # write each visit under the patient
                for i, v in enumerate(p["visits"], 1):
                    f.write(f"  Visit {i}: {v['date']} | Dr. {v['doctor']}\n")
                    f.write(f"    Note  : {v['note']}\n")
                    f.write(f"    Advice: {v['advice']}\n")

        print(f"  Report exported to '{filename}'.")
    except Exception as e:
        print(f"  Failed to export report: {e}")


# main loop - keeps the program running until the user exits
def main():
    print("\n  Loading saved data...")
    load_data()

    while True:
        print()
        show_menu()
        choice = input("  Choose an option: ").strip()

        if choice == "1":
            add_patient()
        elif choice == "2":
            view_patients()
        elif choice == "3":
            search_patient()
        elif choice == "4":
            update_patient()
        elif choice == "5":
            add_visit_note()
        elif choice == "6":
            view_patient_history()
        elif choice == "7":
            save_data()
        elif choice == "8":
            delete_patient()
        elif choice == "9":
            patient_statistics()
        elif choice == "10":
            search_by_symptom()
        elif choice == "11":
            sort_by_name()
        elif choice == "12":
            export_report()
        elif choice == "0":
            # give the user a chance to save before leaving
            save_choice = input("\n  Save data before exiting? (yes/no): ").strip().lower()
            if save_choice == "yes":
                save_data()
            print("\n  Thank you for using the Clinic Patient Management System.")
            print("  Goodbye!\n")
            break
        else:
            print("  Invalid choice. Please enter a number from the menu.")


# entry point
if __name__ == "__main__":
    main()