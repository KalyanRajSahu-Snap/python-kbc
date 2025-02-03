import tkinter as tk
from tkinter import messagebox
import random

class UsernameScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Who Wants to be a Millionaire - Indian Edition")
        self.root.geometry("1000x600")
        self.root.configure(bg="#000080")
        
        # Center frame for username entry
        self.frame = tk.Frame(root, bg="#000080")
        self.frame.place(relx=0.5, rely=0.4, anchor="center")
        
        # Welcome label
        self.welcome_label = tk.Label(
            self.frame,
            text="Welcome to Who Wants to be a Millionaire!",
            bg="#000080",
            fg="white",
            font=("Arial", 20, "bold")
        )
        self.welcome_label.pack(pady=20)
        
        # Username label
        self.name_label = tk.Label(
            self.frame,
            text="Enter your name:",
            bg="#000080",
            fg="white",
            font=("Arial", 14)
        )
        self.name_label.pack(pady=10)
        
        # Username entry
        self.name_entry = tk.Entry(
            self.frame,
            font=("Arial", 12),
            width=30
        )
        self.name_entry.pack(pady=10)
        
        # Start button
        self.start_button = tk.Button(
            self.frame,
            text="Start Game",
            command=self.start_game,
            bg="#000040",
            fg="white",
            font=("Arial", 12, "bold")
        )
        self.start_button.pack(pady=20)
    
    def start_game(self):
        username = self.name_entry.get().strip()
        if not username:
            messagebox.showwarning("Warning", "Please enter your name!")
            return
        
        # Clear the current window contents
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Start the main game
        MillionaireGame(self.root, username)

class MillionaireGame:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("Who Wants to be a Millionaire - Indian Edition")
        self.root.geometry("1000x600")
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
        # Create main game frame (left side)
        self.game_frame = tk.Frame(self.root, bg="#000080")
        self.game_frame.pack(side=tk.LEFT, padx=20, expand=True, fill="both")

        # Add username label at the top left
        self.username_label = tk.Label(
            self.game_frame,
            text=f"Hi, {self.username}",
            bg="#000080",
            fg="white",
            font=("Arial", 14, "bold")
        )
        self.username_label.pack(anchor="w", pady=10)

        # Create prize ladder frame (right side)
        self.prize_ladder_frame = tk.Frame(self.root, bg="#000080", width=200)
        self.prize_ladder_frame.pack(side=tk.RIGHT, padx=20, fill="y")

        # Setup prize ladder
        self.prize_labels = []
        for i, amount in enumerate(reversed(self.prize_amounts)):
            label = tk.Label(
                self.prize_ladder_frame,
                text=self.format_money(amount),
                bg="#000080",
                fg="white",
                font=("Arial", 10, "bold"),
                width=15,
                pady=5
            )
            if amount == 320000:  # Checkpoint amount
                label.configure(bg="#4B0082")  # Different color for checkpoint
            label.pack(pady=1)
            self.prize_labels.append(label)

        # Timer label
        self.timer_label = tk.Label(
            self.game_frame,
            text="Time: 30",
            bg="#000080",
            fg="white",
            font=("Arial", 14, "bold")
        )
        self.timer_label.pack(pady=10)

        # Question frame
        self.question_frame = tk.Frame(self.game_frame, bg="#000080")
        self.question_frame.pack(pady=20)

        self.question_label = tk.Label(
            self.question_frame,
            wraplength=600,
            bg="#000080",
            fg="white",
            font=("Arial", 14, "bold")
        )
        self.question_label.pack()

        # Options frame with grid layout
        self.options_frame = tk.Frame(self.game_frame, bg="#000080")
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
            row = i // 2
            col = i % 2
            btn.grid(row=row, column=col, padx=10, pady=5)
            self.option_buttons.append(btn)

        # Lifelines frame
        self.lifelines_frame = tk.Frame(self.game_frame, bg="#000080")
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

        # Quit button
        self.quit_btn = tk.Button(
            self.game_frame,
            text="Quit Game",
            command=self.quit_game,
            bg="#8B0000",
            fg="white",
            font=("Arial", 12, "bold")
        )
        self.quit_btn.pack(pady=10)

        # Prize label
        self.prize_label = tk.Label(
            self.game_frame,
            text="Current Prize: ₹0",
            bg="#000080",
            fg="white",
            font=("Arial", 12, "bold")
        )
        self.prize_label.pack(pady=20)

    def update_prize_ladder(self):
        # Reset all labels to default
        for label in self.prize_labels:
            label.configure(bg="#000080")
            if label.cget("text") == self.format_money(320000):
                label.configure(bg="#4B0082")

        # Highlight current question
        current_prize = self.format_money(self.prize_amounts[self.current_prize_index])
        for label in self.prize_labels:
            if label.cget("text") == current_prize:
                label.configure(bg="#FFD700", fg="black")

    def start_timer(self):
        if self.timer > 0 and self.timer_running:
            self.timer -= 1
            self.timer_label.config(text=f"Time: {self.timer}")
            self.root.after(1000, self.start_timer)
        elif self.timer == 0 and self.timer_running:
            self.timer_running = False
            if self.prize_amounts[self.current_prize_index] > self.checkpoint_amount:
                won_amount = self.checkpoint_amount
            else:
                won_amount = self.prize_amounts[max(0, self.current_prize_index-1)]
            messagebox.showinfo("Time's Up!", f"{self.username}, you won {self.format_money(won_amount)}")
            self.root.quit()

    def load_question(self):
        if self.current_question >= len(self.questions):
            messagebox.showinfo("Congratulations!", f"Congratulations {self.username}! You've won ₹7 Crore!")
            self.root.quit()
            return

        self.timer = 30
        self.timer_running = True
        self.timer_label.config(text=f"Time: {self.timer}")
        self.start_timer()

        question = self.questions[self.current_question]
        self.question_label.config(text=question["question"])
        
        for i, option in enumerate(question["options"]):
            self.option_buttons[i].config(text=f"{chr(65+i)}. {option}", state="normal")

        self.prize_label.config(text=f"Current Prize: {self.format_money(self.prize_amounts[self.current_prize_index])}")
        self.update_prize_ladder()

    def check_answer(self, choice):
        self.timer_running = False
        question = self.questions[self.current_question]
        selected_answer = question["options"][choice]
        
        if selected_answer == question["correct"]:
            if self.current_question == len(self.questions) - 1:
                messagebox.showinfo("Congratulations!", f"Congratulations {self.username}! You've won ₹7 Crore!")
                self.root.quit()
            else:
                messagebox.showinfo("Correct!", f"Well done {self.username}! You've won {self.format_money(self.prize_amounts[self.current_prize_index])}!")
                self.current_question += 1
                self.current_prize_index += 1
                self.load_question()
        else:
            if self.prize_amounts[self.current_prize_index] > self.checkpoint_amount:
                won_amount = self.checkpoint_amount
            else:
                won_amount = self.prize_amounts[max(0, self.current_prize_index-1)]
            messagebox.showinfo("Game Over", f"Sorry {self.username}, wrong answer! You won {self.format_money(won_amount)}")
            self.root.quit()

    def quit_game(self):
        if self.current_prize_index > 0:
            won_amount = self.prize_amounts[self.current_prize_index - 1]
        else:
            won_amount = 0

        confirm = messagebox.askyesno(
            "Quit Game", 
            f"Are you sure you want to quit? You will win {self.format_money(won_amount)}."
        )
        
        if confirm:
            messagebox.showinfo(
                "Game Over", 
                f"{self.username}, you've chosen to quit. You won {self.format_money(won_amount)}!"
            )
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
        
        # Define friends with different expertise
        friends = [
            {"name": "Tech Expert Raj", "accuracy": 0.9, "field": "Technology and Science"},
            {"name": "College Professor Priya", "accuracy": 0.8, "field": "General Knowledge"},
            {"name": "Sports Enthusiast Amit", "accuracy": 0.6, "field": "Sports and Entertainment"}
        ]
        
        # Create a friend selection window
        friend_window = tk.Toplevel(self.root)
        friend_window.title("Choose a Friend")
        friend_window.geometry("400x250")
        friend_window.configure(bg="#000080")
        
        # Label for friend selection
        tk.Label(
            friend_window, 
            text="Choose a friend to call:", 
            bg="#000080", 
            fg="white", 
            font=("Arial", 14)
        ).pack(pady=10)
        
        # Variable to store selected friend
        selected_friend = tk.StringVar()
        
        def select_friend(friend):
            selected_friend.set(friend["name"])
            friend_window.destroy()
            self.process_phone_friend_help(friend)
        
        # Create buttons for each friend with their expertise
        for friend in friends:
            tk.Button(
                friend_window, 
                text=f"{friend['name']} ({friend['field']})", 
                command=lambda f=friend: select_friend(f),
                bg="#000040", 
                fg="white", 
                font=("Arial", 12),
                width=40
            ).pack(pady=5)
    
    def process_phone_friend_help(self, friend):
        question = self.questions[self.current_question]
        correct_answer = question["correct"]
        
        # Use friend's expertise to determine answer accuracy
        if random.random() < friend["accuracy"]:
            suggested_answer = correct_answer
        else:
            wrong_options = [opt for opt in question["options"] if opt != correct_answer]
            suggested_answer = random.choice(wrong_options)
        
        messagebox.showinfo(
            "Phone a Friend", 
            f"{friend['name']} thinks the answer is: {suggested_answer}\n"
            f"Confidence Level: {friend['accuracy']*100:.0f}%"
        )
        
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
    username_screen = UsernameScreen(root)
    root.mainloop()