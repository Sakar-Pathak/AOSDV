import matplotlib.pyplot as plt

import matplotlib.animation as animation

from matplotlib import style
from matplotlib.widgets import Button
from matplotlib.widgets import CheckButtons
from matplotlib.widgets import Slider

from tkinter import filedialog

import DBMS

import ast

style.use('seaborn-whitegrid')

fig = plt.figure()
ax = plt.axes()


ax.grid(which='major', linewidth='0.5', color='black', alpha=1)  # Customize the major grid
ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black', alpha=1)  # Customize the minor grid


class makeGraph:

    def __init__(self, aosdv_type, shared_data_supervisor, shared_data_time, shared_data_yaw, shared_data_pitch,
                 shared_data_roll, shared_data_quatW, shared_data_quatX, shared_data_quatY, shared_data_quatZ,
                 shared_data_temp1, shared_data_temp2, shared_data_emf1, shared_data_emf2):

        self.aosdv_type = aosdv_type

        self.shared_data_supervisor = shared_data_supervisor

        self.shared_data_time = shared_data_time

        self.shared_data_yaw = shared_data_yaw
        self.shared_data_pitch = shared_data_pitch
        self.shared_data_roll = shared_data_roll

        self.shared_data_quatW = shared_data_quatW
        self.shared_data_quatX = shared_data_quatX
        self.shared_data_quatY = shared_data_quatY
        self.shared_data_quatZ = shared_data_quatZ

        self.shared_data_temp1 = shared_data_temp1
        self.shared_data_temp2 = shared_data_temp2

        self.shared_data_emf1 = shared_data_emf1
        self.shared_data_emf2 = shared_data_emf2

        self.lines_visibility = [True, True, True, True, True, True, True, True, True, True,
                                 True]  # it is a self variable for regulating visibility of lines. initializing all the lines to visible

        self.supervisor = 'stop'  # it is a self variable for regulating start, stop and clearing of the lines

        self.gridregulator = False  # it is a self variable for regulating minor grids

        # initializing the slider_x_value
        self.slider_x_value = 0

        self.ani = animation.FuncAnimation(fig, self.animate,
                                      interval=1000)  # it calls the animate function under the object makegraph after each 1ms interval

    def animate(self, i):
        self.shared_data_supervisor[0] = self.supervisor

        ax.minorticks_on() if self.gridregulator else ax.minorticks_off()  # turning on and off the minorticks(minorgrids) according to the value of self.gridregulator

        if self.supervisor == 'stop':
            return  # if the stop button is pressed then the animate function returns without updating the axis

        if self.supervisor == 'clear':
            ax.clear()
            return  # if the clear button is pressed then the animate function return by clearing the datas

        self.length_x_vals = len(
            self.shared_data_emf2)  # storing the length of self variable data_emf2 to another self variable length_x_vals for further use

        ax.clear()  # clearing the axes before updating

        ax.minorticks_on() if self.gridregulator else ax.minorticks_off()  # turning on and off the minorticks(minorgrids) according to the value of self.gridregulator after the axes is cleared

        # plotting the lines into the axes and giving each line a name
        lyaw, = ax.plot(self.shared_data_time[0:self.length_x_vals], self.shared_data_yaw[0:self.length_x_vals],
                        '-bo', lw=1, label='Yaw', visible=self.lines_visibility[0])
        lpitch, = ax.plot(self.shared_data_time[0:self.length_x_vals], self.shared_data_pitch[0:self.length_x_vals],
                          '-go', lw=1, label='Pitch', visible=self.lines_visibility[1])
        lroll, = ax.plot(self.shared_data_time[0:self.length_x_vals], self.shared_data_roll[0:self.length_x_vals],
                         '-ro', lw=1, label='Roll', visible=self.lines_visibility[2])

        lquatW, = ax.plot(self.shared_data_time[0:self.length_x_vals], self.shared_data_quatW[0:self.length_x_vals],
                          '-co', lw=1, label='QuatW', visible=self.lines_visibility[3])
        lquatX, = ax.plot(self.shared_data_time[0:self.length_x_vals], self.shared_data_quatX[0:self.length_x_vals],
                          '-mo', lw=1, label='QuatX', visible=self.lines_visibility[4])
        lquatY, = ax.plot(self.shared_data_time[0:self.length_x_vals], self.shared_data_quatY[0:self.length_x_vals],
                          '-yo', lw=1, label='QuatY', visible=self.lines_visibility[5])
        lquatZ, = ax.plot(self.shared_data_time[0:self.length_x_vals], self.shared_data_quatZ[0:self.length_x_vals],
                          '-ko', lw=1, label='QuatZ', visible=self.lines_visibility[6])

        ltemp1, = ax.plot(self.shared_data_time[0:self.length_x_vals], self.shared_data_temp1[0:self.length_x_vals],
                          '-bo', lw=1, label='Temp1', visible=self.lines_visibility[7])
        ltemp2, = ax.plot(self.shared_data_time[0:self.length_x_vals], self.shared_data_temp2[0:self.length_x_vals],
                          '-go', lw=1, label='Temp2', visible=self.lines_visibility[8])

        lemf1, = ax.plot(self.shared_data_time[0:self.length_x_vals], self.shared_data_emf1[0:self.length_x_vals],
                         '-ro', lw=1, label='Emf1', visible=self.lines_visibility[9])
        lemf2, = ax.plot(self.shared_data_time[0:self.length_x_vals], self.shared_data_emf2[0:self.length_x_vals],
                         '-co', lw=1, label='Emf2', visible=self.lines_visibility[10])

        # storing the lines into a self variable list
        self.lines = [lyaw, lpitch, lroll, lquatW, lquatX, lquatY, lquatZ, ltemp1, ltemp2, lemf1, lemf2]
        if self.length_x_vals > 3:
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
        index = ['Yaw', 'Pitch', 'Roll', 'QuatW', 'QuatX', 'QuatY', 'QuatZ', 'Temp1', 'Temp2', 'Emf1', 'Emf2'].index(
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
            f.write('Yaw')
            f.write(',')
            f.write('Pitch')
            f.write(',')
            f.write('Roll')
            f.write(',')
            f.write('QuatW')
            f.write(',')
            f.write('QuatX')
            f.write(',')
            f.write('QuatY')
            f.write(',')
            f.write('QuatZ')
            f.write(',')
            f.write('Temp1')
            f.write(',')
            f.write('Temp2')
            f.write(',')
            f.write('Emf1')
            f.write(',')
            f.write('Emf2' + '\n')

            for count in range(self.length_x_vals):
                try:
                    f.write(str(self.shared_data_time[count]))
                    f.write(',')
                    f.write(str(self.shared_data_yaw[count]))
                    f.write(',')
                    f.write(str(self.shared_data_pitch[count]))
                    f.write(',')
                    f.write(str(self.shared_data_roll[count]))
                    f.write(',')
                    f.write(str(self.shared_data_quatW[count]))
                    f.write(',')
                    f.write(str(self.shared_data_quatX[count]))
                    f.write(',')
                    f.write(str(self.shared_data_quatY[count]))
                    f.write(',')
                    f.write(str(self.shared_data_quatZ[count]))
                    f.write(',')
                    f.write(str(self.shared_data_temp1[count]))
                    f.write(',')
                    f.write(str(self.shared_data_temp2[count]))
                    f.write(',')
                    f.write(str(self.shared_data_emf1[count]))
                    f.write(',')
                    f.write(str(self.shared_data_emf2[count]) + '\n')

                except(IndexError, ValueError):
                    print("error saving file")
                    break
                    f.close()
                    return

            f.close()
            print("FILE IS SUCCESSFULLY SAVED LOCALLY !!!!")


    def save_to_database(self, event):
        self.ani.event_source.stop()
        if self.supervisor == 'stop' and self.aosdv_type["streamer_DB"]:
            DBMS.dbms.initialize()
            streamer = []
            ypr = []
            quaternion = []
            temperature = []
            solar_voltage = []

            file = open("config/config.txt", "r")
            contents = file.read()
            dictionary = ast.literal_eval(contents)
            CreatedBy = dictionary["User"]
            DataName = dictionary["DataName"]
            Description = dictionary["Description"]
            file.close()

            streamer.append((CreatedBy, DataName, Description))

            for Time, Yaw, Pitch, Roll, QuatW, QuatX, QuatY, QuatZ, Temp1, Temp2, Emf1, Emf2 in zip(
                    self.shared_data_time[0:self.length_x_vals],
                    self.shared_data_yaw[0:self.length_x_vals],
                    self.shared_data_pitch[0:self.length_x_vals],
                    self.shared_data_roll[0:self.length_x_vals],
                    self.shared_data_quatW[0:self.length_x_vals],
                    self.shared_data_quatX[0:self.length_x_vals],
                    self.shared_data_quatY[0:self.length_x_vals],
                    self.shared_data_quatZ[0:self.length_x_vals],
                    self.shared_data_temp1[0:self.length_x_vals],
                    self.shared_data_temp2[0:self.length_x_vals],
                    self.shared_data_emf1[0:self.length_x_vals],
                    self.shared_data_emf2[0:self.length_x_vals]):
                ypr.append((CreatedBy, DataName, Time, Yaw, Pitch, Roll))
                quaternion.append((CreatedBy, DataName, Time, QuatW, QuatX, QuatY, QuatZ))
                temperature.append((CreatedBy, DataName, Time, Temp1, Temp2))
                solar_voltage.append((CreatedBy, DataName, Time, Emf1, Emf2))
            data = [streamer, ypr, quaternion, temperature, solar_voltage]


            if DBMS.dbms.save_to_database(data):   print("Successfully Saved To Database!!!")
            else: print("Error Saving To Database!!!")

        else:
            print("YOU HAVE NO ACCESS TO SAVE TO DATABASE!!!!!!!!!")

        self.ani.event_source.start()



def PlotGraph_process(aosdv_type, shared_data_supervisor, shared_data_time, shared_data_yaw, shared_data_pitch,
                      shared_data_roll, shared_data_quatW, shared_data_quatX, shared_data_quatY, shared_data_quatZ,
                      shared_data_temp1,
                      shared_data_temp2, shared_data_emf1, shared_data_emf2, ):

    makegraph = makeGraph(aosdv_type, shared_data_supervisor, shared_data_time, shared_data_yaw, shared_data_pitch,
                          shared_data_roll, shared_data_quatW, shared_data_quatX, shared_data_quatY, shared_data_quatZ,
                          shared_data_temp1,
                          shared_data_temp2, shared_data_emf1, shared_data_emf2)


    # checkbuttons for toggling visibility head, pitch and roll lines
    lines_labels = ['Yaw', 'Pitch', 'Roll', 'QuatW', 'QuatX', 'QuatY', 'QuatZ', 'Temp1', 'Temp2', 'Emf1',
                    'Emf2']  # label corresponding to each lines
    lines_activated = [True, True, True, True, True, True, True, True, True, True,
                       True]  # initially all the lines visibility is true
    lines_checkButton = plt.axes([0.95, 0.72, 0.06, 0.26])  # position of the checkbuttons
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
    save_database = plt.axes([0.01, 0.0, 0.05, 0.03])
    save_databasebutton = Button(save_database, 'SAVE TO DB', color='#e28743', hovercolor='gray')
    save_databasebutton.on_clicked(makegraph.save_to_database)
    save_databasebutton.label.set_fontsize(7)

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
