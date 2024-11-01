import datetime
from json import dump
from os.path import exists
from string import ascii_letters
from tkinter import *
from tkinter import font as font

from tkcalendar import Calendar

import Events


class main:
    def __init__(self):
        self.window = Tk()
        self.event = Events.Events()
        self.name, self.date, self.time, self.tag = None, None, None, None
        self.font = font.Font(family="Times New Roman", size=17)

        register = Button(self.window, text="Register An Event", command=self.reg, height=3, width=15)
        register["font"] = self.font
        register.grid(column=0, row=2, pady=2, padx=2)

        delete = Button(self.window, text="Delete An Event", command=self.delEvent, height=3, width=15)
        delete["font"] = self.font
        delete.grid(column=0, row=4, pady=2, padx=2)

        check = Button(self.window, text="Check An Event", command=self.eventCheck, height=3, width=15)
        check["font"] = self.font
        check.grid(column=0, row=6, pady=2, padx=2)

        name = Label(text="Event Planner \n- AsianDude :D")
        name["font"] = self.font
        name.grid(column=3, row=4, columnspan=2, padx=50)

        self.window.geometry("450x307")
        self.window.resizable(False, False)
        self.window.title("Event Manager")
        self.window.mainloop()

    def reg(self):
        def save():
            self.name = nameEntry.get().replace(" ", "-")
            self.date = f"{dateEntry.selection_get().strftime('%Y-%m-%d')} {hrs.get()}:{mins.get()}"
            valid = True
            if self.name in ("", " "):
                valid = False
            for i in list(self.date):
                if i in ascii_letters:
                    valid = False
                    break
            if not valid:
                error = Toplevel(win)
                errorLabel = Label(error, text="Please enter Valid Values")
                errorLabel.pack()
            else:
                self.event.regEvent(self.name, self.date)
                win.destroy()

        win = Toplevel(self.window)

        n = Label(win, text="Name")
        n.grid(row=0, column=0, pady=2)

        nameEntry = Entry(win)
        nameEntry.grid(row=0, column=1, pady=2)

        c = Label(win, text="Date")
        c.grid(row=1, column=0, pady=2)

        dateEntry = Calendar(win, selectmode="day", mindate=datetime.datetime.now().date())
        dateEntry.grid(row=1, column=1, pady=2, rowspan=3, columnspan=3)

        hrs = StringVar()
        hrs.set("Hours")
        hrsOptions = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15",
                      "16", "17", "18", "19", "20", "21", "22", "23"]
        hours = OptionMenu(win, hrs, *hrsOptions)
        hours.grid(row=1, column=5, pady=2)

        mins = StringVar()
        mins.set("Minutes")
        minOptions = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15",
                      "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31",
                      "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47",
                      "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59"]
        minutes = OptionMenu(win, mins, *minOptions)
        minutes.grid(row=1, column=7, pady=2)

        get = Button(win, text="Submit", command=save)
        get.grid(row=2, column=6, pady=2)

    def delEvent(self):
        def delete():
            self.event.delEvent(f"{var.get().split()[0].upper()}_{var.get().split()[1] + ' ' + var.get().split()[2]}")
            win.destroy()

        win = Toplevel(self.window)

        eventList = self.event.getEventList()["Events"]
        eventList.sort(key=lambda j: j['date'])
        eList = [f"{i['name']} {i['date']}" for i in eventList]

        if len(eList) != 0:
            var = StringVar()
            var.set("Please choose an event")

            menu = OptionMenu(win, var, *eList)
            menu["font"] = self.font
            menu.pack()

            button = Button(win, text="Submit", command=delete)
            button["font"] = self.font
            button.pack()
        else:
            invalid = Label(win, text="No registered events!")
            invalid["font"] = self.font
            invalid.pack()

            button = Button(win, text="Enter", command=lambda: win.destroy())
            button["font"] = self.font
            button.pack()

    def eventCheck(self):
        def delete():
            def temp():
                self.event.delEvent(
                    f"{var.get().split()[0].upper()}_{var.get().split()[1] + ' ' + var.get().split()[2]}")

                resultWin.destroy()
                win.destroy()

            result = self.event.checkEvent(
                f"{var.get().split()[0].upper()}_{var.get().split()[1] + ' ' + var.get().split()[2]}")
            resultWin = Toplevel(win)
            if result:
                resultLabel = Label(resultWin, text="It is Coming Up")
            else:
                resultLabel = Label(resultWin, text="It has passed")
                delButton = Button(resultWin, command=temp)
                delButton.pack()
            resultLabel["font"] = self.font
            resultLabel.pack()

        win = Toplevel(self.window)

        eventList = self.event.getEventList()["Events"]
        eventList.sort(key=lambda j: j['date'])
        eList = [f"{i['name']} {i['date']}" for i in eventList]
        if len(eList) != 0:
            var = StringVar()
            var.set("Please choose an event")

            menu = OptionMenu(win, var, *eList)
            menu["font"] = self.font
            menu.pack()

            button = Button(win, text="Submit", command=delete)
            button["font"] = self.font
            button.pack()
        else:
            invalid = Label(win, text="No registered events!")
            invalid["font"] = self.font
            invalid.pack()

            button = Button(win, text="Enter", command=lambda: win.destroy())
            button["font"] = self.font
            button.pack()


if __name__ == "__main__":
    if not exists("events.json"):
        with open("events.json", "w") as x:
            dump({"Events": []}, x, indent=4)
    main = main()
