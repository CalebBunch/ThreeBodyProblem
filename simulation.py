import tkinter as tk
import turtle
import time
from threading import Thread
import math


G = 6.674 * 10e-11


class Planet:
    def __init__(self, pos: list[float], vel: list[float], mass: float, canvas: tk.Canvas) -> None:
        self._pos = pos
        self._pos_reset = pos
        self._vel = vel
        self._vel_reset = vel
        self._acc = [0, 0, 0]
        self._mass = mass
        self._turtle = turtle.RawTurtle(canvas, shape="circle")
        self._turtle.color("white")
        self._turtle.speed("fastest")
        self._turtle.penup()
        self._turtle.goto(self._pos[0], self._pos[1])
        self._turtle.pendown()

    def reset_turtle(self, canvas) -> None:
        self._turtle.reset()
        print(0)
        #self._turtle = turtle.RawTurtle(canvas, shape="circle")
        self._turtle.shape("circle")
        print(1)
        self._turtle.color("white")
        print(2)
        #self._turtle.speed("fastest")
        print(3)
        self._turtle.penup()
        print(4)
        self._turtle.goto(self._pos_reset[0], self._pos_reset[1])
        print(5)
        self._turtle.pendown()
        
        self._pos = self._pos_reset
        #self.pos = self._pos_reset
        self.vel = self._vel_reset
        self.acc = [0, 0, 0]

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
        theta = math.atan(dist_vector[1] / (dist_vector[0] + 1e-9)) # angle of force
        if vector_magnitude(dist_vector) == 0:
            gravity_mag = 0
        else:
            gravity_mag = (G * self._mass * other.mass) / (vector_magnitude(dist_vector)**2)
        
        grav_x = gravity_mag*math.cos(theta)
        grav_y = gravity_mag*math.sin(theta)

        if self._pos[0] > other.pos[0]:
            grav_x = -abs(grav_x)
        if self._pos[0] < other.pos[0]:
            grav_x = abs(grav_x)
        if self._pos[1] > other.pos[1]:
            grav_y = -abs(grav_y)
        if self.pos[1] < other.pos[1]:
            grav_y = abs(grav_y)

        if vector_magnitude(dist_vector) < 5:
            grav_x, grav_y = 0, 0
        
        #print(grav_x, grav_y)
        #print(dist_vector)
        return([grav_x, grav_y])

def update(planets: list[Planet], dt: float) -> None:
    for i in range(len(planets)):
        forces = [0, 0]
        for j in range(len(planets)):
            if i != j:
                forces = list(map(sum, zip(forces, planets[i].gravitational_force(planets[j]))))
        planets[i].acc = [f / planets[i].mass for f in forces]

        planets[i].vel = [
            planets[i].vel[0] + dt * planets[i].acc[0],
            planets[i].vel[1] + dt * planets[i].acc[1]
        ]

    for i in range(len(planets)):
        planets[i].pos = [
            planets[i].pos[0] + dt * planets[i].vel[0],
            planets[i].pos[1] + dt * planets[i].vel[1]
        ]

def vector_magnitude(v: list[float]) -> float:
    return sum([s * s for s in v]) ** 0.5

def run(planets: list[Planet]) -> None:
    t = time.clock_gettime(time.CLOCK_MONOTONIC)
    i = 0
    while True:
        #dt = time.clock_gettime(timewhite.CLOCK_MONOTONIC) - t  # in seconds
        dt = 0.01
        update(planets, dt)
        #t = time.clock_gettime(time.CLOCK_MONOTONIC)
        #i += 1
        #if i > 1:
        #    break

def r_key_pressed(event, planets, canvas) -> None:
    # canvas.delete("all")
    print('prepretest')
    for planet in planets:
        # planet._turtle.teleport(planet._pos_resemeratet[0], planet._pos_reset[1])
        # planet._turtle.clear()
        print('pretest')
        planet.reset_turtle(canvas) 
        print("test")

        

def main() -> None:
    root = tk.Tk()
    root.title ("Body Simulation")
    root.resizable(0, 0)
    
    canvas = tk.Canvas(root, width=900, height=900)
    canvas.pack()

    planet1 = Planet(pos=[-100, 0, 0], vel=[34.71128135672417, 53.2726851767674, 0], mass=1e15, canvas=canvas)
    planet2 = Planet(pos=[0, 0, 0], vel=[0, 0, 0], mass=1e15, canvas=canvas)
    planet3 = Planet(pos=[100, 0, 0], vel=[0, 0, 0], mass=1e15, canvas=canvas)
    planets = [planet1, planet2, planet3]
    
    root.bind("<r>", lambda event : r_key_pressed(event, planets=planets, canvas=canvas))
    
    canvas.configure(bg="black")
    
    thread = Thread(target=run, args = (planets,))
    thread.start()
    
    root.mainloop()
    
if __name__ == "__main__":
    main()
