import tkinter as tk
import turtle
from threading import Thread
import math
from pathlib import Path


SAVE_PATH = Path("parameters.txt")
G = 6.674 * 10e-11
stretch = 0.01
save_bool = True


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

        sigbase = (lambda z: 1/(1+math.exp(-stretch*z)))(newpos[2])
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


def save_params(save_pos: list[list[float]], save_vel: list[list[float]], save_mass: list[float]) -> None:
    save = str(input("Would you like to save these parameters (y/n)? ")).lower()
    if "y" in save:
        with open(SAVE_PATH, "a") as f:
            data = []
            for i in range(len(save_mass)):
                data.append(",".join(map(str, save_pos[i])) + "|")
                data.append(",".join(map(str, save_vel[i])) + "|")
                data.append(str(save_mass[i]))
                if i != len(save_mass)-1:
                    data.append(":")
                else:
                    data.append("\n")

            f.write("".join(data))
    
    global save_bool
    save_bool = False


def main() -> None:
    root = tk.Tk()
    root.title ("Body Simulation")
    root.resizable(False, False)
    root.withdraw()
    
    canvas = tk.Canvas(root, width=900, height=900)
    canvas.pack()

    planets = []

    #ADD try/catch for user input
    load = str(input("Would you like to load parameters from the save file (y/n)? ")).lower()
    if "y" in load:
        index = int(input("Enter the line number for desired parameters: ")) - 1
        with open(SAVE_PATH, "r") as f:
            params = f.readlines()[index]
            saved_planets = params.split(":")
            for sp in saved_planets:
                p = sp.split("|")
                planet = Planet(pos=list(map(float, p[0].split(","))), vel=list(map(float, p[1].split(","))), mass=float(p[2]), canvas=canvas)
                planets.append(planet)
    else:
        num_planets = int(input("Enter number of planets: "))
        for i in range(num_planets):
            pos = [float(s) for s in str(input(f"Enter planet {i+1} initial position - ex: 100,-30,20 : ")).split(",")]
            vel = [float(v) for v in str(input(f"Enter planet {i+1} initial velocity - ex: 50,10,65.7 : ")).split(",")]
            mass = float(input(f"Enter planet {i+1} mass - ex: 1e15 : ")) 
       
            planet = Planet(pos=pos, vel=vel, mass=mass, canvas=canvas)
            planets.append(planet)

    global stretch
    stretch = float(input("Enter color stretch factor (0,1] - "))

    save_pos = []
    save_vel = []
    save_mass = []
    for planet in planets:
        save_pos.append(planet.pos)
        save_vel.append(planet.vel)
        save_mass.append(planet.mass)

    root.deiconify()
    canvas.configure(bg="black")
    
    run_thread = Thread(target=run, args = (planets,))
    run_thread.daemon = True
    run_thread.start()
  
    root.mainloop()
    
    save_thread = Thread(target=save_params, args=(save_pos, save_vel, save_mass,))
    save_thread.daemon = True
    save_thread.start()
    
    while save_bool: continue


if __name__ == "__main__":
    main()
