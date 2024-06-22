import tkinter as tk
import turtle
import time
from threading import Thread
import math

G = 6.674 * 10e-11


class Planet:

    def __init__(self, pos: list[float], vel: list[float], acc: list[float], mass: float, canvas: tk.Canvas):
        self._pos = pos
        self._vel = vel
        self._acc = acc
        self._mass = mass

        self._turtle = turtle.RawTurtle(canvas, shape='circle')
        self._turtle.speed("fastest")
        self._turtle.penup()
        self._turtle.goto(self._pos[0], self._pos[1])
        self._turtle.pendown()

# Position

    @property
    def pos(self) -> list[float]:
        return self._pos

    @pos.setter
    def pos(self, newpos: list[float]) -> None:
        self._pos = newpos
        self._turtle.goto(newpos[0], newpos[1])

# Velocity

    @property
    def vel(self) -> list[float]:
        return self._vel

    @vel.setter
    def vel(self, newvel: list[float]) -> None:
        self._vel = newvel

# Acceleration

    @property
    def acc(self) -> list[float]:
        return self._acc

    @acc.setter
    def acc(self, newacc: list[float]) -> None:
        self._acc = newacc


# Mass

    @property
    def mass(self) -> float:
        return self._mass

# Helpers
    def calculate_distance_vector(self, other: "Planet") -> list[float]:
        return [self._pos[0] - other.pos[0], self._pos[1] - other.pos[1]]

    def gravitational_force(self, other: "Planet") -> list[float]:
        dist_vector = self.calculate_distance_vector(other)
        theta = math.atan(dist_vector[1]/(dist_vector[0]+1e-9)) # angle of force
        if vector_magnitude(dist_vector) == 0:
            gravity_mag = 0
        else:
            gravity_mag = (G * self._mass * other.mass)/(vector_magnitude(dist_vector)**2)
        
        grav_x = gravity_mag*math.cos(theta)
        grav_y = gravity_mag*math.sin(theta)

        if self._pos[0] > other.pos[0]:
            grav_x *= -1
        if self._pos[1] > other.pos[1]:
            grav_y *= -1

        return([grav_x, grav_y])

def update(planets: list[Planet], dt: float) -> None:
    forces = [0, 0]
    for i in range(len(planets)):
        for j in range(len(planets)):
            if i != j:
                forces = list(map(sum, zip(forces, planets[i].gravitational_force(planets[j]))))
        planets[i].acc = [a / planets[i].mass for a in forces]

        planets[i].vel = [
            planets[i].vel[0] + dt * planets[i].acc[0],
            planets[i].vel[1] + dt * planets[i].acc[1],
            #planets[i].vel[2] + dt * planets[i].acc[2]
        ]

        
        planets[i].pos = [
            planets[i].pos[0] + dt * planets[i].vel[0],
            planets[i].pos[1] + dt * planets[i].vel[1],
            #planets[i].pos[2] + dt * planets[i].vel[2]
        ]
        

def vector_magnitude(v: list[float]) -> float:
    return sum([i*i for i in v])**0.5

def run(planets: list[Planet]) -> None:

    t = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
    i = 0
    while True:
        dt = time.clock_gettime_ns(time.CLOCK_MONOTONIC) - t  # in seconds
        update(planets, dt)
        t = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
        print(f"planet1: {planets[0].pos}")
        print(f"planet2: {planets[1].pos}")
        i += 1
        #if i > 50:
            #break


def main() -> None:

    #ADD tkinter
    root = tk.Tk()
    root.title ("Body Simulation")
    root.resizable(0, 0)
    canvas = tk.Canvas(root, width=900, height=900)
    canvas.pack()

    planet1 = Planet(pos=[50, 0, 0], vel=[0, 0, 0], acc=[0, 0, 0], mass=10, canvas=canvas)
    planet2 = Planet(pos=[-50, 0, 0], vel=[0, 0, 0], acc=[0, 0, 0], mass=10, canvas=canvas)
    planets = [planet1, planet2]

    time.sleep(0.5)

    thread = Thread(target=run, args = (planets,))
    thread.start()

    #canvas.configure(bg="black")
    root.mainloop()
    


if __name__ == "__main__":
    main()
