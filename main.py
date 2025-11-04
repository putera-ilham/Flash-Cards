from tkinter import *
import pandas
import random


BACKGROUND_COLOR = "#B1DDC6"
curr_card = {}
to_learn = {}

# ---------------------------- CATCHING EXCEPTIONS ------------------------------- #

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    ori_data = pandas.read_csv("data/french_words.csv")
    to_learn =  ori_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


# ---------------------------- SAVING PROGRESS ------------------------------- #

def is_known():
    to_learn.remove(curr_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)

    next_card()


# ---------------------------- CREATE NEW FLASH CARDS ------------------------------- #

def next_card():
    global curr_card, flip_timer
    window.after_cancel(flip_timer) # Cancels the timer when a new card is flipped
    curr_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=curr_card["French"], fill="black")
    canvas.itemconfig(card_bg, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card) # Once new card is flipped, timer starts again

# ---------------------------- CARDS FLIPPING ------------------------------- #
def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=curr_card["English"], fill="white")
    canvas.itemconfig(card_bg, image=card_back_img)


# ---------------------------- UI SETUP ------------------------------- #

### --- WINDOW --- ###
window = Tk()
window.title("Flasher")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

### --- CANVAS --- ###
canvas = Canvas(width=800,height=526)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_bg = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

### --- BUTTONS --- ###
cross_img = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_img, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

tick_img = PhotoImage(file="images/right.png")
known_button = Button(image=tick_img, highlightthickness=0, command=next_card)
known_button.grid(row=1, column=1)

next_card()






window.mainloop()