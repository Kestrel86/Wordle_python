# How to Run
# While in the folder of Wordle_python,
# Run the command: python wordle.py

from tkinter import *
import random
from dictionary import five_letter_word_list, six_letter_word_list, seven_letter_word_list, eight_letter_word_list, nine_letter_word_list
from collections import Counter
import sys

# Global variables for game state
global guess, attempt, keyword, labels, btn_refs, keyword_length, current_dictionary, row_size

def get_os():
    if sys.platform.startswith('darwin'):
        return 'macOS'
    else:
        return 'other'
    
current_os = get_os()

if current_os == 'macOS':
    from word_definition import lookup_word
    from tkmacosx import Button as KeyButton
else:
    KeyButton = Button

length_to_dict = {
    5: five_letter_word_list,
    6: six_letter_word_list,
    7: seven_letter_word_list,
    8: eight_letter_word_list,
    9: nine_letter_word_list
}

# root window
root = Tk()
root.title("Wordle")
root.geometry('600x800')

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
    Once you guess the correct word, the word length increases by 1, and you get 1 additional chance to solve the next word! \n
    Continue solving the increasing word lengths and challenges to achieve victory!"""

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

# A label to show messages to the user
def create_status_label():
    global status_label
    status_label = Label(root,
                         text="",
                         font=("Helvetica", 20),
                         fg="white")
    status_label.pack(pady=(50,0))

# A label to show messages to the user
def create_definition_label():
    global definition_label
    definition_label = Label(root,
                         text="",
                         font=("Helvetica", 20),
                         fg="white",
                         wraplength=500,
                         justify=LEFT,
                         padx=10,
                         pady=10)
    definition_label.pack(pady=(50,0), padx=(20,20))

# Function to have the status label show only for a few seconds
def show_message(msg, delay=3000):
    status_label.config(text=msg, fg="red")
    root.after(delay, lambda: status_label.config(text=""))

def show_definition(msg):
    if msg:
        definition_label.config(text=msg)
    else:
        definition_label.config(text="No definition found.")

# Function to create guess grid
def create_grid(size=6, winning_row=False):
    global labels, keyword, row_size

    grid_frame = Frame(root)
    grid_frame.pack(anchor='n', pady=10)

    row_size = max(3, size)
    labels = []     # reset labels for rows

    if winning_row == True:
        row_size += 1

    for j in range(row_size):
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
    keyboard_frame.pack(side="bottom", pady=20, expand=False, fill='x') # keeps it at the bottom of the window

    for row in keyboard_rows:
        row_frame = Frame(keyboard_frame)
        row_frame.pack()
        for key in row:
            if current_os == 'macOS':           # pixel sizes for tkmacosx
                if key == "ENTER":
                    w, h = 85, 50              # wide key
                elif key == "⌫":
                    w, h = 65, 50
                else:
                    w, h = 50, 50              # single-letter key
                font_size = 24
            else:                              # character units for regular Tk
                w = 6 if key == "ENTER" else 4 if key == "⌫" else 3
                h = 1
                font_size = 18

            btn = KeyButton(
                row_frame,
                text=key,
                width=w,
                height=h,
                font=("Franklin Gothic Medium", font_size),
                cursor="hand2",
                bg="#818384",
                fg="white",
                command=lambda k=key: on_virtual_key_press(k)
            )
            btn.pack(side="left", padx=2, pady=2)
            btn_refs[key.lower()] = btn


# Event handling functions
def on_key_press(event):
    global guess, attempt, labels
    key = event.keysym
    char = event.char

    if key == "BackSpace":
        remove_letter()
        guess = guess[:-1]
        # print(f"Backspace pressed, guess: {guess}")
    elif key == "Return":
        if current_os == 'macOS':
            if len(guess) == keyword_length and lookup_word(guess) != None:
                handle_guess()     # handle VALID guess here
            elif lookup_word(guess) == None and len(guess) == keyword_length:
                show_message("Not in word list") 
            else:
                show_message("Not enough letters")
        else:
            if len(guess) == keyword_length and guess in current_dictionary:
                handle_guess()     # handle VALID guess here
            elif guess not in current_dictionary and len(guess) == keyword_length:
                show_message("Not in word list") 
            else:
                show_message("Not enough letters")
    elif char.isalpha() and len(guess) < keyword_length:
        guess += char
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
    valid_word = False
    keyword_letter_counts = None
    used_counts = None

    # validate the word based on OS
    if current_os == 'macOS':
        if lookup_word(guess) is not None or guess in current_dictionary:
            valid_word = True
        
    else:
        if guess in current_dictionary:
            valid_word = True

    if valid_word:
        keyword_letter_counts = Counter(keyword)
        used_counts = Counter()

        # mark green squares
        for idx, letter in enumerate(guess):
            if letter == keyword[idx]: # green square (letter in correct pos)
                labels[attempt][idx].config(bg="#538D4E")
                used_counts[letter] += 1 # track used letters
            else:
                labels[attempt][idx].config(bg="#3A3A3C") # initially mark as not in word
        
        for idx, letter in enumerate(guess):
            if letter != keyword[idx] and letter in keyword:
                if used_counts[letter] < keyword_letter_counts[letter]:
                    labels[attempt][idx].config(bg="#B59F3B") # yellow square (letter in wrong pos)
                    used_counts[letter] += 1

        return True # valid word and colors applied
    
    return False # word not valid
                

# Function to change color of keyboard
def update_keyboard(guess):
    global btn_refs, keyword, attempt, labels
    for label in labels[attempt]:       # get latest row guessed
        letter = label.cget('text').lower()
        bg_color = label.cget('bg')
        btn_prev_color = btn_refs[letter].cget('bg')
        
        if bg_color == "#3A3A3C" or bg_color == "#121213":
            btn_refs[letter].config(bg="#3A3A3C")
        elif bg_color == "#B59F3B" and btn_prev_color != "#538D4E":
            btn_refs[letter].config(bg="#B59F3B")
        else:
            btn_refs[letter].config(bg="#538D4E")

def show_end_popup(message, game_end=0,attempts_left=True, winning_row=False):
    popup = Toplevel(root)
    popup.title("Game Over")
    popup.geometry("300x200")
    popup.grab_set() 

    def quit_game():
        root.destroy()

    def play_again():
        global row_size
        if game_end == 1:
            popup.destroy()
            start_round(increase=attempts_left, size=row_size-attempt, winning_row=winning_row)
        else:
            popup.destroy()
            start_round()
    
    def restart_game():
        global keyword_length
        keyword_length = 5
        popup.destroy()
        start_round(increase = False, size = 6, winning_row = False)
        
    if keyword_length == 9:
        popup.geometry("350x250")
        Label(popup, text=message, font=("Helvetica", 16), wraplength=250, pady=20).pack()

        Button(popup, text="Restart Game (Back to 5 letter words)", command=restart_game, font=("Helvetica", 14), bg="green", fg="black").pack(pady=5)
        Button(popup, text = "Continue (With 9 letter words)", command = play_again, font=("Helvetica", 14), bg="green", fg="black").pack(pady=5)
        Button(popup, text="Quit", command=quit_game, font=("Helvetica", 14), bg="red", fg="black").pack(pady=5)
    else: 
        Label(popup, text=message, font=("Helvetica", 16), wraplength=250, pady=20).pack()

        Button(popup, text="Play Again", command=restart_game, font=("Helvetica", 14), bg="green", fg="black").pack(pady=5)
        Button(popup, text="Quit", command=quit_game, font=("Helvetica", 14), bg="red", fg="black").pack(pady=5)

def show_continue_popup(message, game_end=0,attempts_left=True, winning_row=False):
    popup = Toplevel(root)
    popup.title("Game Over")
    popup.geometry("300x200")
    popup.grab_set() 

    Label(popup, text=message, font=("Helvetica", 16), wraplength=250, pady=20).pack()

    def quit_game():
        root.destroy()

    def restart_game():
        global row_size
        # Clear the definition when player hits continue
        definition_label.config(text="")
        if game_end == 1:
            popup.destroy()
            start_round(increase=attempts_left, size=row_size-attempt, winning_row=winning_row)
        else:
            popup.destroy()
            start_round()

    popup.bind("<Return>", lambda event: restart_game())
    Button(popup, text="Continue", command=restart_game, font=("Helvetica", 14), bg="green", fg="black").pack(pady=5)
    Button(popup, text="Quit", command=quit_game, font=("Helvetica", 14), bg="red", fg="black").pack(pady=5)

# Handle row guess
def handle_guess():
    global guess, attempt, keyword, row_size
    handle_row(guess)               # change row color
    update_keyboard(guess)

    attempts_left = True

    if guess == keyword:
        guess = ""
        # attempt += 1

        if current_os == 'macOS':
            show_definition(lookup_word(keyword))

        if len(keyword) != 9:
            show_continue_popup("Round Complete! Continue to next round?", game_end=1, attempts_left=attempts_left, winning_row=False)
        else:
            show_end_popup("You finished!")

    elif attempt >= row_size-1 and guess != keyword:
        show_end_popup(f"You lose!\nThe word was {keyword.upper()}")

    elif guess == keyword and keyword_length == 9:
        show_end_popup("You Win")

    else:
        print(f"{attempt}: Guess: {guess}") 
        attempt += 1
        guess = ""

def get_keyword():
    global keyword, keyword_length
    if keyword_length == 5:
        length = len(five_letter_word_list)
        num = random.randint(0, length)
        return five_letter_word_list[num]
    elif keyword_length == 6:
        length = len(six_letter_word_list)
        num = random.randint(0, length)
        return six_letter_word_list[num]
    elif keyword_length == 7:
        length = len(seven_letter_word_list)
        num = random.randint(0, length)
        return seven_letter_word_list[num]
    elif keyword_length == 8:
        length = len(eight_letter_word_list)
        num = random.randint(0, length)
        return eight_letter_word_list[num]
    elif keyword_length == 9:
        length = len(nine_letter_word_list)
        num = random.randint(0, length)
        return nine_letter_word_list[num]
        
def start_round(increase=False, size=6, winning_row=False):

    global keyword_length, current_dictionary
    global keyword, attempt, guess, labels, btn_refs

    # If the player gets the word correct and the current word is less
    # than 9 characters increase word length and clear the board
    if increase and keyword_length < 9:
        keyword_length += 1
    current_dictionary = length_to_dict[keyword_length]

    keyword = get_keyword()
    print(keyword)
    guess   = ""
    labels  = []
    btn_refs = {}
    attempt = 0

    for widget in root.winfo_children():
        widget.destroy()
    create_status_label()
    create_grid(size,winning_row=winning_row)
    create_definition_label()
    create_keyboard()
    root.focus_set()

# game function
def game():
    global keyword_length, attempt
    attempt = 0
    root.bind("<Key>", on_key_press)
    root.focus_set()
    keyword_length = 5          # first round is always 5 letters
    start_round()               
        
show_instructions()
root.mainloop()


# next stage
# on correct word, reset game and new word added. 
# Reset board and grey out sections that were used last round? 
# Or give at least two tries back?