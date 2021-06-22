from tkinter import *
import numpy as np
import cv2
import colorsys


#global variable to keep track of the row we are on
cur_row = 0

'''
    Click action for each of the 'enter' buttons

    If a color is entered correctly, the background 
    of the text box will change

    if it's entered correctly and it's the last entry
    box in the window, another box will be generated

    TODO: make sure non-hex values can't be passed

'''
def entry_button_clicked(this_row):
    global cur_row

    # set background of entry box
    entries[this_row].configure(bg=entries[this_row].get())

    if(this_row != cur_row):
        return

    # increment through the program
    cur_row = cur_row + 1

    # add buttons and entry boxes
    entries.append(Entry(window,width=17))
    entries[cur_row].grid(column=0,row=cur_row+1)

    buttons.append(Button(window, text="Enter",command=lambda i=this_row+1: entry_button_clicked(i)))
    buttons[cur_row].grid(column=1,row=cur_row+1)

    # moves the generate area button down the grid
    generate_label.grid(column=0,row=cur_row+2)
    generate_entry.grid(column=0,row=cur_row+3)
    generate_button.grid(column=1,row=cur_row+3)

'''
    gets the values from the entered entries and 
    return them as an array of np arrays that contain
    the RGB values from the entries
'''
def get_values():
    values = []
    for i in range(cur_row):
        color = entries[i].get()[1:]
        values.append(np.array([int(color[j:j+2],16) for j in range(0,6,2)]))
    return values

def generate_button_clicked():
    colors = get_values()

    image = np.zeros((4,len(colors),3),np.uint8)

    for x in range(len(colors)):
        colorHSV = np.asarray(colorsys.rgb_to_hsv(colors[x][0],colors[x][1],colors[x][2]))
        diff = colorHSV[1] / 4.0
        saturation = colorHSV[1]
        for y in range(4):
            colorHSV[1] = saturation - (diff*y)
            #convert from HSV->RGB->GBR
            colorGBR = np.flip(np.array(colorsys.hsv_to_rgb(colorHSV[0],colorHSV[1],colorHSV[2])),0)
            colorGBR = [abs(int(val)) for val in colorGBR]
            image[y,x] = colorGBR

    cv2.imwrite(generate_entry.get()+".png",image)

# initialize button/entries array
entries = []
buttons = []

# create window and adjust settings
window = Tk()
window.title("Pallet Generator")
window.geometry('200x400')

# print text at the top of the window
lbl = Label(window, text="Enter Color Hex Values:")
lbl.grid(column=0,row=0)

# add first entry/button
entries.append(Entry(window,width=17))
entries[cur_row].grid(column=0,row=cur_row+1)

buttons.append(Button(window, text="Enter",command=lambda i=cur_row: entry_button_clicked(i)))
buttons[cur_row].grid(column=1,row=cur_row+1)

# add finename and generate buttons/text/entry
generate_label = Label(window,text="filename: (*.png)")
generate_label.grid(column=0,row=cur_row+2)

generate_entry = Entry(window,width=17)
generate_entry.grid(column=0,row=cur_row+3)

generate_button = Button(window, text="Generate", command=generate_button_clicked)
generate_button.grid(column=1,row=cur_row+3)


window.mainloop()
