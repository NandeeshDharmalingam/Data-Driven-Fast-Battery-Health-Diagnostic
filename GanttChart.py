import plotly.express as px
from datetime import datetime, timedelta

# Define your tasks and their details
tasks = [
    {"Task": "Literature Review", "Start": "2024-01-18", "Finish": "2024-01-25", "Status": "In Progress"},
    {"Task": "Finalize Open Source Data", "Start": "2024-01-26", "Finish": "2024-02-05", "Status": "To Be Done"},
    {"Task": "Data Manipulation", "Start": "2024-02-06", "Finish": "2024-03-05", "Status": "To Be Done"},
    {"Task": "Model Development Planning", "Start": "2024-03-06", "Finish": "2024-03-15", "Status": "To Be Done"},
    {"Task": "Develop Model", "Start": "2024-03-16", "Finish": "2024-04-15", "Status": "To Be Done"},
    {"Task": "Feature Extraction", "Start": "2024-04-16", "Finish": "2024-04-30", "Status": "To Be Done"},
    {"Task": "Training Completed", "Start": "2024-05-01", "Finish": "2024-05-01", "Status": "To Be Done"},
    {"Task": "Analysis and Refinement", "Start": "2024-05-02", "Finish": "2024-05-15", "Status": "To Be Done"},
    {"Task": "Update Thesis Report", "Start": "2024-05-16", "Finish": "2024-06-20", "Status": "To Be Done"},
    
    # Additional tasks during model development
    {"Task": "Optimize Hyperparameters", "Start": "2024-03-16", "Finish": "2024-03-30", "Status": "Mandatory"},
    {"Task": "Cross-Validation", "Start": "2024-03-31", "Finish": "2024-04-10", "Status": "mandatory"},
    
    # Additional tasks during feature extraction
    {"Task": "Developing scipt for  Relevant Features selection", "Start": "2024-04-17", "Finish": "2024-04-25", "Status": "mandatory"},
    {"Task": "Apply Dimensionality Reduction", "Start": "2024-04-26", "Finish": "2024-05-05", "Status": "mandatory"},
    {"Task": "Finalizing Activation Function", "Start": "2024-04-05", "Finish": "2024-04-15", "Status": "mandatory"},
]

# Convert date strings to datetime objects
for task in tasks:
    task["Start"] = datetime.strptime(task["Start"], "%Y-%m-%d")
    task["Finish"] = datetime.strptime(task["Finish"], "%Y-%m-%d")

# Create Gantt chart
fig = px.timeline(tasks, x_start="Start", x_end="Finish", y="Task", color="Status",
                   labels={"Task": "Task Name", "Start": "Start Date", "Finish": "Finish Date"},
                   color_discrete_map={"In Progress": "Blue", "To Be Done": "orange", "Done": "green","Mandatory":"red"})

# Customize Gantt chart layout
fig.update_layout(title="Thesis Gantt Chart",
                  xaxis_title="Timeline",
                  yaxis_title="Tasks",
                  showlegend=True,  # Hide legend
                  font=dict(family="Arial, sans-serif", size=14, color="RebeccaPurple"))  # Set font properties

# Show the plot
fig.show()
