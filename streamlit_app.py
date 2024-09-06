import tkinter as tk
import tkinter.font as font
import math

# Constants
GRAVITY = 196.2  # Studs/second^2
CHARGE_VELOCITIES = [720, 780, 840, 900, 960]  # Velocities for C0 to C4 in Studs/Second
MAX_ANGLE = 85.25  # Maximum angle of elevation in degrees
MIN_ANGLE = 44.25  # Minimum angle of elevation in degrees

# Function to calculate the bearing angle
def calculate_bearing(mortar_coords, target_coords):
    dx = target_coords[0] - mortar_coords[0]
    dz = target_coords[2] - mortar_coords[2]
    bearing = math.atan2(dz, dx) * (180 / math.pi)
    bearing -= 90
    if bearing < 0:
        bearing += 360
    return bearing

# Function to calculate the horizontal range
def calculate_horizontal_range(mortar_coords, target_coords):
    dx = target_coords[0] - mortar_coords[0]
    dz = target_coords[2] - mortar_coords[2]
    return math.sqrt(dx**2 + dz**2)

# Function to calculate elevation angles and time of flight
def calculate_elevations_and_time_of_flight(mortar_coords, target_coords):
    horizontal_range = calculate_horizontal_range(mortar_coords, target_coords)
    dy = target_coords[1] - mortar_coords[1]
    results = []

    for i, velocity in enumerate(CHARGE_VELOCITIES):
        try:
            term = (velocity**4) - GRAVITY * (GRAVITY * horizontal_range**2 + 2 * dy * velocity**2)
            if term < 0:
                results.append((None, None, i))
                continue
            sqrt_term = math.sqrt(term)
            angle_radians_1 = math.atan((velocity**2 + sqrt_term) / (GRAVITY * horizontal_range))
            angle_radians_2 = math.atan((velocity**2 - sqrt_term) / (GRAVITY * horizontal_range))
            angle_degrees_1 = math.degrees(angle_radians_1)
            angle_degrees_2 = math.degrees(angle_radians_2)

            valid_angle_1 = MIN_ANGLE <= angle_degrees_1 <= MAX_ANGLE
            valid_angle_2 = MIN_ANGLE <= angle_degrees_2 <= MAX_ANGLE

            time_of_flight_1 = (velocity * math.sin(angle_radians_1) + math.sqrt((velocity * math.sin(angle_radians_1))**2 + 2 * GRAVITY * dy)) / GRAVITY if valid_angle_1 else None
            time_of_flight_2 = (velocity * math.sin(angle_radians_2) + math.sqrt((velocity * math.sin(angle_radians_2))**2 + 2 * GRAVITY * dy)) / GRAVITY if valid_angle_2 else None

            if valid_angle_1:
                results.append((angle_degrees_1, time_of_flight_1, i))
            elif valid_angle_2:
                results.append((angle_degrees_2, time_of_flight_2, i))
            else:
                results.append((None, None, i))
        except ValueError:
            results.append((None, None, i))
    return results

# Function to calculate mortar settings
def mortar_calculator(mortar_coords, target_coords):
    bearing = calculate_bearing(mortar_coords, target_coords)
    charge_results = calculate_elevations_and_time_of_flight(mortar_coords, target_coords)
    return bearing, charge_results

# Function to handle the calculate button click
def calculate():
    try:
        x0 = float(entry_x0.get())
        y0 = float(entry_y0.get())
        z0 = float(entry_z0.get())
        xt = float(entry_xt.get())
        yt = float(entry_yt.get())
        zt = float(entry_zt.get())
        mortar_coords = (x0, y0, z0)
        target_coords = (xt, yt, zt)

        bearing, charge_results = mortar_calculator(mortar_coords, target_coords)
        distance = calculate_horizontal_range(mortar_coords, target_coords)

        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Bearing: ")
        result_text.insert(tk.END, f"{bearing:.2f} degrees\n", "bearing")
        result_text.insert(tk.END, "Distance: ")
        result_text.insert(tk.END, f"{distance:.2f} studs\n", "distance")
        result_text.insert(tk.END, "\n")

        for angle, time_of_flight, charge_mode in charge_results:
            if angle is not None:
                result_text.insert(tk.END, f"Elevation Angle for C{charge_mode}: ")
                result_text.insert(tk.END, f"{angle:.2f} degrees\n", "elevation")
                result_text.insert(tk.END, f"Time of Flight for C{charge_mode}: {time_of_flight:.2f} seconds\n")
            else:
                result_text.insert(tk.END, f"No feasible solution for C{charge_mode} within angle limits.\n")
    except ValueError:
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Please enter valid numeric values for coordinates.")

# Create the main window
root = tk.Tk()
root.title("Mortar Calculator")
root.geometry("600x600")
root.configure(bg="#1c1c1c")  # Dark background

# Load a modern font
modern_font = font.Font(family="Arial", size=12)

# Create input fields
input_frame = tk.Frame(root, bg="#2a2a2a", bd=2, relief=tk.FLAT)
input_frame.pack(pady=20, padx=20, fill=tk.X)

tk.Label(input_frame, text="Launch Point (x0, y0, z0)", bg="#2a2a2a", fg="#ffffff", font=modern_font).grid(row=0, column=0, padx=10)
entry_x0 = tk.Entry(input_frame, width=10, font=modern_font, bd=2, bg="#3a3a3a", fg="#ffffff")
entry_y0 = tk.Entry(input_frame, width=10, font=modern_font, bd=2, bg="#3a3a3a", fg="#ffffff")
entry_z0 = tk.Entry(input_frame, width=10, font=modern_font, bd=2, bg="#3a3a3a", fg="#ffffff")
entry_x0.grid(row=0, column=1, padx=5)
entry_y0.grid(row=0, column=2, padx=5)
entry_z0.grid(row=0, column=3, padx=5)

tk.Label(input_frame, text="Target Point (xt, yt, zt)", bg="#2a2a2a", fg="#ffffff", font=modern_font).grid(row=1, column=0, padx=10, pady=10)
entry_xt = tk.Entry(input_frame, width=10, font=modern_font, bd=2, bg="#3a3a3a", fg="#ffffff")
entry_yt = tk.Entry(input_frame, width=10, font=modern_font, bd=2, bg="#3a3a3a", fg="#ffffff")
entry_zt = tk.Entry(input_frame, width=10, font=modern_font, bd=2, bg="#3a3a3a", fg="#ffffff")
entry_xt.grid(row=1, column=1, padx=5)
entry_yt.grid(row=1, column=2, padx=5)
entry_zt.grid(row=1, column=3, padx=5)

# Create calculate button
calculate_button = tk.Button(root, text="Calculate", command=calculate, bg="#d9534f", fg="white", padx=20, pady=10, font=modern_font)
calculate_button.pack(pady=20)

# Create result text area
result_frame = tk.Frame(root, bg="#1c1c1c")
result_frame.pack(pady=20)
result_text = tk.Text(result_frame, width=70, height=20, font=modern_font, bd=2, relief=tk.FLAT, bg="#2a2a2a", fg="#ffffff")
result_text.pack(side=tk.LEFT)

# Set highlight colors
result_text.tag_configure("bearing", foreground="#00FFFF")  # Cyan
result_text.tag_configure("distance", foreground="#FFA500")  # Orange
result_text.tag_configure("elevation", foreground="#90EE90")  # Light Green

scrollbar = tk.Scrollbar(result_frame, command=result_text.yview, bg="#3a3a3a")
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
result_text.config(yscrollcommand=scrollbar.set)

# Run the application
root.mainloop()
