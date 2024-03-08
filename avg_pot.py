import numpy as np 
import matplotlib.pyplot as plt
import sys

# Check if the correct number of command-line arguments are provided
if len(sys.argv) != 3:
    print("Usage: python3 script.py <input> <output>")
    sys.exit(1)

# Extract the input and output filenames from the command-line arguments
input_file = sys.argv[1]
output_file = sys.argv[2]


print("--- Reading the input file ---")

LOCPOT = open(input_file, "r")
LOCPOT_data = LOCPOT.readlines()

LOCPOT_data_column = []

# Iterate over each entry in LOCPOT_data
for entry in LOCPOT_data:
    # Split the entry into individual elements by whitespace
    split_entry = entry.split()
    # Iterate over each element in the split entry
    for element in split_entry:
        try:
            # Attempt to convert the element to a float
            float_value = float(element)
            # Append the float value to the list
            LOCPOT_data_column.append(float_value)
        except ValueError:
            # If conversion fails, handle the error (e.g., skip the element)
            pass

a=np.array([LOCPOT_data_column[1],LOCPOT_data_column[2],LOCPOT_data_column[3]])
b=np.array([LOCPOT_data_column[4],LOCPOT_data_column[5],LOCPOT_data_column[6]])
c=np.array([LOCPOT_data_column[7],LOCPOT_data_column[8],LOCPOT_data_column[9]])

Nx=int(LOCPOT_data_column[17])
Ny=int(LOCPOT_data_column[18])
Nz=int(LOCPOT_data_column[19])

vol = np.abs(np.dot(a,(np.cross(b,c))))
print("--- The volme of the unit cell is ", vol,' Å')
plane_values = []
z_coord = [(Z - 1) / Nz * c[2] for Z in range(1, Nz + 1)]


index = 19  # Initialize the index to start from LOCPOT_data_column[20]

for Z in range(Nz):
    plane_sum = 0
    for Y in range(Ny):
        for X in range(Nx):
            index += 1  # Increment the index for each element within the loop
            plane_sum += LOCPOT_data_column[index] 
    # Calculate the average value for the current plane and append it to the list
    average_value = plane_sum / (Nx * Ny * vol)
    plane_values.append(average_value)

print("--- Writing data as an output ---")

with open(output_file, 'w') as file:
    # Write the data from z_coord and plane_values to the file
    for z, value in zip(z_coord, plane_values):
        file.write(f"{z} {value}\n")

plot_data = input("Do you want to plot the data? (y/n): ")

# Check if the user wants to plot the data
if plot_data.lower() == "y":
    # Plot the average plane
    plt.plot(z_coord, plane_values)
    plt.xlabel('z-axis')
    plt.ylabel('Average potential eV')
    plt.title('Plane average potential in the z-direction')
    plt.show()
