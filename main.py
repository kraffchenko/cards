from tkinter import *
import pandas
import pandas as pd

BACKGROUND = '#B1DDC6'
data = pandas.read_csv('data/flash cards.csv')
index = ''


def file_editor(eng, de):
    global german_words
    global data
    try:
        german_words = pandas.read_csv('data/german words.csv')
    except FileNotFoundError:
        german_words = pd.DataFrame(columns=['German', 'English'])
    finally:
        new_row = {'German': de,
                   'English': eng}
        german_words = pd.concat([german_words, pd.DataFrame([new_row])], ignore_index=True)
        german_words = german_words.to_csv('data/german words.csv', index=False)


def comparer():
    global index
    index = data['German'].sample()
    return index


index = comparer()


def accept():
    global index
    global data
    try:
        file_editor(data._get_value(index.index[0], 'English'), data._get_value(index.index[0], 'English'))
        data.drop(index.index[0], inplace=True)
        data.drop(data.filter(regex="Unname"), axis=1, inplace=True)
        data = data.to_csv('data/flash cards.csv', index=False)
        data = pandas.read_csv('data/flash cards.csv')
        comparer()
        window.after_cancel(window.after_idle(eng_changer))
        gr_changer(index)
        window.after(3000, eng_changer, index)
        print(data)
    except ValueError:
        window.destroy()


def skip():
    global index
    comparer()
    window.after_cancel(window.after_idle(eng_changer))
    gr_changer(index)
    window.after(3000, eng_changer, index)
    print(data)


window = Tk()
window.title('Flashy')
window.config(bg=BACKGROUND)

card_front = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND)
card_front_file = PhotoImage(file='images/card_front.png')
card_back_file = PhotoImage(file='images/card_back.png')
img = card_front.create_image(400, 263, image=card_front_file)
card_front.grid(row=0, column=0, columnspan=2, padx=50, pady=50)

deny_canvas = Canvas(width=100, height=99, highlightthickness=0, bg=BACKGROUND)
deny_button_img = PhotoImage(file='images/wrong.png')
deny_button = Button(deny_canvas, image=deny_button_img, bd=0, highlightthickness=0, command=skip)
deny_button.grid(row=1, column=0, padx=50)
deny_canvas.grid(row=1, column=0, padx=50, ipady=50)

accept_canvas = Canvas(width=100, height=99, highlightthickness=0, bg=BACKGROUND)
accept_button_img = PhotoImage(file='images/right.png')
accept_button = Button(accept_canvas, image=accept_button_img, bd=0, highlightthickness=0, command=accept)
accept_button.grid(row=1, column=1, padx=50)
accept_canvas.grid(row=1, column=1, padx=50, ipady=55)

lang = card_front.create_text(400, 150, text='German', font=('Ariel', 40, 'italic'), fill='black')
text = card_front.create_text(400, 263, text=index.values[0], font=('Ariel', 60, 'bold'), fill='black')


def eng_changer(ind):
    card_front.itemconfig(img, image=card_back_file)
    card_front.itemconfig(lang, text='English', fill='white')
    card_front.itemconfig(text, text=data._get_value(ind.index[0], 'English'), fill='white')


window.after(3000, eng_changer, index)


def gr_changer(ind):
    card_front.itemconfig(img, image=card_front_file)
    card_front.itemconfig(lang, text='German', fill='black')
    card_front.itemconfig(text, text=data._get_value(ind.index[0], 'German'), fill='black')


window.mainloop()