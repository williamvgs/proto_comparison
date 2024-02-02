import tkinter.messagebox
import tkinter.filedialog
from tkinter import *
from jsonfile import readvalue
from PIL import ImageTk, Image
import mss

global clones, screenless
screenless = 0
clones = []
screens = False

#returns colors used in text 
def color(acttt, tt):
    if tt == 0 and acttt == 0:
        return "black"
    elif (tt != acttt and tt != "Max:1") or (tt == "Max:1" and acttt > 1):
        return "red"
    else:
        return "dark green"


def check_requirements(): 
    for thruster in thrusters:
        if thruster[0] != thruster[1]:
            print("something missing")
            return False
    return True


#Comfirmation pop up to delete all items in screen
def cls():
    global screenless
    if tkinter.messagebox.askokcancel('Clear screen?', 'All unsaved progress will be lost'):
        for clone in clones:
            delclone(clone[0], clone[1], clone[2])
        clones.clear()
        for i in thrusters:
            i[0] = 0
        screenless = 0
        validate()


def validate():
    global menucounter_4
    size = 18
    try:
        menucounter_4.place_forget()
    except NameError:
        pass

    for i, thruster in enumerate(thrusters):
        print(f"Thruster {i+1}: {thruster[0]}/{thruster[1]}, Color: {color(thruster[0], thruster[1])}")

    menucounter_1 = Label(framel, text=f"Azimuth: {thrusters[0][0]}/{thrusters[0][1]}", font=("", size), fg=color(thrusters[0][0], thrusters[0][1]), bg="grey")
    menucounter_1.place(relx=0.5, rely=0.15, anchor=CENTER)

    menucounter_2 = Label(framel, text=f"Tunnel: {thrusters[1][0]}/{thrusters[1][1]}", font=("", size), fg=color(thrusters[1][0], thrusters[1][1]), bg="grey")
    menucounter_2.place(relx=0.5, rely=0.2, anchor=CENTER, )

    menucounter_3 = Label(framel, text=f"split handle: {thrusters[2][0]}/{thrusters[2][1]}", font=("", size), fg=color(thrusters[2][0], thrusters[2][1]), bg="grey")
    menucounter_3.place(relx=0.5, rely=0.25, anchor=CENTER)

    menucounter_4 = Label(framel, text=f"screen: {thrusters[3][0]}/{thrusters[3][1]}", font=("", size), fg=color(thrusters[3][0], thrusters[3][1]), bg="grey")
    menucounter_4.place(relx=0.5, rely=0.3, anchor=CENTER)


def mkclone(img, x, y, xs, ys, offsetx, offsety, tt, screen):
    # tt = thruster type
    global screenless
    cloneimage = ImageTk.PhotoImage(Image.open(img).resize((xs, ys), Image.LANCZOS))
    cloneitem = Label(window, image=cloneimage, bd=0, cursor="fleur")
    cloneitem.place(x=x, y=y)
    cloneitem.bind("<B1-Motion>", lambda e: moveclone(cloneitem, offsetx, offsety))
    cloneitem.bind("<Button-3>", lambda e: delclone(cloneitem, tt, screen))
    cloneitem.image = cloneimage
    thrusters[tt][0] += 1
    if not screen:
        thrusters[3][1] = 1
        screenless += 1
    if tt == 2:
        thrusters[1][0] += 2
    clones.append([cloneitem, tt, screen])
    validate()

    # Print the name of the cloned item
    item_name = image_text_mapping.get(img, "Unknown Item")
    print(f"Cloned item: {item_name}")




#ensures that all items are inside the white middle screen and enables or disables the option to save (not working)
def all_items_inside_screen():
    screen_width = 800  # Set the width of the white screen
    for clone in clones:
        place_info = clone[0].place_info()
        if 'x' in place_info:
            x = int(place_info['x'])
            if not (0 <= x <= screen_width):
                return False
    print("TRUE")
    return True



#gives poissibility to delete items
def delclone(name, tt, screen):
    global screenless
    name.place_forget()
    thrusters[tt][0] -= 1
    if tt == 2:
        thrusters[1][0] -= 2
    if not screen:
        screenless -= 1
    if screenless < 1:
        thrusters[3][1] = "Max:1"
    validate()

#enables moving of control panels around
def moveclone(name, offsetx, offsety):
    x, y = window.winfo_pointerxy()
    x -= window.winfo_rootx()
    y -= window.winfo_rooty()
    name.place(x=x-offsetx, y=y-offsety)

#makes a screen shot of items and saves as png
def export(root):
    if check_requirements() and all_items_inside_screen():
        print("true")  # Check both requirements and item placement
        default_file_name = "Bridgedesign.png"
        file_name = tkinter.filedialog.asksaveasfilename(defaultextension=".png", initialfile=default_file_name)
        if file_name:
            root.lift()  # Raise the window to the top of the stacking order
            root.update()  # Refresh the state of the window
            x = root.winfo_x()
            y = root.winfo_y()
            width = root.winfo_width()
            height = root.winfo_height()
            offset = 210
            with mss.mss() as sct:
                sct_img = sct.grab({"left": x+offset, "top": y+30, "width": width-503, "height": height-80})

            mss_img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            mss_img.save(file_name)
    else:
        print("false")
        tkinter.messagebox.showinfo("Requirements Not Fulfilled or Items Outside Screen", "Please ensure all requirements are fulfilled and items are inside the screen before exporting.")


# values read from .json file
thrusters = list(readvalue())

window = Tk()
window.title("Bridge designer")
#picture list
images = ["assets/BC-5-panel-tunnel.png", 'assets/BC-5-panel-azimuth.png', 'assets/BC-5-panel-two-tunnels.png', 'assets/BC-5-panel-two-tunnels-dp.png', "assets/BC-5-panel-azimuth-wo-monitor.png", "assets/BC-5-panel-tunnel-wo-monitor.png", "assets/BC-5-panel-two-tunnels-wo-monitor.png", "assets/BC-5-common-monitor.png"]


#dictionary to make it possible for user to hover image and text is displayed
image_text_mapping = {
    "assets/BC-5-panel-tunnel.png": "Tunnel Panel",
    'assets/BC-5-panel-azimuth.png': "Azimuth Panel",
    'assets/BC-5-panel-two-tunnels.png': "Two Tunnels Panel",
    'assets/BC-5-panel-two-tunnels-dp.png': "Two Tunnels DP Panel",
    "assets/BC-5-panel-azimuth-wo-monitor.png": "Azimuth Without Monitor",
    "assets/BC-5-panel-tunnel-wo-monitor.png": "Tunnel Without Monitor",
    "assets/BC-5-panel-two-tunnels-wo-monitor.png": "Two Tunnels Without Monitor",
    "assets/BC-5-common-monitor.png": "Common Monitor Panel"
}

# makes window (almost) fullscreen
window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))

window.resizable(width=True, height=True)

# Content starts here
window.columnconfigure(2, weight=1)

#middle frame
new_frame = Frame(window, bg='white', width=800, height=window.winfo_screenheight())
new_frame.grid(row=0, column=1) 

#left frame
frame = Frame(window, bg='grey', width=200, height=window.winfo_screenheight())
frame.grid(row=0, column=0)
frame.grid_propagate(False)

#right frame
framel = Frame(window, bg='grey', width=300, height=window.winfo_screenheight())
framel.grid(row=0, column=3)
framel.grid_propagate(False)

#delete icon and function
clsimg = ImageTk.PhotoImage(Image.open("assets/cls dark.png").resize((20, 25), Image.LANCZOS))
clsicon = Label(window, image=clsimg, bd=0, cursor="hand2", bg="grey")
clsicon.place(x=175, y=25)
clsicon.bind("<Button-1>", lambda e: cls())

#Title configurations 
#right side
menutitle = Label(framel, text="Requirements", font=("", 16))
menutitle.place(relx=0.5, rely=0.05, anchor=CENTER)
#left side
menutitle = Label(frame, text="Control panels", font=("", 16))
menutitle.place(relx=0.5, rely=0.05, anchor=CENTER)

#Define where to set "export" button on screen
exportimg = ImageTk.PhotoImage(Image.open("assets/export.png").resize((30, 30), Image.LANCZOS))
exporticon = Label(framel, image=exportimg, bd=0, bg="grey",  cursor="hand2")
exporticon.place(anchor=CENTER, relx=0.1, rely=0.05)
exporticon.bind("<Button-1>", lambda e: export(window))

menuitem_list = []

#======= MAIN =========

def switch():
    global screens, menuitem_list, menuitem_8

    try:
        menuitem_8.place_forget()
    except NameError:
        pass

    # Forget placement of previous menu items
    for item in menuitem_list:
        item.place_forget()

    menuitem_list = []

    

    if screens := not screens:
        for i in range(4):
            menuimage = ImageTk.PhotoImage(Image.open(images[i]).resize((132, 100), Image.LANCZOS))
            menuitem = Label(frame, image=menuimage, bd=0, cursor="hand2")
            menuitem.place(relx=0.5, rely=0.15 * (i + 1), anchor=CENTER)
            menuitem.bind("<Button-1>", lambda e, index=i, has_monitor=True: mkclone(images[index], 40, 170 + 110 * index, 132, 100, 70, 50, index, has_monitor))
            menuitem.image = menuimage
            menuitem.bind("<Enter>", lambda e, text=image_text_mapping[images[i]]: text_label.config(text=text))
            menuitem.bind("<Leave>", lambda e: text_label.config(text=""))
            menuitem_list.append(menuitem)

        nextimg = ImageTk.PhotoImage(Image.open("assets/navarrow.png").resize((40, 40), Image.LANCZOS))
        nextpage = Label(frame, image=nextimg, bd=0, cursor="hand2", bg="grey")
        nextpage.bind("<Button-1>", lambda e: switch())
        nextpage.place(relx=0.4, rely=0.75)
        nextpage.image = nextimg

    else:
        for i in range(4, 8):
            menuimage = ImageTk.PhotoImage(Image.open(images[i]).resize((84, 100), Image.LANCZOS))
            menuitem = Label(frame, image=menuimage, bd=0, cursor="hand2")
            menuitem.place(relx=0.5, rely=0.15 * (i - 3), anchor=CENTER)
            menuitem.bind("<Button-1>", lambda e, index=i, has_monitor=False: mkclone(images[index], 60, 66 + 110 * (index - 4), 84, 100, 43, 50, index - 4, has_monitor))
            menuitem.image = menuimage
            menuitem.bind("<Enter>", lambda e, text=image_text_mapping[images[i]]: text_label.config(text=text))
            menuitem.bind("<Leave>", lambda e: text_label.config(text=""))
            menuitem_list.append(menuitem)

        nextimg = ImageTk.PhotoImage(Image.open("assets/navarrow.png").resize((40, 40), Image.LANCZOS).rotate(180))
        nextpage = Label(frame, image=nextimg, bd=0, cursor="hand2", bg="grey")
        nextpage.bind("<Button-1>", lambda e: switch())
        nextpage.place(relx=0.4, rely=0.75)
        nextpage.image = nextimg

    text_label = Label(frame, text="", font=("", 12), bd=0)


#content runs here
switch()
validate()
# Content ends here
window.mainloop()