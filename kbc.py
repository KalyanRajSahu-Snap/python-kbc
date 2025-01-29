import tkinter as tk
from tkinter import messagebox
import random

class MillionaireGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Who Wants to be a Millionaire")
        self.root.geometry("800x600")
        self.root.configure(bg="#000080")

        self.timer = 30
        self.timer_running = False

        # Prize amounts
        self.prize_amounts = [
            100, 200, 300, 500, 1000,
            2000, 4000, 8000, 16000, 32000,
            64000, 125000, 250000, 500000, 1000000
        ]
        
        # Question bank
        self.questions = [
            {
                "question": "Which planet is known as the Red Planet?",
                "options": ["Venus", "Mars", "Jupiter", "Saturn"],
                "correct": "Mars"
            },
            {
                "question": "Who painted the Mona Lisa?",
                "options": ["Van Gogh", "Da Vinci", "Picasso", "Monet"],
                "correct": "Da Vinci"
            },
            {
                "question": "What is the capital of Japan?",
                "options": ["Seoul", "Beijing", "Tokyo", "Bangkok"],
                "correct": "Tokyo"
            },
            {
                "question": "Which element has the chemical symbol 'Au'?",
                "options": ["Silver", "Gold", "Copper", "Iron"],
                "correct": "Gold"
            },
            {
                "question": "What is the largest mammal in the world?",
                "options": ["African Elephant", "Blue Whale", "Giraffe", "Hippopotamus"],
                "correct": "Blue Whale"
            }
        ]

        self.current_question = 0
        self.current_prize_index = 0
        
        self.setup_gui()
        self.lifelines = {
            "fifty_fifty": True,
            "phone_friend": True,
            "ask_audience": True
        }
        self.load_question()

    def setup_gui(self):
        # Timer label
        self.timer_label = tk.Label(
            self.root,
            text="Time: 30",
            bg="#000080",
            fg="white",
            font=("Arial", 14, "bold")
        )
        self.timer_label.pack(pady=10)

        # Question frame
        self.question_frame = tk.Frame(self.root, bg="#000080")
        self.question_frame.pack(pady=20)

        self.question_label = tk.Label(
            self.question_frame,
            wraplength=700,
            bg="#000080",
            fg="white",
            font=("Arial", 14, "bold")
        )
        self.question_label.pack()

        # Options frame with grid layout
        self.options_frame = tk.Frame(self.root, bg="#000080")
        self.options_frame.pack(pady=20)

        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(
                self.options_frame,
                width=30,
                height=2,
                bg="#000040",
                fg="white",
                font=("Arial", 12),
                command=lambda x=i: self.check_answer(x)
            )
            row = i // 2  # Integer division to get row (0 or 1)
            col = i % 2   # Remainder to get column (0 or 1)
            btn.grid(row=row, column=col, padx=10, pady=5)
            self.option_buttons.append(btn)

        # Lifelines frame
        self.lifelines_frame = tk.Frame(self.root, bg="#000080")
        self.lifelines_frame.pack(pady=20)

        self.fifty_fifty_btn = tk.Button(
            self.lifelines_frame,
            text="50:50",
            command=self.use_fifty_fifty,
            bg="#000040",
            fg="white"
        )
        self.fifty_fifty_btn.pack(side=tk.LEFT, padx=10)

        self.phone_friend_btn = tk.Button(
            self.lifelines_frame,
            text="Phone a Friend",
            command=self.use_phone_friend,
            bg="#000040",
            fg="white"
        )
        self.phone_friend_btn.pack(side=tk.LEFT, padx=10)

        self.ask_audience_btn = tk.Button(
            self.lifelines_frame,
            text="Ask the Audience",
            command=self.use_ask_audience,
            bg="#000040",
            fg="white"
        )
        self.ask_audience_btn.pack(side=tk.LEFT, padx=10)

        # Prize label
        self.prize_label = tk.Label(
            self.root,
            text="Current Prize: $0",
            bg="#000080",
            fg="white",
            font=("Arial", 12, "bold")
        )
        self.prize_label.pack(pady=20)

    def start_timer(self):
        if self.timer > 0 and self.timer_running:
            self.timer -= 1
            self.timer_label.config(text=f"Time: {self.timer}")
            self.root.after(1000, self.start_timer)
        elif self.timer == 0 and self.timer_running:
            self.timer_running = False
            messagebox.showinfo("Time's Up!", f"You've won ${self.prize_amounts[max(0, self.current_prize_index-1)]:,}")
            self.root.quit()

    def load_question(self):
        if self.current_question >= len(self.questions):
            messagebox.showinfo("Congratulations!", "You've won $1,000,000!")
            self.root.quit()
            return

        # Reset and start timer
        self.timer = 30
        self.timer_running = True
        self.timer_label.config(text=f"Time: {self.timer}")
        self.start_timer()

        question = self.questions[self.current_question]
        self.question_label.config(text=question["question"])
        
        for i, option in enumerate(question["options"]):
            self.option_buttons[i].config(text=f"{chr(65+i)}. {option}", state="normal")

        self.prize_label.config(text=f"Current Prize: ${self.prize_amounts[self.current_prize_index]:,}")

    def check_answer(self, choice):
        self.timer_running = False  # Stop the timer
        question = self.questions[self.current_question]
        selected_answer = question["options"][choice]
        
        if selected_answer == question["correct"]:
            if self.current_question == len(self.questions) - 1:
                messagebox.showinfo("Congratulations!", "You've won $1,000,000!")
                self.root.quit()
            else:
                messagebox.showinfo("Correct!", f"You've won ${self.prize_amounts[self.current_prize_index]:,}!")
                self.current_question += 1
                self.current_prize_index += 1
                self.load_question()
        else:
            messagebox.showinfo("Game Over", f"Wrong answer! You won ${self.prize_amounts[max(0, self.current_prize_index-1)]:,}")
            self.root.quit()

    def use_fifty_fifty(self):
        if not self.lifelines["fifty_fifty"]:
            return
        
        question = self.questions[self.current_question]
        correct_answer = question["correct"]
        wrong_options = [opt for opt in question["options"] if opt != correct_answer]
        remove_options = random.sample(wrong_options, 2)
        
        for i, option in enumerate(question["options"]):
            if option in remove_options:
                self.option_buttons[i].config(state="disabled")
        
        self.lifelines["fifty_fifty"] = False
        self.fifty_fifty_btn.config(state="disabled")

    def use_phone_friend(self):
        if not self.lifelines["phone_friend"]:
            return
        
        question = self.questions[self.current_question]
        correct_answer = question["correct"]
        
        if random.random() < 0.8:
            suggested_answer = correct_answer
        else:
            wrong_options = [opt for opt in question["options"] if opt != correct_answer]
            suggested_answer = random.choice(wrong_options)
        
        messagebox.showinfo("Phone a Friend", f"Your friend thinks the answer is: {suggested_answer}")
        
        self.lifelines["phone_friend"] = False
        self.phone_friend_btn.config(state="disabled")

    def use_ask_audience(self):
        if not self.lifelines["ask_audience"]:
            return
        
        question = self.questions[self.current_question]
        correct_answer = question["correct"]
        
        correct_percentage = random.randint(45, 85)
        remaining = 100 - correct_percentage
        wrong_percentages = []
        
        for i in range(3):
            if i == 2:
                wrong_percentages.append(remaining)
            else:
                value = random.randint(0, remaining)
                wrong_percentages.append(value)
                remaining -= value
        
        random.shuffle(wrong_percentages)
        
        results = []
        for i, option in enumerate(question["options"]):
            if option == correct_answer:
                results.append(correct_percentage)
            else:
                results.append(wrong_percentages.pop())
        
        result_text = "Audience Poll Results:\n"
        for i, option in enumerate(question["options"]):
            result_text += f"{chr(65+i)}: {results[i]}%\n"
        
        messagebox.showinfo("Ask the Audience", result_text)
        
        self.lifelines["ask_audience"] = False
        self.ask_audience_btn.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    game = MillionaireGame(root)
    root.mainloop()