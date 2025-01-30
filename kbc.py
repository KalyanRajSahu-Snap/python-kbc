import tkinter as tk
from tkinter import messagebox
import random

class MillionaireGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Who Wants to be a Millionaire - Indian Edition")
        self.root.geometry("800x600")
        self.root.configure(bg="#000080")

        self.timer = 30
        self.timer_running = False

        # Prize amounts in Indian Rupees with checkpoint at 3,20,000
        self.prize_amounts = [
            1000, 5000, 10000, 50000, 160000, 
            320000,  # Checkpoint
            640000, 1250000, 2500000, 5000000, 
            10000000,  # 1 Crore
            70000000,  # 7 Crore
        ]
        
        # Question bank with 12 questions
        self.questions = [
            {
                "question": "Which city is the capital of India?",
                "options": ["Mumbai", "New Delhi", "Kolkata", "Chennai"],
                "correct": "New Delhi"
            },
            {
                "question": "Who wrote India's national anthem 'Jana Gana Mana'?",
                "options": ["Rabindranath Tagore", "Bankim Chandra", "Sarojini Naidu", "Mahatma Gandhi"],
                "correct": "Rabindranath Tagore"
            },
            {
                "question": "Which is the smallest state of India by area?",
                "options": ["Goa", "Sikkim", "Tripura", "Kerala"],
                "correct": "Goa"
            },
            {
                "question": "Which Indian scientist won the Nobel Prize in Physics in 1930?",
                "options": ["C.V. Raman", "Homi Bhabha", "S.N. Bose", "A.P.J. Abdul Kalam"],
                "correct": "C.V. Raman"
            },
            {
                "question": "Which river is known as 'Ganga of the South'?",
                "options": ["Kaveri", "Krishna", "Godavari", "Narmada"],
                "correct": "Godavari"
            },
            {
                "question": "Who was the first Indian woman to win an Olympic medal?",
                "options": ["P.T. Usha", "Karnam Malleswari", "Mary Kom", "Saina Nehwal"],
                "correct": "Karnam Malleswari"
            },
            {
                "question": "Which was the first Indian movie submitted for the Academy Awards?",
                "options": ["Mother India", "Guide", "Madhumati", "Awaara"],
                "correct": "Mother India"
            },
            {
                "question": "Who was the first Indian to win the Booker Prize?",
                "options": ["Salman Rushdie", "Arundhati Roy", "Kiran Desai", "V.S. Naipaul"],
                "correct": "Arundhati Roy"
            },
            {
                "question": "Which Indian state has the highest literacy rate?",
                "options": ["Kerala", "Mizoram", "Goa", "Tamil Nadu"],
                "correct": "Kerala"
            },
            {
                "question": "Who designed the Indian Parliament building?",
                "options": ["Edwin Lutyens", "Herbert Baker", "Charles Correa", "Laurie Baker"],
                "correct": "Herbert Baker"
            },
            {
                "question": "Which was the first Indian company to be listed on NASDAQ?",
                "options": ["Infosys", "TCS", "Wipro", "HCL"],
                "correct": "Infosys"
            },
            {
                "question": "Who is known as the 'Father of Indian Space Program'?",
                "options": ["Vikram Sarabhai", "A.P.J. Abdul Kalam", "Satish Dhawan", "Homi Bhabha"],
                "correct": "Vikram Sarabhai"
            }
        ]

        self.current_question = 0
        self.current_prize_index = 0
        self.checkpoint_amount = 320000  # Checkpoint at ₹3,20,000
        
        self.setup_gui()
        self.lifelines = {
            "fifty_fifty": True,
            "phone_friend": True,
            "ask_audience": True
        }
        self.load_question()

    def format_money(self, amount):
        if amount >= 10000000:  # 1 Crore or more
            crores = amount / 10000000
            return f"₹{crores:.0f} Crore"
        elif amount >= 1000:
            return f"₹{amount:,}"
        else:
            return f"₹{amount}"

    def setup_gui(self):
        # [Previous GUI setup code remains the same until prize_label]

        # Prize label with Indian currency format
        self.prize_label = tk.Label(
            self.root,
            text="Current Prize: ₹0",
            bg="#000080",
            fg="white",
            font=("Arial", 12, "bold")
        )
        self.prize_label.pack(pady=20)

    def check_answer(self, choice):
        self.timer_running = False
        question = self.questions[self.current_question]
        selected_answer = question["options"][choice]
        
        if selected_answer == question["correct"]:
            if self.current_question == len(self.questions) - 1:
                messagebox.showinfo("Congratulations!", "You've won ₹7 Crore!")
                self.root.quit()
            else:
                messagebox.showinfo("Correct!", f"You've won {self.format_money(self.prize_amounts[self.current_prize_index])}!")
                self.current_question += 1
                self.current_prize_index += 1
                self.load_question()
        else:
            # Check if player has crossed checkpoint
            if self.prize_amounts[self.current_prize_index] > self.checkpoint_amount:
                won_amount = self.checkpoint_amount
            else:
                won_amount = self.prize_amounts[max(0, self.current_prize_index-1)]
            
            messagebox.showinfo("Game Over", f"Wrong answer! You won {self.format_money(won_amount)}")
            self.root.quit()

    def load_question(self):
        if self.current_question >= len(self.questions):
            messagebox.showinfo("Congratulations!", "You've won ₹7 Crore!")
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

        self.prize_label.config(text=f"Current Prize: {self.format_money(self.prize_amounts[self.current_prize_index])}")

    # [Rest of the code remains the same]

if __name__ == "__main__":
    root = tk.Tk()
    game = MillionaireGame(root)
    root.mainloop()