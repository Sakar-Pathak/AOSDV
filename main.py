import multiprocessing

from panda3d.core import loadPrcFile  # to load .prc file

loadPrcFile("config\config.prc")  # it contains configurational settings

from direct.showbase.ShowBase import ShowBase
from panda3d.core import Vec4  # it is a 4 dimensional vector
from panda3d.core import AmbientLight
from panda3d.core import DirectionalLight

import Menu
import SerialRead

import PlotGraph

import time


class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        self.models = Models()
        Menu.menu.second_frame(self)
        self.Head = 0.0
        self.Pitch = 0.0
        self.Roll = 0.0

        self.lighting()

    def lighting(self):
        ambientLight = AmbientLight("ambient light")
        ambientLight.setColor(Vec4(0.2, 0.2, 0.2, 1))
        self.ambientLightNodePath = render.attachNewNode(ambientLight)
        render.setLight(self.ambientLightNodePath)

        mainLight = DirectionalLight("main light")
        self.mainLightNodePath = render.attachNewNode(mainLight)
        # Turn it around by 45 degrees, and tilt it down by 45 degrees
        self.mainLightNodePath.setHpr(45, -45, 0)
        render.setLight(self.mainLightNodePath)

    def taskmanager(self):
        self.taskMgr.add(self.update, "update")

    def update(self, task):

        length_shared_data_time = len(shared_data_roll) - 1

        try:
            self.Head = shared_data_yaw[length_shared_data_time]
            self.Pitch = shared_data_pitch[length_shared_data_time]
            self.Roll = shared_data_roll[length_shared_data_time]



        except (IndexError, ValueError):
            return task.cont

        self.models.model.setHpr(self.Head, self.Pitch, self.Roll)
        return task.cont


class Models(Game):

    def __init__(self):
        pass

    def Rocket(self):
        game.second_screen.hide()
        game.taskmanager()
        self.model = loader.loadModel("assets/characters/untitld.dae")
        self.model.reparentTo(render)
        self.model.setPos(0, 0, 0)
        self.model.setScale(1, 1, 1)

    def Drone(self):
        game.second_screen.hide()
        game.taskmanager()
        self.model = loader.loadModel("models/misc/rgbCube")
        self.model.reparentTo(render)
        self.model.setPos(0, 0, 0)
        self.model.setScale(20, 20, 5)

    def SelfBalancingRobot(self):
        game.second_screen.hide()
        game.taskmanager()
        self.model = loader.loadModel("models/panda")
        self.model.reparentTo(render)
        self.model.setPos(0, 0, 0)

    def Cuboid(self):
        game.second_screen.hide()
        game.taskmanager()
        self.model = loader.loadModel("models/misc/rgbCube")
        self.model.reparentTo(render)
        self.model.setPos(0, 0, 0)
        self.model.setScale(20, 20, 5)



def CLI():
    temp = int(input("Enter:\n"
                     "1 --> Local\n"
                     "2 --> Read Data from Database\n"
                     "3 --> Read Live Data\n"
                     "4 --> Streamer with Database Access\n"
                     "5 --> Streamer without Database Access\n"))
    if temp < 1 or temp > 5:
        CLI()
        return

    if temp == 1:
        aosdv_type["local"] = True
        port_baud["port_baud"] = SerialRead.getport_baud()


    elif temp == 2:
        aosdv_type["recorded"] = True

    elif temp == 3:
        aosdv_type["reader"] = True

    else:
        aosdv_type["streamer"] = True
        port_baud["port_baud"] = SerialRead.getport_baud()

    if temp == 4:
        aosdv_type["streamer_DB"] = True


    SerialRead_process1.start()
    PlotGraph_process2.start()





if __name__ == '__main__':
    manager = multiprocessing.Manager()

    port_baud = manager.dict()

    shared_data_supervisor = manager.dict()
    shared_data_supervisor[0] = 'stop'

    aosdv_type = manager.dict()

    aosdv_type = {
        "local": False,
        "recorded": False,
        "reader": False,
        "streamer": False,
        "streamer_DB": False
    }


    shared_data_time = manager.list()
    shared_data_yaw = manager.list()
    shared_data_pitch = manager.list()
    shared_data_roll = manager.list()

    shared_data_quatW = manager.list()
    shared_data_quatX = manager.list()
    shared_data_quatY = manager.list()
    shared_data_quatZ = manager.list()


    shared_data_temp1 = manager.list()
    shared_data_temp2 = manager.list()

    shared_data_emf1 = manager.list()
    shared_data_emf2 = manager.list()

    SerialRead_process1 = multiprocessing.Process(target=SerialRead.data_management, args=(
        port_baud, aosdv_type, shared_data_supervisor, shared_data_time, shared_data_yaw, shared_data_pitch,
        shared_data_roll, shared_data_quatW, shared_data_quatX, shared_data_quatY, shared_data_quatZ, shared_data_temp1,
        shared_data_temp2, shared_data_emf1, shared_data_emf2,))

    PlotGraph_process2 = multiprocessing.Process(target=PlotGraph.PlotGraph_process, args=(
        aosdv_type, shared_data_supervisor, shared_data_time, shared_data_yaw, shared_data_pitch,
        shared_data_roll, shared_data_quatW, shared_data_quatX, shared_data_quatY, shared_data_quatZ, shared_data_temp1,
        shared_data_temp2, shared_data_emf1, shared_data_emf2,))


    CLI()

    game = Game()
    game.run()
