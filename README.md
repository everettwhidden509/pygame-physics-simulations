# pygame-physics-simulations
 A collection of 2D physics simulations made on Python using the Pygame library. These projects demonstrate the application of Newtonian Mechanics, vector mathematics, and numerical integration in software development.

## 1. Ball Drop & Gravitational Elasticity Simulator
This script models gravitational acceleration ($$g = \frac{G \cdot M}{R^2}$$) using the real-world mass and radius values of various celestial bodies. It calculates frame-by-frame velocity updates and incorporates kinetic energy dissipation (bounce elasticity) upon floor collision. 

## 2. N-Body Orbital Mechanics Simulation
An advanced orbital simulation that calculates the gravitational attraction between multiple bodies simultaneously in real-time. 

### Core Features & Engineering Extensions:
* **Vector Math Resolution:** Utilizes trigonometric functions to resolve total gravitational force vectors into component $X$ and $Y$ forces.
* **Dynamic Time Step Slider:** Implemented a custom interactive UI slider to control simulation speed using substep physics processing without breaking the mathematical integration loops.
* **Telemetry Metrics:** Displays real-time calculations tracking the exact number of planetary days passed for individual celestial bodies.

### Credits & Acknowledgments
* Base N-body simulation architecture inspired by [Tech With Tim's Planet Simulation Tutorial](http://www.youtube.com/watch?v=WTLPmUHTPqo).

### My Custom Extensions & Modifications:
* Time-step variable speed handling
* expanded astronomical datasets (Jupiter/Saturn)
* custom Pygame UI slider mechanics
