from tkinter import *
import random

# Global variables for game state
global guess, attempt, keyword, labels, btn_refs

# root window
root = Tk()
root.title("Wordle")
root.geometry('600x700')

# instructions 
def show_instructions():
    def start_game():
        rules.destroy()
        rules_btn.destroy()
        game()

    rules_text = """🎯 How to Play \n
    You have 6 chances to crack the secret word! \n
    🟩 Green means the letter is correct and in the right spot. \n
    🟨 Yellow means the letter is in the word but in the wrong spot. \n
    ⬜️ Gray means the letter is not in the word at all. \n
    Type your guesses and watch the colors guide your way to victory!"""

    rules = Label(root, text=rules_text, font=("Helvetica", 16), wraplength=450)
    rules.grid(row=0, column=0, columnspan=7, pady=(100, 10), padx = 70)
    # Instructions button
    rules_btn = Button(root, text = "Got it!" ,
                    command = start_game,
                    font=("Helvetica", 16),
                    bg = "blue",
                    width=10,
                    height=2)
    rules_btn.grid(row=1, column=0, columnspan=7, pady=20, padx = 70)

# Function to create guess grid
def create_grid():
    global labels, keyword

    grid_frame = Frame(root)
    grid_frame.pack(anchor='n', pady=50)

    row_size = 5

    labels = []     # reset labels for rows
    for j in range(6):
        row_entries = []
        for i, letter in enumerate(keyword):
            letter_box = Label(grid_frame, width=1, font=("Franklin Gothic Medium", 32), justify="center", bg="#121213", fg="white", padx=16)
            letter_box.grid(row=j, column=i, padx=3, pady=3)
            row_entries.append(letter_box)
        labels.append(row_entries)

# Function to create on-screen keyboard
def create_keyboard():
    global btn_refs
    keyboard_rows = [
        ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
        ['ENTER', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '⌫'],
    ]
    keyboard_frame = Frame(root)
    keyboard_frame.pack()

    for row in keyboard_rows:
        row_frame = Frame(keyboard_frame)
        row_frame.pack()
        for key in row:
            btn_width = 6 if key == "ENTER" else 4 if key == "⌫" else 3
            btn = Button(
                row_frame, text=key, width=btn_width, height=1, font=("Franklin Gothic Medium", 18), cursor="hand2",
                bg="#818384", fg="white", command=lambda k=key: on_virtual_key_press(k)
            )
            btn.pack(side="left", padx=2, pady=2)
            btn_refs[key.lower()] = btn         # store btn reference

# Event handling functions
def on_key_press(event):
        global guess, attempt, labels
        key = event.keysym
        char = event.char

        if key == "BackSpace":
            remove_letter()
            guess = guess[:-1]
            print(f"Backspace pressed, guess: {guess}")
        elif key == "Return":
            if len(guess) == 5:
                handle_guess()     # handle guess here
            else:
                print("Not enough letters")             # should display popup saying this
        elif char.isalpha() and len(guess) < 5:
            guess += char
            print(f"{attempt}: New guess: {guess}")        # update letter in Label
            update_letter()

# Function to handle keyboard clicks
def on_virtual_key_press(key):
    event = type('Event', (object,), {})()      # Dummy event object
    if key == "⌫":
        event.keysym = "BackSpace"
        event.char = ""
    elif key == "ENTER":
        event.keysym = "Return"
        event.char = ""
    else:
        event.keysym = key
        event.char = key.lower()
    on_key_press(event)

# Function to update text of label 
def update_letter():
    for i in range(len(guess)):
        labels[attempt][i].config(text=guess[i].upper())

# Function to remove text (imitate backspace)
def remove_letter():
    labels[attempt][len(guess)-1].config(text="")

# Function to change color of row
def handle_row(guess):
    global keyword, attempt, labels
    for idx, letter in enumerate(guess):
        if letter == keyword[idx]:              # green square (letter in keyword + letter in correct position)
            labels[attempt][idx].config(bg="#538D4E")
        elif letter in keyword:                 # yellow square (letter in keyword but NOT in correct position)
            labels[attempt][idx].config(bg="#B59F3B")
        else:                                   # not in keyword
            labels[attempt][idx].config(bg="#3A3A3C")

# Function to change color of keyboard
def update_keyboard(guess):
    global btn_refs, keyword, attempt, labels
    for label in labels[attempt]:       # get latest row guessed
        letter = label.cget('text').lower()
        bg_color = label.cget('bg')
        btn_prev_color = btn_refs[letter].cget('bg')
        
        if bg_color == "#3A3A3C":
            btn_refs[letter].config(bg="#3A3A3C")
        elif bg_color == "#B59F3B" and btn_prev_color != "#538D4E":
            btn_refs[letter].config(bg="#B59F3B")
        else:
            btn_refs[letter].config(bg="#538D4E")

# Handle row guess
def handle_guess():
    global guess, attempt, keyword
    handle_row(guess)
    update_keyboard(guess)

    if guess == keyword and attempt <= 5:
        print("You win!")           # TODO: end game (win)
    elif attempt == 5 and guess != keyword:
        print("You lose!")          # TODO: end game (lose)
    else:
        attempt += 1        # increment attempt
        guess = ""          # reset guess

def get_keyword(word_file):
    global keyword
    with open(word_file, "r") as file:
        lines = file.readlines()
        line = random.choice(lines).strip()
        return line


# game function
def game():
    global guess, attempt, keyword, labels, btn_refs

    file_5 = "five-letter-words.txt"
    file_6 = "six-letter-words.txt"

    # current window size can fit up to 9 letters.

    # Reset variables
    guess = ""
    attempt = 0
    keyword = get_keyword(file_6)     # change to dynamically pick from words.txt
    labels = []                 # store rows of letter Labels
    btn_refs = {}               # store btn references for on-screen keyboard

    # debug
    print(f"Keyword: {keyword}")

    # Create game grid + keyboard
    create_grid()
    create_keyboard()

    # Bind keyboard events for player input
    root.bind("<Key>", on_key_press)
    root.focus_set()
        
show_instructions()
root.mainloop()

# next stage
# on correct word, reset game and new word added. 
# Reset board and grey out sections that were used last round? 
# Or give at least two tries back?