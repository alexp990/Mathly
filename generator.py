from random import randint


class QuestionGenerator:
    def __init__(self, question_type: str, difficulty: str):
        if question_type not in (
            "Multiplication",
            "Division",
            "Addition",
            "Subtraction",
        ):
            raise Exception(f"Invalid question type: {question_type}")
        else:
            self.question_type = question_type

        # Setting ranges for number generation
        if difficulty == "Easy":
            if question_type == "Multiplication":
                self.question_range = [1, 20]
            elif question_type == "Division":
                self.question_range = [1, 15]
            elif question_type in ("Addition", "Subtraction"):
                self.question_range = [1, 50]

        elif difficulty == "Medium":
            if question_type == "Multiplication":
                self.question_range = [10, 30]
            elif question_type == "Division":
                self.question_range = [5, 20]
            elif question_type in ("Addition", "Subtraction"):
                self.question_range = [100, 500]

        elif difficulty == "Hard":
            if question_type == "Multiplication":
                self.question_range = [20, 50]
            elif question_type == "Division":
                self.question_range = [10, 100]
            elif question_type in ("Addition", "Subtraction"):
                self.question_range = [1000, 5000]

        else:
            raise Exception(f"Invalid question difficulty: {question_type}")

    def generate_numbers_for_question(self) -> list:
        """Generates mental math quesiton

        Returns:
            list: Sorted (ascending) array storing numbers for question in the format (n1, n2, answer).
        """
        if self.question_type in ("Addition", "Subtraction", "Multiplication"):
            n1, n2 = randint(
                *self.question_range), randint(*self.question_range)
            if n2 < n1:
                n1, n2 = n2, n1  # Make sure n1 < n2
            if self.question_type == "Addition":
                return (n1, n2, n1 + n2)
            elif self.question_type == "Subtraction":
                return (n1, n2, n2 - n1)
            else:
                return (n1, n2, n1 * n2)

        elif self.question_type == "Division":
            n1, helper = randint(
                *self.question_range), randint(*self.question_range)
            while n1 == 10 or helper == 10:  # We do not want very easy divisions
                n1, helper = randint(*self.question_range), randint(
                    *self.question_range
                )
            n2 = n1 * helper
            return (n1, n2, n2 // n1)


if __name__ == "__main__":
    gen = QuestionGenerator("Division", "Medium")
    print(gen.generate_numbers_for_question())
