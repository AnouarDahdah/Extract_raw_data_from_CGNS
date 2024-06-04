import pandas as pd
import matplotlib.pyplot as plt

# Load CSV file into a DataFrame
df = pd.read_csv('/home/adahdah/monitor_data.csv', delimiter=',', header=0)

# Assuming your CSV file has columns named 'meanVxMonitor', 'meanVyMonitor', and 'meanVzMonitor'
x = df['meanVxMonitor']
y = df['meanVyMonitor']
z = df['meanVzMonitor']

# Plotting
plt.plot(x, label='meanVxMonitor')
plt.plot(y, label='meanVyMonitor')
plt.plot(z, label='meanVzMonitor')
plt.xlabel('X-axis label')
plt.ylabel('Y-axis label')
plt.title('Your Title Here')
plt.legend()
plt.grid(True)
plt.show()
