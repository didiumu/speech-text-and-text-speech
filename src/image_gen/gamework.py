import tkinter as tk
from tkinter import messagebox

# Simple phishing examples
examples = [
    {"text": "You’ve won $1,000, click here to claim your prize!", "is_phish": True},
    {"text": "Your bank statement for this month is available for viewing", "is_phish": False},
]

class PhishGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Phish Fighter Game")
        self.score = 0
        self.current_example = 0

        self.label = tk.Label(root, text="Identify the Phishing Email:", font=('Helvetica', 14))
        self.label.pack()

        self.text_label = tk.Label(root, text=examples[self.current_example]["text"], font=('Helvetica', 12))
        self.text_label.pack()

        self.btn_phish = tk.Button(root, text="Phishing", command=self.check_phish)
        self.btn_phish.pack(side=tk.LEFT)

        self.btn_legit = tk.Button(root, text="Legitimate", command=self.check_legit)
        self.btn_legit.pack(side=tk.RIGHT)

    def check_phish(self):
        if examples[self.current_example]["is_phish"]:
            self.score += 1
            messagebox.showinfo("Correct!", "You identified it correctly as Phishing!")
        else:
            messagebox.showerror("Incorrect", "This was not a phishing email.")

        self.next_example()

    def check_legit(self):
        if not examples[self.current_example]["is_phish"]:
            self.score += 1
            messagebox.showinfo("Correct!", "You identified it correctly as Legitimate!")
        else:
            messagebox.showerror("Incorrect", "This was a phishing email.")

        self.next_example()

    def next_example(self):
        self.current_example += 1
        if self.current_example >= len(examples):
            messagebox.showinfo("Game Over", f"Your score is {self.score}")
            self.root.quit()
        else:
            self.text_label.config(text=examples[self.current_example]["text"])

if __name__ == "__main__":
    root = tk.Tk()
    game = PhishGame(root)
    root.mainloop()
