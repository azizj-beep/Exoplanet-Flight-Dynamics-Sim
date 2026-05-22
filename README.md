# Contributing to ExoAero Flight Engine

Thank you for your interest in contributing to ExoAero! This is an academic, open-source interplanetary flight physics simulator designed to model aerodynamic lift and variable gravity. We welcome developers, physicists, and students from around the world to help expand this engine.

## 🚀 How You Can Help

We are currently looking for contributions in the following advanced areas:

### 1. Propulsion Systems (`RocketPropulsion` Class)
* **Goal:** Implement a dynamic fuel consumption model where the aircraft's mass decreases over time as thrust is applied.
* **Physics:** $m(t) = m_0 - (\dot{m} \cdot t)$, where $\dot{m}$ is the fuel mass flow rate.

### 2. Advanced Aerodynamic Drag
* **Goal:** Upgrade the current simulation to compute full forward drag based on wing surface area, dynamic air density, and drag coefficient, impacting forward velocity over time.
* **Equation:** $F_{Drag} = \frac{1}{2} \cdot \rho \cdot v^2 \cdot C_D \cdot A$

### 3. Graphical UI Enhancements
* **Goal:** Improve the Tkinter GUI by adding real-time control sliders for thrust, pitch angle adjustments, and interactive planet preset buttons (e.g., Earth, Mars, Venus).

### 4. Code Optimization & Modern Integration
* **Goal:** Implement modern Runge-Kutta (RK4) numerical integration instead of the basic Euler method to prevent numerical drift in long flight simulations.

## 🛠️ Submission Process

1. **Fork the Repository:** Create your own copy of this project.
2. **Create a Feature Branch:** Build your updates on a separate branch (`git checkout -b feature/AmazingFeature`).
3. **Commit Your Changes:** Write clear, professional English commit messages.
4. **Push & Open a Pull Request:** Submit your code changes to the `main` branch for review.

*All mathematical code modifications must include academic comments reference.*
