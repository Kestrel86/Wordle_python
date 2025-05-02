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

def on_key_press(event):
        global guess
        global attempt
        global labels

        key = event.keysym
        char = event.char

        if key == "BackSpace":
            remove_letter()
            guess = guess[:-1]
            print(f"Backspace pressed, guess: {guess}")          # remove letter from guess
        elif key == "Return":
            if len(guess) == 5:
                handle_guess()     # handle guess here
            else:
                print("Not enough letters")
        elif char.isalpha() and len(guess) < 5:
            guess += char
            print(f"{attempt}: New guess: {guess}")        # update letter in Label
            update_letter()

def update_letter():
    for i in range(len(guess)):
        labels[attempt][i].config(text=guess[i].upper())

def remove_letter():
    labels[attempt][len(guess)-1].config(text="")

def handle_row(guess):
    global keyword
    global attempt
    global labels

    for idx, letter in enumerate(guess):
        if letter == keyword[idx]:        # green square (letter in keyword + letter in correct position)
            labels[attempt][idx].config(bg="#538D4E")
        elif letter in keyword:         # yellow square (letter in keyword but NOT in correct position)
            labels[attempt][idx].config(bg="#B59F3B")
        else:
            labels[attempt][idx].config(bg="#3A3A3C")


def handle_guess():
    global attempt
    global guess
    handle_row(guess)

    if guess == "hello":        # keyword here
        print("Correct")
    else:
        attempt += 1        # increment attempt
        guess = ""          # reset guess

# game 
def game():
    global guess
    global attempt
    global labels
    global keyword

    guess = ""
    keyword = "hello"
    attempt = 0

    grid_frame = Frame(root)
    grid_frame.pack(anchor='n', pady=50)

    labels = []     # store rows
    for j in range(6):
        row_entries = []
        for i, letter in enumerate(keyword):
            letter_box = Label(grid_frame, width=1, height=1, font=("Franklin Gothic Medium", 32), justify="center", bg='#121213', fg='white', padx=16)
            letter_box.grid(row=j, column=i, padx=3, pady=3)
            row_entries.append(letter_box)
        labels.append(row_entries)      # add rows to labels

    root.bind("<Key>", on_key_press)
    root.focus_set()
        
root.mainloop()
