import customtkinter as ctk
import random
from generator import QuestionGenerator
import time
import csv
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import datetime


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
        self.question_label = ctk.CTkLabel(
            root, text="", font=("Helvetica", 25))

        self.answer_entry = ctk.CTkEntry(root, font=("Helvetica", 14))

        self.result_label = ctk.CTkLabel(root, text="", font=("Helvetica", 12))

        self.time_label = ctk.CTkLabel(
            root, text="Time taken: ", font=("Helvetica", 14)
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

        self.view_data_button = ctk.CTkButton(
            root, text="View your data", font=("Helvetica", 12), command=self.view_data)
        self.view_data_button.pack()

        self.change_modes_button.pack(pady=10)
        self.random_mode = True

        self.operations = ["Addition", "Subtraction",
                           "Division", "Multiplication"]

        self.question_mode_select_box = ctk.CTkComboBox(
            root, values=self.operations)

        self.root.bind("<Escape>", self.show_start_menu)

    def change_modes(self):

        self.random_mode = not self.random_mode

        if not self.random_mode:
            self.question_mode_select_box.pack()
            self.change_modes_button.configure(text="Specific")

        elif self.random_mode:
            self.question_mode_select_box.pack_forget()
            self.change_modes_button.configure(text="Random")

    def view_data(self):

        self.change_modes_button.pack_forget()
        self.question_mode_select_box.pack_forget()
        self.difficulty_frame.pack_forget()
        self.view_data_button.pack_forget()

        # Ensure timestamps are parsed
        df = pd.read_csv("results.csv", parse_dates=[4])
        df.columns = ["Operation", "Difficulty",
                      "Time Taken", "Correct", "Timestamp"]

        # Convert timestamps to date only
        df["Date"] = df["Timestamp"].dt.date

        # Count correct answers per day
        daily_corrects = df[df["Correct"] == True].groupby("Date").size()

        # Create a new figure for correct answers plot
        fig2 = Figure(figsize=(5, 3), dpi=100)
        ax2 = fig2.add_subplot(111)

        # Plot the number of correct answers per day
        ax2.plot(daily_corrects.index, daily_corrects.values,
                 marker="o", linestyle="-", color="green")
        ax2.set_title("Number of Correct Answers Per Day")
        ax2.set_xlabel("Date")
        ax2.set_ylabel("Correct Answers")
        ax2.grid(True)

        # Display the plot
        canvas2 = FigureCanvasTkAgg(fig2, master=self.root)
        canvas2_widget = canvas2.get_tk_widget()
        canvas2_widget.pack(fill=ctk.BOTH, expand=True)

        # Call the existing graph update function to display the first graph as well
        self.view_data_avgs()

    def view_data_avgs(self):

        self.change_modes_button.pack_forget()
        self.question_mode_select_box.pack_forget()
        self.difficulty_frame.pack_forget()
        self.view_data_button.pack_forget()

        df = pd.read_csv("results.csv")

        operations, difficulties, times_taken, corrects, times = df.iloc[:,
                                                                         0], df.iloc[:, 1], df.iloc[:, 2], df.iloc[:, 3], df.iloc[:, 4]

        def find_averages(operation: str) -> list:

            res = []

            for difficulty in ("Easy", "Medium", "Hard"):

                arr = [row.iloc[2]
                       for index, row in df.iterrows() if row.iloc[0] == operation and row.iloc[1] == difficulty]

                l = len(arr)

                res.append(round(sum(arr)/l, 2) if l != 0 else 0)

            return res

        average_time_addition = find_averages("Addition")
        average_time_subtraction = find_averages("Subtraction")
        average_time_multiplication = find_averages("Multiplication")
        average_time_division = find_averages("Division")
        average_times = {"Addition": average_time_addition, "Subtraction": average_time_subtraction,
                         "Multiplication": average_time_multiplication, "Division": average_time_division}

        def update_graph(event=None):

            selected_operation = self.combobox.get()
            ax.clear()
            averages = average_times[selected_operation]
            difficulties = ["Easy", "Medium", "Hard"]

            ax.bar(difficulties, averages, color="skyblue", edgecolor="black")
            ax.set_title(f"Average Times for {selected_operation}")
            ax.set_xlabel("Difficulty")
            ax.set_ylabel("Average Time (seconds)")

            canvas.draw()

        fig = Figure(figsize=(5, 3), dpi=100)
        ax = fig.add_subplot(111)

        # Combobox for selecting operation
        self.combobox = ctk.CTkComboBox(
            self.root, values=self.operations, command=lambda event: update_graph())
        self.combobox.pack(pady=10)

        # Set up initial canvas
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(fill=ctk.BOTH, expand=True)

        self.combobox.set("Addition")
        update_graph()

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
        self.view_data_button.pack()

        if not self.random_mode:
            self.question_mode_select_box.pack()

        try:
            self.score_label.pack_forget()
            self.question_label.pack_forget()
            self.answer_entry.pack_forget()
            self.result_label.pack_forget()
            self.time_label.pack_forget()
            self.submit_button.pack_forget()
            self.canvas_widget.pack_forget()
            self.combobox.pack_forget()
        except Exception as e:
            pass

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
        self.view_data_button.pack_forget()

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
            self.time_label.configure(
                text=f"Time taken: {elapsed_time} seconds")
            self.root.after(100, self.update_time)  # Update every 100ms

    def check_answer(self, event=None):

        user_answer = self.answer_entry.get()

        try:
            user_answer = float(user_answer)
            if user_answer == self.answer:
                self.result_label.configure(
                    text="Correct!", text_color="green")
                self.end_time = time.time()
                self.time_taken = round(self.end_time - self.start_time, 2)
                self.score += int(-self.time_taken + 10)
                self.correct = True
            else:
                self.result_label.configure(
                    text=f"Wrong! The correct answer was {self.answer}.",
                    text_color="red",
                )
                self.score -= 5
                self.correct = False
            self.time_label.configure(
                text=f"Time taken: {self.time_taken} seconds")
            new_data = [[self.operation[1], self.difficulty,
                         self.time_taken, self.correct, datetime.now()]]
            with open("results.csv", mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerows(new_data)
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
