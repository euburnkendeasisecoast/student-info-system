"""Student service: CRUD operations on a JSON data store."""
import json
import logging
import os
from datetime import datetime

from models.student import Student
from utils.validators import (validate_name, validate_email, validate_course,
                              validate_year_level, validate_gpa)

logger = logging.getLogger(__name__)

# Fields that may be changed through update_student
UPDATABLE_FIELDS = {'name', 'email', 'course', 'year_level', 'gpa'}


class StudentService:
    def __init__(self, data_file='data/students.json'):
        self.data_file = data_file
        self._ensure_data_file()

    # ---------- storage helpers ----------
    def _ensure_data_file(self):
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        if not os.path.exists(self.data_file):
            self._save_students([])

    def _load_students(self):
        try:
            with open(self.data_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Could not read data file: {e}")
            return []

    def _save_students(self, students):
        with open(self.data_file, 'w') as f:
            json.dump(students, f, indent=2)

    @staticmethod
    def _validate(data):
        """Validate whichever fields are present. Raises ValueError."""
        checks = {
            'name': validate_name, 'email': validate_email,
            'course': validate_course, 'year_level': validate_year_level,
            'gpa': validate_gpa,
        }
        for field, check in checks.items():
            if field in data:
                ok, message = check(data[field])
                if not ok:
                    raise ValueError(message)

    # ---------- CRUD ----------
    def add_student(self, student_data):
        self._validate(student_data)
        student_data = dict(student_data)
        student_data['year_level'] = int(student_data['year_level'])

        students = self._load_students()
        if any(s['email'].lower() == student_data['email'].lower()
               for s in students):
            raise ValueError("A student with this email already exists.")

        student = Student(**student_data)
        students.append(student.to_dict())
        self._save_students(students)
        return student.to_dict()

    def get_all_students(self):
        return self._load_students()

    def get_student(self, student_id):
        for student in self._load_students():
            if student['student_id'] == student_id:
                return student
        return None

    def update_student(self, student_id, update_data):
        # Ignore fields that must not change (id, timestamps)
        update_data = {k: v for k, v in update_data.items()
                       if k in UPDATABLE_FIELDS}
        self._validate(update_data)
        if 'year_level' in update_data:
            update_data['year_level'] = int(update_data['year_level'])

        students = self._load_students()
        for student in students:
            if student['student_id'] == student_id:
                student.update(update_data)
                student['updated_at'] = datetime.now().isoformat()
                self._save_students(students)
                return student
        return None

    def delete_student(self, student_id):
        students = self._load_students()
        remaining = [s for s in students if s['student_id'] != student_id]
        if len(remaining) == len(students):
            return False  # nothing was deleted
        self._save_students(remaining)
        return True
