import sys
import os

from database import db
from datetime import datetime

templates = [
    {
        'module': 'Basic-skills',
        'category': 'Math',
        'grade': 6,
        'topic': 'Arithmetic',
        'skill_name': 'Addition',
        'format': 1,
        'type': 'MAQ',
        'question_template': 'import random\na = random.randint(1, 100)\nb = random.randint(1, 100)\nquestion = f"What is {a} + {b}?"',
        'answer_template': 'answer = a + b',
        'created_by': 'system',
        'updated_by': 'system',
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    },
    {
        'module': 'Basic-skills',
        'category': 'Math',
        'grade': 6,
        'topic': 'Geometry',
        'skill_name': 'Area of Rect',
        'format': 1,
        'type': 'MAQ',
        'question_template': 'import random\nls = random.randint(1, 20)\nws = random.randint(1, 10)\nquestion = f"Find area of rectangle with length {ls} and width {ws}?"',
        'answer_template': 'answer = ls * ws',
        'created_by': 'system',
        'updated_by': 'system',
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
]

# Insert dummy data
mock_db = db.get_client()
# Check if using mock
if hasattr(mock_db, 'db_file'):
    print(f"Seeding Mock DB at {mock_db.db_file}...")
    mock_db.table('question_templates').insert(templates).execute()
    print("Dummy data seeded successfully.")
else:
    print("Not using Mock DB. Skipping seed.")
