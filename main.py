from pymem import Pymem
import time
import keyboard

pm = Pymem("HROT.exe")

class Entity:
    def __init__(self,index):
        self.index = index
        self.health = 0x180F800+index*0x1C0
        self.x = 0x180F7DC+index*0x1C0
        self.y = 0x180F7E0+index*0x1C0
        self.z = 0x180F7E4+index*0x1C0
        if index == 0:
            self.dx = 0xDE68F8
            self.dy = 0xDE68FC
            self.dz = 0xDE6900
    def get_orientation(self):
        return [pm.read_float(self.dx), pm.read_float(self.dy),pm.read_float(self.dz)]

    def read_health(self):
        return pm.read_int(self.health)
    def read_x(self):
        return pm.read_float(self.x)
    def read_y(self):
        return pm.read_float(self.y)
    def read_z(self):
        return pm.read_float(self.z)
    def read_xyz(self):
        return [self.read_x(),self.read_y(),self.read_z()]
    
    def set_health(self,h):
        pm.write_int(self.health,h)
    def set_x(self,x):
        pm.write_float(self.x,x)
    def set_y(self,y):
        pm.write_float(self.y,y)
    def set_z(self,z):
        pm.write_float(self.z,z)
    def set_xyz(self,vec):
        x,y,z = vec
        self.set_x(x)
        self.set_y(y)
        self.set_z(z)

def read_frame_data(file_path):
    pixel_data = []
    with open(file_path, "r") as file:
        for line in file:
            points = line.strip().split(" ")
            for point in points:
                pid, xy = point.split(":")
                x, y = xy.split(",")
                pixel_data.append((int(pid), float(x), float(y)))
    return pixel_data

    
n = 49
ents = [Entity(i) for i in range(n+1)]
for i in ents:
    if i.index != 0:
        i.set_health(0)
ply = ents[0]
r=2.5

count = 0
playerpos = ply.read_xyz()
playerorientation = ply.get_orientation()
width,height = (480,360)
scale = 0.018


frames = [read_frame_data(f"precess/out{i+1}.txt") for i in range(2191)]

dt = 0

print("fucking done")



"""
width*=scale
height*=scale
offset_x = width/2
offset_z = height/2"""

for frame in frames:
    for pixel in frame:
        pid,x,z = pixel
        x*=scale
        z*=scale
        gridpos = playerpos#[playerpos[i]+playerorientation[i]*r for i in range(3)]
        cellpos = [gridpos[0]+x,gridpos[1],gridpos[2]+z]
        ents[pid].set_xyz(cellpos)
        time.sleep(dt)
    count+=1
    print(count)








