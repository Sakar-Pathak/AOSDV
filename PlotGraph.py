import matplotlib.pyplot as plt

import matplotlib.animation as animation

from matplotlib import style
from matplotlib.widgets import Button
from matplotlib.widgets import CheckButtons
from matplotlib.widgets import Slider

from tkinter import filedialog


import DBMS

style.use('seaborn-whitegrid')

fig = plt.figure()
ax = plt.axes()

ax.grid(which='major', linewidth='0.5', color='black', alpha=1)  # Customize the major grid
ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black', alpha=1)  # Customize the minor grid


class makeGraph:

    def __init__(self, aosdv_type, shared_data_supervisor, shared_data_time, shared_data_head, shared_data_pitch, shared_data_roll):

        self.aosdv_type = aosdv_type

        self.shared_data_supervisor = shared_data_supervisor

        self.shared_data_time = shared_data_time
        self.shared_data_head = shared_data_head
        self.shared_data_pitch = shared_data_pitch
        self.shared_data_roll = shared_data_roll

        self.lines_visibility = [True, True, True]  # it is a self variable for regulating visibility of lines. initializing all the lines to visible

        self.supervisor = 'stop'  # it is a self variable for regulating start, stop and clearing of the lines

        self.gridregulator = False  # it is a self variable for regulating minor grids

        # initializing the slider_x_value
        self.slider_x_value = 0

    def animate(self, i):
        self.shared_data_supervisor[0] = self.supervisor

        ax.minorticks_on() if self.gridregulator else ax.minorticks_off()  # turning on and off the minorticks(minorgrids) according to the value of self.gridregulator

        if self.supervisor == 'stop':
            return  # if the stop button is pressed then the animate function returns without updating the axis

        if self.supervisor == 'clear':
            ax.clear()
            return  # if the clear button is pressed then the animate function return by clearing the datas

        self.length_x_vals = len(self.shared_data_time)  # storing the length of self variable x_vals to another self variable length_x_vals for further use

        ax.clear()  # clearing the axes before updating

        ax.minorticks_on() if self.gridregulator else ax.minorticks_off()  # turning on and off the minorticks(minorgrids) according to the value of self.gridregulator after the axes is cleared

        # plotting the lines into the axes and giving each line a name
        lhead, = ax.plot(self.shared_data_time[0:self.length_x_vals], self.shared_data_head[0:self.length_x_vals],
                         '-bo', lw=1, label='Head', visible=self.lines_visibility[0])
        lpitch, = ax.plot(self.shared_data_time[0:self.length_x_vals], self.shared_data_pitch[0:self.length_x_vals],
                          '-go', lw=1, label='Pitch', visible=self.lines_visibility[1])
        lroll, = ax.plot(self.shared_data_time[0:self.length_x_vals], self.shared_data_roll[0:self.length_x_vals],
                         '-ro', lw=1, label='Roll', visible=self.lines_visibility[2])

        # storing the lines into a self variable list
        self.lines = [lhead, lpitch, lroll]
        if self.length_x_vals > 0:
            self.set_x_limits()

    def get_slider_x_value(self, val):
        self.slider_x_value = val
        self.set_x_limits()

    def set_x_limits(self):
        out_min = self.shared_data_time[0]  # min output value
        out_max = self.shared_data_time[self.length_x_vals - 2]  # max output value
        x_left_limit = self.slider_x_value * (out_max - out_min) / 90 + out_min  # left limit of x axis
        x_right_limit = self.shared_data_time[self.length_x_vals - 1]  # right limit of x axis
        ax.set_xlim(x_left_limit, x_right_limit)

    def set_lines_visible(self, label):  # it takes label of the button clicked as argument
        index = ['Head', 'Pitch', 'Roll'].index(
            label)  # getting corresponging number of label i.e 0, 1 and 2 for Head, Pitch and Roll
        self.lines_visibility[index] = not self.lines_visibility[
            index]  # if button is clicked then corresponding lines visibility is toggled. It is required while axes is being cleared and updated
        self.lines[index].set_visible(not self.lines[index].get_visible())  # toggling lines visibility
        plt.draw()  # updating the graph when the visibility is toggled

    def grid_regulator(self, label):
        self.gridregulator = not self.gridregulator

    def _start(self, event):
        self.supervisor = 'start'

    def _stop(self, event):
        self.supervisor = 'stop'

    def _clear(self, event):
        self.supervisor = 'clear'

    def save_file(self, event):
        if self.supervisor == 'stop':
            f = filedialog.asksaveasfile(mode='w', defaultextension='.csv')

            if f is None:
                return

            f.write('Time')
            f.write(',')
            f.write('Head')
            f.write(',')
            f.write('Pitch')
            f.write(',')
            f.write('Roll' + '\n')

            for count in self.shared_data_time[0:self.length_x_vals]:
                try:
                    f.write(str(self.shared_data_time[count]))
                    f.write(',')
                    f.write(str(self.shared_data_head[count]))
                    f.write(',')
                    f.write(str(self.shared_data_pitch[count]))
                    f.write(',')
                    f.write(str(self.shared_data_roll[count]) + '\n')
                except(IndexError, ValueError):
                    print("error saving file")
                    break

            f.close()
            print("FILE IS SUCCESSFULLY SAVED LOCALLY !!!!")

    def save_to_database(self, event):
        if self.supervisor == 'stop' and self.aosdv_type["streamer_DB"]:
            DBMS.dbms.initialize()
            data = []

            for time, yaw, pitch, roll in zip(self.shared_data_time[0:self.length_x_vals],
                                              self.shared_data_head[0:self.length_x_vals],
                                              self.shared_data_pitch[0:self.length_x_vals],
                                              self.shared_data_roll[0:self.length_x_vals]):
                data.append((time, yaw, pitch, roll))
            DBMS.dbms.save_to_database(data)
            print("SUCCESSFULLY SAVED TO DATABASE")

        else:
            print("YOU HAVE NO ACCESS TO SAVE TO DATABASE!!!!!!!!!")


def PlotGraph_process(aosdv_type, shared_data_supervisor, shared_data_time, shared_data_head, shared_data_pitch, shared_data_roll):
    makegraph = makeGraph(aosdv_type, shared_data_supervisor, shared_data_time, shared_data_head, shared_data_pitch,
                          shared_data_roll)

    ani = animation.FuncAnimation(fig, makegraph.animate,
                                  interval=100)  # it calls the animate function under the object makegraph after each 1ms interval

    # checkbuttons for toggling visibility head, pitch and roll lines
    lines_labels = ['Head', 'Pitch', 'Roll']  # label corresponding to each lines
    lines_activated = [True, True, True]  # initially all the lines visibility is true
    lines_checkButton = plt.axes([0.96, 0.90, 0.04, 0.07])  # position of the checkbuttons
    lineschxbox = CheckButtons(lines_checkButton, lines_labels, lines_activated)
    lineschxbox.on_clicked(makegraph.set_lines_visible)

    # checkbutton for turning on and off the minorgrids
    minorgrids_labels = ['Minor Grid']
    minorgrids_activated = [False]
    minorgrids_CheckButton = plt.axes([0.93, 0.97, 0.08, 0.03])
    minorgridschxbox = CheckButtons(minorgrids_CheckButton, minorgrids_labels, minorgrids_activated)
    minorgridschxbox.on_clicked(makegraph.grid_regulator)

    # start button
    start = plt.axes([0.8, 0.0, 0.05, 0.03])
    startbutton = Button(start, 'START', color='green', hovercolor='gray')
    startbutton.on_clicked(makegraph._start)
    startbutton.label.set_fontsize(7)

    # stop button
    stop = plt.axes([0.9, 0.0, 0.05, 0.03])
    stopbutton = Button(stop, 'STOP', color='red', hovercolor='gray')
    stopbutton.on_clicked(makegraph._stop)
    stopbutton.label.set_fontsize(7)

    # clear button
    clear = plt.axes([0.7, 0.0, 0.05, 0.03])
    clearbutton = Button(clear, 'CLEAR', color='yellow', hovercolor='gray')
    clearbutton.on_clicked(makegraph._clear)
    clearbutton.label.set_fontsize(7)

    # save button
    save = plt.axes([0.10, 0.0, 0.05, 0.03])
    savebutton = Button(save, 'SAVE', color='cyan', hovercolor='gray')
    savebutton.on_clicked(makegraph.save_file)
    savebutton.label.set_fontsize(7)

    # save to database button
    save = plt.axes([0.01, 0.0, 0.05, 0.03])
    savebutton = Button(save, 'SAVE TO DB', color='#e28743', hovercolor='gray')
    savebutton.on_clicked(makegraph.save_to_database)
    savebutton.label.set_fontsize(7)

    # slider for regulating x_lim i.e regulating x axis
    sliderX_location = plt.axes([0.2, 0.01, 0.4, 0.02], facecolor='lightgoldenrodyellow')
    sliderX = Slider(sliderX_location, 'Slider', 0, 90,
                     valinit=0)  # lowerlimit = 0 and upperlimit = 90 and initialPosition = 0
    sliderX.on_changed(makegraph.get_slider_x_value)  # calls the get_slider_x_value function if the sliderX is changed

    # turn the full screen mode on
    # mng = plt.get_current_fig_manager()
    # mng.window.state("zoomed")  # displaying in zoomed mode

    plt.subplots_adjust(left=0.02, right=1, top=1, bottom=0.05)  # adjusting the axes dimension

    plt.show()
