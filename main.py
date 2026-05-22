import math
import tkinter as tk

# =========================================================================
# 1. CELESTIAL BODY DEFINITION (CustomPlanet Class)
# =========================================================================
class CustomPlanet:
    def __init__(self, name, mass, radius, surface_density, molar_mass, temperature):
        self.name = name                  # Name of the planet
        self.mass = mass                  # Planet mass in kilograms (kg)
        self.radius = radius              # Planet radius in meters (m)
        self.rho_0 = surface_density      # Atmospheric density at surface (kg/m³)
        self.m_molar = molar_mass        # Molar mass of atmospheric gas (kg/mol)
        self.temp = temperature           # Surface temperature in Kelvin (K)
        self.G = 6.67430e-11              # Universal Gravitational Constant
        self.R_GAS = 8.314                # Universal Gas Constant

    def get_gravity(self, altitude):
        """Calculates dynamic gravity based on distance from the planet's center."""
        return (self.G * self.mass) / ((self.radius + altitude) ** 2)

    def get_atmospheric_density(self, altitude):
        """Calculates dynamic air density at a given altitude using the Barometric formula."""
        if self.rho_0 <= 0 or altitude < 0:
            return 0.0
        g = self.get_gravity(altitude)
        # Barometric equation: rho = rho0 * e^(-M*g*h / R*T)
        return self.rho_0 * math.exp((-self.m_molar * g * altitude) / (self.R_GAS * self.temp))


# =========================================================================
# 2. AIRCRAFT PROPERTIES & FLIGHT DYNAMICS (Airplane Class)
# =========================================================================
class Airplane:
    def __init__(self, mass, wing_area, initial_alt, forward_velocity):
        self.mass = mass                  # Total aircraft mass (kg)
        self.wing_area = wing_area        # Total wing surface area (m²)
        self.altitude = initial_alt       # Initial flight altitude (m)
        self.forward_vel = forward_velocity # Constant forward speed through the air (m/s)
        self.vertical_vel = 0.0           # Vertical speed (climbing or sinking rate)
        self.time = 0.0                   # Flight time clock
        self.cl = 1.2                     # Lift Coefficient (wing efficiency profile)

    def compute_next_frame(self, planet, dt=1.0):
        """Computes aerodynamics forces (Lift vs Weight) and updates flight state for the next second."""
        if self.altitude <= 0:
            return

        # A) Fetch environment properties at current altitude
        g = planet.get_gravity(self.altitude)
        density = planet.get_atmospheric_density(self.altitude)
        
        # B) Calculate Aerodynamic Lift Force: L = 0.5 * rho * v² * Cl * A
        f_lift = 0.5 * density * (self.forward_vel ** 2) * self.cl * self.wing_area
        
        # C) Calculate Gravitational Weight Force: W = m * g
        f_weight = self.mass * g
        
        # D) Apply Newton's Second Law for vertical acceleration (Net Force = Lift - Weight)
        f_net_vertical = f_lift - f_weight
        vertical_acceleration = f_net_vertical / self.mass

        # E) Numerical integration to update velocity and position for the next frame
        self.vertical_vel += vertical_acceleration * dt
        self.altitude += self.vertical_vel * dt
        self.time += dt

        # Crash check / ground collision safety
        if self.altitude < 0:
            self.altitude = 0.0
            self.vertical_vel = 0.0


# =========================================================================
# 3. GRAPHICAL USER INTERFACE & VISUAL PLOTTER (FlightSimulatorGUI Class)
# =========================================================================
class FlightSimulatorGUI:
    def __init__(self, planet, airplane):
        self.planet = planet
        self.airplane = airplane
        self.frame_count = 0
        
        # Setup Window
        self.root = tk.Tk()
        self.root.title(f"AeroFlight Physics Engine - Current Planet: {planet.name}")
        self.root.geometry("850x500")
        self.root.configure(bg="#1e1e1e")

        # Left Panel: Text Telemetry Console
        self.text_frame = tk.Frame(self.root, bg="#1a1a1a", bd=2, relief="groove")
        self.text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        self.title_label = tk.Label(self.text_frame, text="LIVE DATA TELEMETRY", font=("Courier", 14, "bold"), fg="#00ff00", bg="#1a1a1a")
        self.title_label.pack(anchor="w", padx=10, pady=5)

        self.console = tk.Text(self.text_frame, font=("Courier", 10), bg="#000000", fg="#00ff00", width=55, height=22)
        self.console.pack(padx=10, pady=5, fill="both", expand=True)
        
        # Headers inside text console
        headers = f"{'Frame':<7}{'Time':<8}{'Altitude':<14}{'V-Vel':<10}{'Status'}\n"
        self.console.insert(tk.END, headers + "-"*52 + "\n")

        # Right Panel: Radar Graphical Canvas
        self.canvas_frame = tk.Frame(self.root, bg="#1a1a1a", bd=2, relief="groove")
        self.canvas_frame.pack(side="right", fill="both", pady=10, padx=10)
        
        self.radar_label = tk.Label(self.canvas_frame, text="FLIGHT PATH RADAR PLOT", font=("Courier", 12, "bold"), fg="#00ff00", bg="#1a1a1a")
        self.radar_label.pack(pady=5)

        self.canvas = tk.Canvas(self.canvas_frame, width=300, height=400, bg="#000000", highlightbackground="#00ff00")
        self.canvas.pack(padx=10, pady=5)
        
        # Draw altitude markers on Canvas (0m to 40,000m grid lines)
        for h_marker in range(0, 40001, 10000):
            y_pixel = 400 - int((h_marker / 40000.0) * 360) - 20
            self.canvas.create_line(30, y_pixel, 300, y_pixel, fill="#333333", dash=(4, 2))
            self.canvas.create_text(20, y_pixel, text=f"{h_marker//1000}k", fill="#888888", font=("Courier", 8))

        # Start automatic 30-frame simulation loop
        self.run_simulation()
        self.root.mainloop()

    def run_simulation(self):
        if self.frame_count >= 30 or self.airplane.altitude <= 0:
            self.console.insert(tk.END, "-"*52 + "\n[Simulation Complete]")
            return

        self.frame_count += 1
        
        # 1. Compute Physics Data Frame
        self.airplane.compute_next_frame(self.planet, dt=1.0)
        
        # 2. Format and Append Written Text Frame
        if self.airplane.altitude == 0: status = "CRASH"
        elif self.airplane.vertical_vel > 0.1: status = "CLIMB"
        elif self.airplane.vertical_vel < -0.1: status = "DESCENT"
        else: status = "STABLE"

        row = f"#{self.frame_count:<6}{self.airplane.time:<8.1f}{self.airplane.altitude:<14.1f}{self.airplane.vertical_vel:<10.2f}{status}\n"
        self.console.insert(tk.END, row)
        self.console.see(tk.END)

        # 3. Draw Graphic Dot Frame on Canvas (Mapping Altitude 0-40,000m to Canvas Pixels)
        pixel_x = 40 + (self.frame_count * 8)
        pixel_y = 400 - int((self.airplane.altitude / 40000.0) * 360) - 20
        
        # Draw a bright green telemetry coordinate dot
        self.canvas.create_oval(pixel_x-3, pixel_y-3, pixel_x+3, pixel_y+3, fill="#00ff00", outline="")
        
        # Connect dots with a line to display the trajectory arc
        if hasattr(self, 'prev_x'):
            self.canvas.create_line(self.prev_x, self.prev_y, pixel_x, pixel_y, fill="#00ff00", width=2)
            
        self.prev_x = pixel_x
        self.prev_y = pixel_y

        # Call next frame after a delay (300 milliseconds)
        self.root.after(300, self.run_simulation)


# =========================================================================
# 4. EXECUTION ENTRY POINT
# =========================================================================
if __name__ == "__main__":
    print("=== AeroFlight Setup: Input Parameters in Terminal First ===")
    p_name = input("Enter Planet Name: ")
    p_mass = float(input("   Mass in kg (e.g., Earth is 5.97e24): "))
    p_radius = float(input("   Radius in meters (e.g., Earth is 6371000): "))
    p_density = float(input("   Surface Air Density in kg/m³ (Earth is 1.225): "))
    p_molar = float(input("   Atmosphere Molar Mass in kg/mol (Air is 0.028): "))
    p_temp = float(input("   Surface Temperature in Kelvin: "))
    f_speed = float(input("Enter Aircraft Forward Velocity (m/s): "))

    # Build objects and open the graphical workspace window
    custom_planet = CustomPlanet(p_name, p_mass, p_radius, p_density, p_molar, p_temp)
    test_plane = Airplane(mass=5000.0, wing_area=30.0, initial_alt=10000.0, forward_velocity=f_speed)
    
    print("\n[Opening Graphical Simulation UI Grid...]")
    FlightSimulatorGUI(custom_planet, test_plane)
