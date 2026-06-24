from tools import *

jd = """
Need Java Developer with Spring Boot.
AWS preferred.
"""

requirements = extract_requirements(jd)

print(requirements)

questions = generate_interview_questions("John")

print(questions)