from tkinter import *

# root window
root = Tk()

root.title("Wordle")
root.geometry('600x700')

# instructions 
rules = Label(root, text = """🎯 How to Play \n
You have 6 chances to crack the secret word! \n
🟩 Green means the letter is correct and in the right spot. \n
🟨 Yellow means the letter is in the word but in the wrong spot. \n
⬜️ Gray means the letter is not in the word at all. \n
Type your guesses and watch the colors guide your way to victory!""", 
font=("Helvetica", 16))

rules.grid(row=0, column=0, columnspan=7, pady=(100, 10), padx = 70)

# button to start the game
def start_game():
    rules.destroy()
    rules_btn.destroy()
    game()

rules_btn = Button(root, text = "Got it!" ,
                   command = start_game,
                   font=("Helvetica", 16),
                   bg = "blue",
                   width=10,
                   height=2)

rules_btn.grid(row=1, column=0, columnspan=7, pady=20, padx = 70)

# game 
def game():

    keyword = "hello"

    grid_frame = Frame(root)
    grid_frame.pack(expand=True)

    def handle_guess(event):
        user_input = event.widget.get()
        print(user_input)

    for j in range(6):
        row_entries = []
        for i, letter in enumerate(keyword):
            letter_box = Entry(grid_frame, width=5, font=("Helvetica", 20), justify="center")
            letter_box.grid(row=j, column=i, padx=2, pady=3)
            row_entries.append(letter_box)
            letter_box.bind("<Return>", handle_guess)


root.mainloop()
