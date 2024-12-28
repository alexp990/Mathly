import customtkinter as ctk
import random
from generator import QuestionGenerator


class MentalMathApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mental Math App")
        self.root.geometry("500x400")

        self.score = 0
        self.score_label = ctk.CTkLabel(
            root, text=f"Score: {self.score}", font=("Helvetica", 18)
        )
        self.score_label.pack(pady=10)

        self.question_label = ctk.CTkLabel(
            root, text="Mental Math", font=("Helvetica", 18)
        )
        self.question_label.pack(pady=10)

        self.question_text = ctk.CTkLabel(root, text="", font=("Helvetica", 14))
        self.question_text.pack(pady=10)

        self.answer_entry = ctk.CTkEntry(root, font=("Helvetica", 14))
        self.answer_entry.pack(pady=10)

        self.result_label = ctk.CTkLabel(root, text="", font=("Helvetica", 12))
        self.result_label.pack(pady=5)

        self.submit_button = ctk.CTkButton(
            root,
            text="Submit Answer",
            font=("Helvetica", 12),
            command=self.check_answer,
        )
        self.submit_button.pack(pady=10)
        self.root.bind("<Return>", self.check_answer)
        self.root.bind("<space>", self.generate_question)
        self.answer_checked = True

        # self.new_question_button = ctk.CTkButton(
        #     root,
        #     text="New Question",
        #     font=("Helvetica", 12),
        #     command=self.generate_question,
        # )
        # self.new_question_button.pack(pady=10)

        self.generate_question()

    def generate_question(self, event="Placeholder"):
        if self.answer_checked:
            self.answer_entry.delete(0, "end")
            self.result_label.configure(text="")

            operations = [
                ("+", "Addition"),
                ("-", "Subtraction"),
                ("*", "Multiplication"),
                ("/", "Division"),
            ]
            self.operation = random.choice(operations)

            gen = QuestionGenerator(self.operation[1], "Medium")
            print(self.operation)
            self.num1, self.num2, self.answer = gen.generate_numbers_for_question()
            self.question_label.configure(
                text=f"{self.num2} {self.operation[0]} {self.num1}"
            )
            self.answer_checked = False

    def check_answer(self, event):
        user_answer = self.answer_entry.get()

        try:
            user_answer = float(user_answer)
            if user_answer == self.answer:
                self.result_label.configure(text="Correct!", text_color="green")
                self.score += 1
            else:
                self.result_label.configure(
                    text=f"Wrong! The correct answer was {self.answer}.",
                    text_color="red",
                )
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
