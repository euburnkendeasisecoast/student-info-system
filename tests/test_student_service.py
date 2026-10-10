import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from services.student_service import StudentService  # noqa: E402


class TestStudentService(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.service = StudentService(os.path.join(self.tmp.name, 's.json'))
        self.data = {'name': 'Ana Cruz', 'email': 'ana@example.com',
                     'course': 'BSIT', 'year_level': '2'}

    def tearDown(self):
        self.tmp.cleanup()

    def test_add_and_get(self):
        s = self.service.add_student(self.data)
        self.assertEqual(self.service.get_student(s['student_id'])['name'], 'Ana Cruz')

    def test_invalid_email_rejected(self):
        self.data['email'] = 'bad-email'
        with self.assertRaises(ValueError):
            self.service.add_student(self.data)

    def test_duplicate_email_rejected(self):
        self.service.add_student(self.data)
        with self.assertRaises(ValueError):
            self.service.add_student(self.data)

    def test_update(self):
        s = self.service.add_student(self.data)
        updated = self.service.update_student(s['student_id'], {'course': 'BSCS'})
        self.assertEqual(updated['course'], 'BSCS')

    def test_delete(self):
        s = self.service.add_student(self.data)
        self.assertTrue(self.service.delete_student(s['student_id']))
        self.assertFalse(self.service.delete_student(s['student_id']))


if __name__ == '__main__':
    unittest.main()
