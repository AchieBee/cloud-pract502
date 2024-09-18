import re
import csv

def process_question(question_text):
    match = re.match(r'(\d+)\.\s*(.*)', question_text)
    if match:
        return match.group(2).strip()
    return question_text.strip()

def process_answer(answer_text):
    match = re.match(r'([A-D])\)\s*(.*)', answer_text)
    if match:
        return match.group(2).strip()
    return answer_text.strip()

def determine_question_type(answers):
    if len(answers) > 1:
        return 'radio'
    return 'check'

def process_file(input_file, output_file):
    with open(input_file, 'r') as f:
        content = f.read()

    questions = re.split(r'(?=\d+\.)', content)[1:]  # Split on number followed by period

    csv_data = []
    skipped_questions = []

    for q_index, q in enumerate(questions, 1):
        lines = q.strip().split('\n')
        if len(lines) < 2:
            skipped_questions.append((q_index, q))
            continue

        question = process_question(lines[0])
        
        answers = []
        correct_ans = 1
        correct_answer_found = False

        for line in lines[1:]:
            if line.lower().startswith('correct answer:'):
                correct_text = line.split(':', 1)[1].strip()
                answers.append(correct_text)
                correct_ans = 1
                correct_answer_found = True
            elif re.match(r'[A-D][\).]', line):
                answer = process_answer(line)
                if '(Correct Answer)' in line or '(correct answer)' in line.lower():
                    correct_ans = ord(line[0].upper()) - ord('A') + 1
                    correct_answer_found = True
                    answer = re.sub(r'\(Correct Answer\)|\(correct answer\)', '', answer, flags=re.IGNORECASE).strip()
                answers.append(answer)

        if not correct_answer_found:
            print(f"Warning: No correct answer found for question {q_index}")
            print("Question content:")
            print(q)
            print("---")

        question_type = determine_question_type(answers)

        row = [question] + answers + [''] * (4 - len(answers)) + [str(correct_ans), question_type]
        csv_data.append(row)

    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Question', 'Ans1', 'Ans2', 'Ans3', 'Ans4', 'Correct ans', 'check_radio'])
        writer.writerows(csv_data)

    if skipped_questions:
        print("\nSkipped questions due to insufficient content:")
        for index, content in skipped_questions:
            print(f"Question {index}: {content}")

# Usage
process_file('output.txt', 'questions.csv')