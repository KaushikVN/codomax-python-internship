"""
Codomax Python Internship - Module 2
Student Record Management System (CRUD with JSON & CSV Storage)
Covers: Functions, Lambdas, List Comprehensions, File I/O, and Exception Handling.
"""

import json
import csv
import os

JSON_FILE = "students.json"
CSV_EXPORT_FILE = "students_export.csv"


def load_students():
    """Loads student records from a JSON file with exception handling."""
    if not os.path.exists(JSON_FILE):
        return []
    try:
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError) as e:
        print(f"⚠️ Warning: Could not read {JSON_FILE} ({e}). Starting with empty list.")
        return []


def save_students(students):
    """Saves student records to a JSON file safely."""
    try:
        with open(JSON_FILE, "w", encoding="utf-8") as file:
            json.dump(students, file, indent=4)
        print("💾 Data saved successfully to JSON storage.")
    except IOError as e:
        print(f"❌ Error saving to file: {e}")


def calculate_grade(marks):
    """Calculates student grade using a helper function."""
    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return "A"
    elif marks >= 70:
        return "B"
    elif marks >= 60:
        return "C"
    elif marks >= 50:
        return "D"
    return "F"


def add_student(students):
    """Creates a new student record with input validation."""
    print("\n--- Add New Student ---")
    try:
        student_id = input("Enter Student ID: ").strip()
        if not student_id:
            raise ValueError("Student ID cannot be empty.")

        # Check for duplicate ID using list comprehension
        existing_ids = [s["id"] for s in students]
        if student_id in existing_ids:
            print(f"❌ Student with ID {student_id} already exists.")
            return

        name = input("Enter Student Name: ").strip()
        if not name:
            raise ValueError("Student name cannot be empty.")

        course = input("Enter Course (e.g., Python Development): ").strip()
        marks = float(input("Enter Marks (0 - 100): "))

        if not (0 <= marks <= 100):
            raise ValueError("Marks must be between 0 and 100.")

        grade = calculate_grade(marks)

        new_student = {
            "id": student_id,
            "name": name,
            "course": course if course else "General",
            "marks": marks,
            "grade": grade
        }

        students.append(new_student)
        save_students(students)
        print(f"✅ Student '{name}' added successfully!")

    except ValueError as ve:
        print(f"❌ Input Validation Error: {ve}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")


def view_students(students):
    """Displays all student records formatted cleanly."""
    print("\n--- Student Records ---")
    if not students:
        print("No student records found.")
        return

    # Using lambda function for sorted display
    sorted_students = sorted(students, key=lambda s: s["marks"], reverse=True)

    print(f"{'ID':<10} {'Name':<20} {'Course':<20} {'Marks':<10} {'Grade':<5}")
    print("-" * 65)
    for s in sorted_students:
        print(f"{s['id']:<10} {s['name']:<20} {s['course']:<20} {s['marks']:<10.2f} {s['grade']:<5}")


def search_student(students):
    """Searches for a student by ID or Name using list comprehension."""
    print("\n--- Search Student ---")
    query = input("Enter ID or Name to search: ").strip().lower()
    
    # List comprehension search filter
    results = [s for s in students if query in s["id"].lower() or query in s["name"].lower()]

    if results:
        print(f"\nFound {len(results)} matching record(s):")
        for s in results:
            print(f"ID: {s['id']} | Name: {s['name']} | Course: {s['course']} | Marks: {s['marks']} | Grade: {s['grade']}")
    else:
        print(f"❌ No records matching '{query}'.")


def update_student(students):
    """Updates an existing student's record."""
    print("\n--- Update Student Record ---")
    student_id = input("Enter Student ID to update: ").strip()

    for s in students:
        if s["id"] == student_id:
            print(f"Updating details for: {s['name']}")
            try:
                new_name = input(f"Enter New Name (leave blank to keep '{s['name']}'): ").strip()
                new_course = input(f"Enter New Course (leave blank to keep '{s['course']}'): ").strip()
                marks_input = input(f"Enter New Marks (leave blank to keep {s['marks']}): ").strip()

                if new_name:
                    s["name"] = new_name
                if new_course:
                    s["course"] = new_course
                if marks_input:
                    marks_val = float(marks_input)
                    if not (0 <= marks_val <= 100):
                        raise ValueError("Marks must be between 0 and 100.")
                    s["marks"] = marks_val
                    s["grade"] = calculate_grade(marks_val)

                save_students(students)
                print("✅ Record updated successfully!")
                return
            except ValueError as ve:
                print(f"❌ Update Error: {ve}")
                return

    print(f"❌ Student with ID {student_id} not found.")


def delete_student(students):
    """Deletes a student record by ID."""
    print("\n--- Delete Student Record ---")
    student_id = input("Enter Student ID to delete: ").strip()

    initial_count = len(students)
    students[:] = [s for s in students if s["id"] != student_id]

    if len(students) < initial_count:
        save_students(students)
        print(f"✅ Student with ID {student_id} deleted successfully.")
    else:
        print(f"❌ Student with ID {student_id} not found.")


def export_to_csv(students):
    """Exports all current student records to a CSV file."""
    print("\n--- Export to CSV ---")
    if not students:
        print("No student records available to export.")
        return

    try:
        with open(CSV_EXPORT_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["id", "name", "course", "marks", "grade"])
            writer.writeheader()
            writer.writerows(students)
        print(f"✅ Exported {len(students)} record(s) to '{CSV_EXPORT_FILE}' successfully.")
    except Exception as e:
        print(f"❌ Failed to export CSV: {e}")


def main():
    """Main application loop."""
    students = load_students()

    while True:
        print("\n==========================================")
        print("🎓 STUDENT RECORD MANAGEMENT SYSTEM")
        print("==========================================")
        print("1. View All Students (Sorted by Marks)")
        print("2. Add New Student")
        print("3. Search Student")
        print("4. Update Student Record")
        print("5. Delete Student Record")
        print("6. Export Records to CSV")
        print("7. Exit Application")
        print("==========================================")

        choice = input("Enter your choice (1-7): ").strip()

        try:
            if choice == "1":
                view_students(students)
            elif choice == "2":
                add_student(students)
            elif choice == "3":
                search_student(students)
            elif choice == "4":
                update_student(students)
            elif choice == "5":
                delete_student(students)
            elif choice == "6":
                export_to_csv(students)
            elif choice == "7":
                print("\n👋 Exiting Student Management System. Goodbye!")
                break
            else:
                print("⚠️ Invalid choice. Please enter a number between 1 and 7.")
        except Exception as e:
            print(f"❌ Error during operation: {e}")
        finally:
            pass


if __name__ == "__main__":
    main()