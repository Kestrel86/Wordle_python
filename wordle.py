from tkinter import *
import random
from dictionary import five_letter_word_list, six_letter_word_list, seven_letter_word_list, eight_letter_word_list, nine_letter_word_list
from collections import Counter

# Global variables for game state
global guess, attempt, keyword, labels, btn_refs, keyword_length, current_dictionary

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

# A label to show messages to the user
def create_status_label():
    global status_label
    status_label = Label(root,
                         text="",
                         font=("Helvetica", 20),
                         fg="white")
    status_label.pack(pady=(50,0))

# Function to have the status label show only for a few seconds
def show_message(msg, delay=3000):
    status_label.config(text=msg)
    root.after(delay, lambda: status_label.config(text=""))

# Function to create guess grid
def create_grid():
    global labels, keyword

    grid_frame = Frame(root)
    grid_frame.pack(anchor='n', pady=10)

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
        # print(f"Backspace pressed, guess: {guess}")
    elif key == "Return":
        if len(guess) == keyword_length:
            handle_guess()     # handle guess here
        else:
            show_message("Not enough letters")
            print("Not enough letters")             # should display popup saying this
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
    # Don't update the row colors if the word is not valid
    if guess in current_dictionary:
        keyword_letter_counts = Counter(keyword) # counter object creates a dictionary of letters as key and the count of each letter as values
        used_counts = Counter() # counter object for the user's guess
        
        for idx, letter in enumerate(guess):
            if letter == keyword[idx]:   # green square (letter in keyword + letter in correct position)
                labels[attempt][idx].config(bg="#538D4E")
                used_counts[letter] += 1  # will keep track of the letter count from the user's guess  
            else:                                   
                labels[attempt][idx].config(bg="#3A3A3C") # not in keyword
        
        for idx, letter in enumerate(guess):
            if letter != keyword[idx] and letter in keyword: 
                if used_counts[letter] < keyword_letter_counts[letter]:
                    labels[attempt][idx].config(bg="#B59F3B") # yellow square (letter in keyword but NOT in correct position)
                    used_counts[letter] += 1
                

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

def show_end_popup(message):
    popup = Toplevel(root)
    popup.title("Game Over")
    popup.geometry("300x200")
    popup.grab_set() 

    Label(popup, text=message, font=("Helvetica", 16), wraplength=250, pady=20).pack()

    def quit_game():
        root.destroy()

    def restart_game():
        popup.destroy()
        for widget in root.winfo_children():
            widget.destroy()
        game()

    Button(popup, text="Play Again", command=restart_game, font=("Helvetica", 14), bg="green", fg="black").pack(pady=5)
    Button(popup, text="Quit", command=quit_game, font=("Helvetica", 14), bg="red", fg="black").pack(pady=5)

# Handle row guess
def handle_guess():
    global guess, attempt, keyword
    handle_row(guess)
    update_keyboard(guess)

    attempts_left = True

    if attempt == 5:
        attempts_left = False

    if guess == keyword and attempt != 5:
        attempt += 1

        # Start the next round and increase the word length
        start_round(increase=attempts_left)
        return
    
    elif guess == keyword and attempt == 5:
        show_end_popup(f"You solved it!")

    elif guess not in current_dictionary:
        show_message("Not in word list")

    elif attempt >= 5 and guess != keyword:
        show_end_popup(f"You lose!\nThe word was {keyword.upper()}")

    elif guess == keyword and keyword_length == 9:
        show_end_popup("You Win")

    else:
        print(f"{attempt}: New guess: {guess}") 
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
        
def start_round(increase=False):

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

    for widget in root.winfo_children():
        widget.destroy()
    create_status_label()
    create_grid()
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