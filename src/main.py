"""Student Information System - command line interface."""
import logging
import os

from services.student_service import StudentService
from utils.config import load_config

config = load_config()
os.makedirs(os.path.dirname(config['log_file']), exist_ok=True)

logging.basicConfig(
    level=getattr(logging, config['log_level'].upper(), logging.INFO),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config['log_file']),
        logging.StreamHandler(),
    ],
)


class StudentInformationSystem:
    def __init__(self):
        self.student_service = StudentService(config['data_file'])
        self.logger = logging.getLogger(__name__)

    def display_menu(self):
        print("\n=== Student Information System ===")
        print("1. Add Student")
        print("2. View All Students")
        print("3. View Student by ID")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Exit")

    @staticmethod
    def _print_student(s):
        print(f"ID: {s['student_id']}, Name: {s['name']}, "
              f"Email: {s['email']}, Course: {s['course']}, "
              f"Year: {s['year_level']}")

    def add_student(self):
        print("\n--- Add New Student ---")
        student_data = {
            'name': input("Name: "),
            'email': input("Email: "),
            'course': input("Course: "),
            'year_level': input("Year Level (1-4): "),
        }
        try:
            student = self.student_service.add_student(student_data)
            self.logger.info(f"Added student: {student['student_id']}")
            print(f"Student added successfully! ID: {student['student_id']}")
        except ValueError as e:  # validation problems
            self.logger.warning(f"Validation failed: {e}")
            print(f"Error: {e}")
        except Exception as e:
            self.logger.error(f"Error adding student: {e}")
            print("Error adding student.")

    def view_all_students(self):
        print("\n--- All Students ---")
        students = self.student_service.get_all_students()
        if not students:
            print("No students found.")
            return
        for student in students:
            self._print_student(student)

    def view_student(self):
        student = self.student_service.get_student(input("Enter Student ID: "))
        if student:
            print()
            self._print_student(student)
        else:
            print("Student not found.")

    def update_student(self):
        student_id = input("Enter Student ID to update: ")
        student = self.student_service.get_student(student_id)
        if not student:
            print("Student not found.")
            return

        print("Press Enter to keep the current value.")
        update_data = {}
        for field, label in [('name', 'Name'), ('email', 'Email'),
                             ('course', 'Course'), ('year_level', 'Year Level')]:
            value = input(f"{label} [{student[field]}]: ")
            if value:
                update_data[field] = value

        if not update_data:
            print("No changes made.")
            return
        try:
            self.student_service.update_student(student_id, update_data)
            self.logger.info(f"Updated student: {student_id}")
            print("Student updated successfully!")
        except ValueError as e:
            self.logger.warning(f"Validation failed: {e}")
            print(f"Error: {e}")
        except Exception as e:
            self.logger.error(f"Error updating student: {e}")
            print("Error updating student.")

    def delete_student(self):
        student_id = input("Enter Student ID to delete: ")
        if input(f"Delete {student_id}? (y/n): ").lower() != 'y':
            print("Cancelled.")
            return
        try:
            if self.student_service.delete_student(student_id):
                self.logger.info(f"Deleted student: {student_id}")
                print("Student deleted successfully!")
            else:
                print("Student not found.")
        except Exception as e:
            self.logger.error(f"Error deleting student: {e}")
            print("Error deleting student.")

    def run(self):
        actions = {
            '1': self.add_student, '2': self.view_all_students,
            '3': self.view_student, '4': self.update_student,
            '5': self.delete_student,
        }
        while True:
            self.display_menu()
            choice = input("Enter your choice (1-6): ")
            if choice == '6':
                print("Exiting... Done.")
                break
            action = actions.get(choice)
            if action:
                action()
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    StudentInformationSystem().run()
