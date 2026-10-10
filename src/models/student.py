"""Student model."""
import uuid
from datetime import datetime


class Student:
    """Represents a single student record."""

    def __init__(self, name, email, course, year_level,
                 student_id=None, gpa=0.0):
        # Generate a short unique ID if none is supplied
        self.student_id = student_id or str(uuid.uuid4())[:8]
        self.name = name
        self.email = email
        self.course = course
        self.year_level = year_level
        self.gpa = gpa
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at

    def to_dict(self):
        """Convert to a JSON-serializable dictionary."""
        return {
            'student_id': self.student_id,
            'name': self.name,
            'email': self.email,
            'course': self.course,
            'year_level': self.year_level,
            'gpa': self.gpa,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
