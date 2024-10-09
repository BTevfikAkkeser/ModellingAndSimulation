import matplotlib.pyplot as plt
import numpy as np

# Assuming x_t is a sequence of values from 1 to 200 (since log(0) is undefined)
x_t = np.arange(1, 201)

# Calculate the logarithm of each x_t value
log_x_t = np.log(x_t)

# Plotting the values
plt.figure(figsize=(10, 6))
plt.plot(x_t, log_x_t, label='log(x_t)', color='blue')

# Adding titles and labels
plt.title('Plot of log(x_t) for x_t values from 1 to 200')
plt.xlabel('x_t')
plt.ylabel('log(x_t)')
plt.legend()
plt.grid(True)

# Display the plot
plt.show()