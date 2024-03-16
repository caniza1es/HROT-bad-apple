import time
import keyboard
import pyMeow as pm

proc = pm.open_process("HROT.exe")

class Entity:
    def __init__(self, index):
        self.index = index
        self.health = 0x180F800 + index * 0x1C0
        self.x = 0x180F7DC + index * 0x1C0
        self.y = 0x180F7E0 + index * 0x1C0
        self.z = 0x180F7E4 + index * 0x1C0
        if index == 0:
            self.dx = 0xDE68F8
            self.dy = 0xDE68FC
            self.dz = 0xDE6900

    def get_orientation(self):
        return [pm.r_float(proc, self.dx), pm.r_float(proc, self.dy), pm.r_float(proc, self.dz)]

    def read_health(self):
        return pm.r_int(proc, self.health)

    def read_x(self):
        return pm.r_float(proc, self.x)

    def read_y(self):
        return pm.r_float(proc, self.y)

    def read_z(self):
        return pm.r_float(proc, self.z)

    def read_xyz(self):
        return [self.read_x(), self.read_y(), self.read_z()]

    def set_health(self, h):
        pm.w_int(proc, self.health, h)

    def set_x(self, x):
        pm.w_float(proc, self.x, x)

    def set_y(self, y):
        pm.w_float(proc, self.y, y)

    def set_z(self, z):
        pm.w_float(proc, self.z, z)

    def set_xyz(self, vec):
        x, y, z = vec
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
ents = [Entity(i) for i in range(n + 1)]
for i in ents:
    if i.index != 0:
        i.set_health(0)
ply = ents[0]
r = 2.5

count = 0
gridpos = [43.15075684, 3.125, 46.61097064]
playerorientation = ply.get_orientation()
width, height = (480, 360)
scale = 0.018

frames = [read_frame_data(f"precess/out{i + 1}.txt") for i in range(2191)]

dt = 0.096

print("fucking done")

while not keyboard.is_pressed("p"):
    pass

for frame in frames:
    for pixel in frame:
        pid, x, z = pixel
        x *= scale
        z *= scale
        cellpos = [gridpos[0] + x, gridpos[1], gridpos[2] + z]
        ents[pid].set_xyz(cellpos)
    time.sleep(dt)
    count += 1
    print(count)
