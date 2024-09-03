import random

import faker
from faker import Faker

fake = Faker()

subjects = ["Biology", "Math", "English", "Physics", "Chemistry"]


def generate_mobile_number(starting_number="", total_digits=11):
    # Validate that the starting number is not too long
    if len(starting_number) >= total_digits:
        raise ValueError("Starting number length must be less than total number length")

    remaining_digits = total_digits - len(starting_number)
    remaining_number = random.randint(10 ** (remaining_digits - 1), 10 ** remaining_digits - 1)

    return f"{starting_number}{remaining_number:0{remaining_digits}}"


def generate_random_students(n=10):
    students_list = []  # Renamed to avoid potential shadowing
    for _ in range(n):
        # Randomly select a first name and last name
        first_name = fake.first_name()
        last_name = fake.last_name()
        full_name = f"{first_name} {last_name}"

        # Randomly select a subject
        subject = random.choice(subjects)

        # Generate a random mobile number with a specific starting number
        mobile_number = generate_mobile_number(starting_number="")

        # Create a dict for the student
        student_info = {
            "name": full_name,
            "subject": subject,
            "mobile": mobile_number
        }

        students_list.append(student_info)

    return students_list


# Generate 10 random students
random_students = generate_random_students()

# Print the generated students
for student in random_students:
    print(f"Name: {student['name']}, Subject: {student['subject']}, Mobile: {student['mobile']}")
