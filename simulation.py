import tkinter as tk
import turtle
from threading import Thread
import math

# TODO tkinter initial positions/color customization, dt?

G = 6.674 * 10e-11

STRETCH = 0.01

class Planet:
    def __init__(self, pos: list[float], vel: list[float], mass: float, canvas: tk.Canvas) -> None:
        self._pos = pos
        self._vel = vel
        self._acc = [0, 0, 0]
        self._mass = mass
        self._turtle = turtle.RawTurtle(canvas, shape="circle")
        self._turtle.color("white")
        self._turtle.speed("fastest")
        self._turtle.penup()
        self._turtle.goto(self._pos[0], self._pos[1])
        self._turtle.pendown()


    @property
    def pos(self) -> list[float]:
        return self._pos


    @pos.setter
    def pos(self, newpos: list[float]) -> None:
        self._pos = newpos
        self._turtle.goto(newpos[0], newpos[1])

        sigbase = (lambda z: 1/(1+math.exp(-STRETCH*z)))(newpos[2])
        r_val = sigbase
        g_val = sigbase
        b_val = sigbase*(-1)+1

        self._turtle.color((r_val, g_val, b_val))


    @property
    def vel(self) -> list[float]:
        return self._vel


    @vel.setter
    def vel(self, newvel: list[float]) -> None:
        self._vel = newvel


    @property
    def acc(self) -> list[float]:
        return self._acc


    @acc.setter
    def acc(self, newacc: list[float]) -> None:
        self._acc = newacc


    @property
    def mass(self) -> float:
        return self._mass


    def calculate_distance_vector(self, other: "Planet") -> list[float]:
        return [self._pos[i]-other.pos[i] for i in range(len(self._pos))]


    def gravitational_force(self, other: "Planet") -> list[float]:
        dist_vector = self.calculate_distance_vector(other)
        theta = math.atan(dist_vector[1] / (dist_vector[0] + 1e-9)) # angle of force vector in x y plane
 
        if vector_magnitude(dist_vector) == 0:
            grav_mag = 0
        else:
            grav_mag = (G * self._mass * other.mass) / (vector_magnitude(dist_vector)**2)
       
        phi = math.asin(dist_vector[2] / (vector_magnitude(dist_vector) + 1e-9)) # angle of force vector in x z plane

        grav_x = grav_mag*math.cos(theta)*math.cos(phi)
        grav_y = grav_mag*math.sin(theta)*math.cos(phi)
        grav_z = grav_mag*math.sin(phi)

        # clarify direction of components
        if self._pos[0] > other.pos[0]:
            grav_x = -abs(grav_x)
        if self._pos[0] < other.pos[0]:
            grav_x = abs(grav_x)
        if self._pos[1] > other.pos[1]:
            grav_y = -abs(grav_y)
        if self.pos[1] < other.pos[1]:
            grav_y = abs(grav_y)
        if self._pos[2] > other.pos[2]:
            grav_z = -abs(grav_z)
        if self._pos[2] < other.pos[2]:
            grav_z = abs(grav_z)

        # collision detection
        if vector_magnitude(dist_vector) < 5:
            grav_x, grav_y, grav_z = 0, 0, 0
        
        return([grav_x, grav_y, grav_z])


def update(planets: list[Planet], dt: float) -> None:
    for i in range(len(planets)):
        forces = [0, 0, 0]
        for j in range(len(planets)):
            if i != j:
                forces = list(map(sum, zip(forces, planets[i].gravitational_force(planets[j]))))
        planets[i].acc = [f / planets[i].mass for f in forces]

        planets[i].vel = [
            planets[i].vel[0] + dt * planets[i].acc[0],
            planets[i].vel[1] + dt * planets[i].acc[1],
            planets[i].vel[2] + dt * planets[i].acc[2]
        ]

    # update pos AFTER acc and vel because they are dependant on pos
    for i in range(len(planets)):
        planets[i].pos = [
            planets[i].pos[0] + dt * planets[i].vel[0],
            planets[i].pos[1] + dt * planets[i].vel[1],
            planets[i].pos[2] + dt * planets[i].vel[2]
        ]


def vector_magnitude(v: list[float]) -> float:
    return sum([s * s for s in v]) ** 0.5


def run(planets: list[Planet]) -> None:
    while True:
        dt = 0.01
        update(planets, dt)


def main() -> None:
    root = tk.Tk()
    root.title ("Body Simulation")
    root.resizable(0, 0)
    
    canvas = tk.Canvas(root, width=900, height=900)
    canvas.pack()
    
    planet1 = Planet(pos=[-100, 0, 0], vel=[34.71128135672417, 53.2726851767674, 0], mass=1e15, canvas=canvas)
    planet2 = Planet(pos=[0, 10, 50], vel=[0, 0, 19], mass=1.5e15, canvas=canvas)
    planet3 = Planet(pos=[100, 0, 0], vel=[-30, -50, 0], mass=1e15, canvas=canvas)

    #planet1 = Planet(pos=[-300, 300, 50], vel=[10, 10, -10], mass=1e15, canvas=canvas)
    #planet2 = Planet(pos=[0, 100, 30], vel=[0, 0, 0], mass=1e15, canvas=canvas)
    #planet3 = Planet(pos=[-100, 150, 0], vel=[5, 5, 0], mass=1e15, canvas=canvas)
    planets = [planet1, planet2, planet3]
    
    canvas.configure(bg="black")
    
    thread = Thread(target=run, args = (planets,))
    thread.start()
    
    root.mainloop()
    
if __name__ == "__main__":
    main()
