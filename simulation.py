import tkinter as tk
import turtle
import time


G = 6.674 * 10e-11


class Planet:

    def __init__(self, pos: list[float], vel: list[float], acc: list[float], mass: float):
        self._pos = pos
        self._vel = vel
        self._acc = acc
        self._mass = mass

# Position

    @property
    def pos(self) -> list[float]:
        return self._pos

    @pos.setter
    def pos(self, newpos: list[float]) -> None:
        self._pos = newpos

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

    def calculate_distance(self, other: "Planet", index: int) -> float:
        return ((self.pos[index] - other.pos[index])**2)**0.5

    def gravitational_force(self, other: "Planet") -> list[float]:
        forces = []
        for idx in range(len(self.pos)):
            forces.append(G * self.mass * other.mass /
                (self.calculate_distance(other, idx) + 1e-9)**2)
        return forces


def update(planets: list[Planet], dt: float):
    for i in range(len(planets)):
        for j in range(len(planets)):
            if i != j:
                forces = planets[i].gravitational_force(planets[j])
                planets[i].acc = [a / planets[i].mass for a in forces]
        planets[i].vel = [
            planets[i].vel[0] + dt * planets[i].acc[0],
            planets[i].vel[1] + dt * planets[i].acc[1],
            planets[i].vel[2] + dt * planets[i].acc[2]
        ]
        planets[i].pos = [
            planets[i].pos[0] + dt * planets[i].vel[0],
            planets[i].pos[1] + dt * planets[i].vel[1],
            planets[i].pos[2] + dt * planets[i].vel[2]
        ]


def main() -> None:
    planet1 = Planet(pos=[10, 7, 8], vel=[0, 0, 0], acc=[0, 0, 0], mass=4)
    planet2 = Planet(pos=[4, 1, 3], vel=[0, 0, 0], acc=[0, 0, 0], mass=12)
    planet3 = Planet(pos=[7, 4, 6], vel=[0, 0, 0], acc=[0, 0, 0], mass=7)
    planets = [planet1, planet2, planet3]

    #ADD tkinter
    root = tk.Tk()
    root.title ("Body Simulation")
    root.resizable(False, False)
    canvas = tk.Canvas(root, width=900, height=900)
    canvas.pack()

    p1 = turtle.RawTurtle(canvas, shape="circle")
    p2 = turtle.RawTurtle(canvas, shape="circle")
    p3 = turtle.RawTurtle(canvas, shape="circle")
    
    p1.color("red")
    p1.pendown()
    p1.forward(10)
    p1.goto(-10, 50)
    p1.penup()
    p1.goto(0, -50)

    p2.color("white")
    p2.setpos(20, 20)
    # p2.pendown()
    #p2.forward(100)
    


    """ 
    p3.color("green")
    p3.pendown()
    p3.forward(50)
    """
    canvas.configure(bg="black")
    root.mainloop()
    
    t = time.clock_gettime_ns(time.CLOCK_MONOTONIC) * 1e9

    while True:
        dt = time.clock_gettime_ns(time.CLOCK_MONOTONIC) * 1e9 - t  # in seconds

        update(planets, dt)
        #for i in range(len(planets)):
        #   print(f"Planet: {i} : {planets[i].pos}")

        t = time.clock_gettime_ns(time.CLOCK_MONOTONIC) * 1e9


if __name__ == "__main__":
    main()
