import csv
import re

# Step 1: Read from 'output.txt' and parse data
with open('output.txt', 'r') as file:
    lines = file.readlines()

questions = []
answers = []
correct_answers = []
check_radio = []

# Regex patterns to match questions and answers
question_pattern = re.compile(r'^\d+\.\s(.+)')  # Match "1. What is the question?"
answer_pattern = re.compile(r'^([A-D])\)\s(.+?)(?:\s\(Correct Answer\))?$')  # Match "A) Option (Correct Answer)"
correct_answer_marker = "(Correct Answer)"

current_question = None
current_answers = []
correct_answer = None

for line in lines:
    line = line.strip()  # Remove leading/trailing whitespace

    # Skip heading lines
    if line.startswith("Cloud Practitioner") or line.startswith("Multiple Choice"):
        continue

    # Check if the line is a question
    question_match = question_pattern.match(line)
    if question_match:
        # If a new question starts and we have a previous question, store the previous one
        if current_question:
            questions.append(current_question)
            answers.append(current_answers)
            correct_answers.append(correct_answer)
            check_radio.append("Radio")  # Assuming multiple choice questions use radio buttons

        # Start processing a new question
        current_question = question_match.group(1)
        current_answers = []
        correct_answer = None
        continue

    # Check if the line is an answer
    answer_match = answer_pattern.match(line)
    if answer_match:
        answer_letter = answer_match.group(1)  # Get the answer letter (A, B, C, D)
        answer_text = answer_match.group(2)  # Get the answer text
        current_answers.append(answer_text)

        # Check if this answer is the correct one
        if correct_answer_marker in line:
            correct_answer = answer_text

# Don't forget to store the last question after finishing the loop
if current_question:
    questions.append(current_question)
    answers.append(current_answers)
    correct_answers.append(correct_answer)
    check_radio.append("Radio")

# Step 2: Write to 'questions.csv' with extra columns (Correct ans, Check/Radio)
with open('questions.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Question", "Ans1", "Ans2", "Ans3", "Ans4", "Correct ans", "Check/Radio"])  # header row
    for question, answer_options, correct_answer, check_or_radio in zip(questions, answers, correct_answers, check_radio):
        # Fill missing answers with empty strings if less than 4 answers are provided
        while len(answer_options) < 4:
            answer_options.append("")
        writer.writerow([question] + answer_options + [correct_answer, check_or_radio])

# Step 3: Clean up quotes and write to 'output.csv'
with open('questions.csv', 'r') as input_file:
    reader = csv.reader(input_file)
    with open('output.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        for row in reader:
            # Strip double quotes only if they surround the cell content
            cleaned_row = [cell.strip('"') if cell.startswith('"') and cell.endswith('"') else cell for cell in row]
            writer.writerow(cleaned_row)

# Additional improvements:
print(f"Processed {len(questions)} questions successfully.")
