import customtkinter as ctk
import random
from generator import QuestionGenerator
import time

# *Implement data saving to csv


class MentalMathApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mental Math App")
        self.root.geometry("500x600")

        self.score = 0
        self.difficulty = None

        # Score Label
        self.score_label = ctk.CTkLabel(
            root, text=f"Score: {self.score}", font=("Helvetica", 18)
        )

        # Title Label
        self.title_label = ctk.CTkLabel(
            root, text="Mental Math", font=("Helvetica", 25)
        )
        self.title_label.pack(pady=10)

        # Difficulty Selection
        self.difficulty_frame = ctk.CTkFrame(root)
        self.difficulty_frame.pack(pady=20)

        self.easy_button = ctk.CTkButton(
            self.difficulty_frame,
            text="Easy",
            font=("Helvetica", 18),
            command=lambda: self.select_difficulty("Easy"),
        )
        self.easy_button.grid(row=0, column=0, padx=10)

        self.medium_button = ctk.CTkButton(
            self.difficulty_frame,
            text="Medium",
            font=("Helvetica", 18),
            command=lambda: self.select_difficulty("Medium"),
        )
        self.medium_button.grid(row=0, column=1, padx=10)

        self.hard_button = ctk.CTkButton(
            self.difficulty_frame,
            text="Hard",
            font=("Helvetica", 18),
            command=lambda: self.select_difficulty("Hard"),
        )
        self.hard_button.grid(row=0, column=2, padx=10)

        # Question and Answer Widgets (hidden initially)
        self.question_label = ctk.CTkLabel(root, text="", font=("Helvetica", 25))

        self.answer_entry = ctk.CTkEntry(root, font=("Helvetica", 14))

        self.result_label = ctk.CTkLabel(root, text="", font=("Helvetica", 12))

        self.time_label = ctk.CTkLabel(
            root, text="Time taken: ", font=("Helvetica", 12)
        )

        self.submit_button = ctk.CTkButton(
            root,
            text="Submit Answer",
            font=("Helvetica", 12),
            command=self.check_answer,
        )

        self.answer_checked = True

        self.change_modes_button = ctk.CTkButton(
            root,
            text="Random",
            font=("Helvetica", 12),
            command=self.change_modes,
        )
        self.change_modes_button.pack(pady=10)
        self.random_mode = True

        self.operations = ["Addition", "Subtraction", "Division", "Multiplication"]
        self.question_mode_select_box = ctk.CTkComboBox(root, values=self.operations)

        self.root.bind("<Escape>", self.show_start_menu)

    def change_modes(self):
        self.random_mode = not self.random_mode
        if not self.random_mode:
            self.question_mode_select_box.pack()
            self.change_modes_button.configure(text="Specific")
        elif self.random_mode:
            self.question_mode_select_box.pack_forget()
            self.change_modes_button.configure(text="Random")

    def select_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.difficulty_frame.pack_forget()
        self.start_quiz()

    def show_start_menu(self, event=None):
        self.score = 0
        self.difficulty_frame.pack()
        self.easy_button.grid(row=0, column=0, padx=10)
        self.medium_button.grid(row=0, column=1, padx=10)
        self.hard_button.grid(row=0, column=2, padx=10)
        self.change_modes_button.pack(pady=10)
        if not self.random_mode:
            self.question_mode_select_box.pack()

        self.score_label.pack_forget()
        self.question_label.pack_forget()
        self.answer_entry.pack_forget()
        self.result_label.pack_forget()
        self.time_label.pack_forget()
        self.submit_button.pack_forget()

    def start_quiz(self):
        self.score = 0  # Reset score
        self.score_label.configure(text=f"Score: {self.score}")
        self.score_label.pack(pady=10)
        self.question_label.pack(pady=10)
        self.answer_entry.pack(pady=10)
        self.result_label.pack(pady=5)
        self.time_label.pack(pady=5)
        self.submit_button.pack(pady=10)

        self.change_modes_button.pack_forget()
        self.question_mode_select_box.pack_forget()

        # Display first question
        self.root.bind("<Return>", self.check_answer)
        self.root.bind("<space>", self.generate_question)
        self.answer_checked = True
        self.generate_question()

    def generate_question(self, event="Placeholder"):
        if self.answer_checked:
            self.start_time = time.time()
            self.answer_entry.delete(0, "end")
            self.time_label.configure(text="Time taken: ")
            self.result_label.configure(text="")

            operations = [
                ("+", "Addition"),
                ("-", "Subtraction"),
                ("*", "Multiplication"),
                ("/", "Division"),
            ]
            if self.random_mode:
                self.operation = random.choice(operations)
            elif not self.random_mode:
                user_operation = self.question_mode_select_box.get()
                symbol = [
                    operation[0]
                    for operation in operations
                    if operation[1] == user_operation
                ][0]
                self.operation = (symbol, user_operation)

            gen = QuestionGenerator(self.operation[1], self.difficulty)
            self.num1, self.num2, self.answer = gen.generate_numbers_for_question()
            self.question_label.configure(
                text=f"{self.num2} {self.operation[0]} {self.num1}"
            )
            self.answer_checked = False

            self.update_time()  # Start updating time continuously

    def update_time(self):
        """Update the time label continuously while answering the question."""
        if not self.answer_checked:
            elapsed_time = round(time.time() - self.start_time, 2)
            self.time_label.configure(text=f"Time taken: {elapsed_time} seconds")
            self.root.after(100, self.update_time)  # Update every 100ms

    def check_answer(self, event=None):
        user_answer = self.answer_entry.get()

        try:
            user_answer = float(user_answer)
            if user_answer == self.answer:
                self.result_label.configure(text="Correct!", text_color="green")
                self.end_time = time.time()
                self.time_taken = round(self.end_time - self.start_time, 2)
                self.time_label.configure(text=f"Time taken: {self.time_taken} seconds")
                self.score += int(-self.time_taken + 10)
            else:
                self.result_label.configure(
                    text=f"Wrong! The correct answer was {self.answer}.",
                    text_color="red",
                )
                self.score -= 5
        except ValueError:
            self.result_label.configure(
                text="Please enter a valid number.", text_color="red"
            )

        self.update_score()
        self.answer_checked = True

    def update_score(self):
        self.score_label.configure(text=f"Score: {self.score}")


if __name__ == "__main__":
    root = ctk.CTk()
    app = MentalMathApp(root)
    root.mainloop()
