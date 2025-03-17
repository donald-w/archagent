#%%

import pandas as pd
import numpy as np
import random

# Set pandas display options for better viewing
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Define realistic department names in financial services
departments = [
    "Investment Banking",
    "Risk Management",
    "Wealth Management",
    "Corporate Finance",
    "Trading & Securities",
    "Compliance & Legal",
    "Financial Planning",
    "Asset Management",
    "Treasury Operations",
    "Credit Analysis"
]

# Define department to JIRA prefix mapping
dept_to_prefix = {
    "Investment Banking": "IB",
    "Risk Management": "RISK",
    "Wealth Management": "WM",
    "Corporate Finance": "FIN",
    "Trading & Securities": "TRADE",
    "Compliance & Legal": "COMPL",
    "Financial Planning": "FP",
    "Asset Management": "AM",
    "Treasury Operations": "TREAS",
    "Credit Analysis": "CRED"
}

# Define project name components
project_prefixes = [
    "Digital", "Smart", "Automated", "Integrated", "Enhanced",
    "Real-time", "AI-Driven", "Cloud-Based", "Secure", "Advanced"
]

project_types = [
    "Portfolio Management", "Risk Assessment", "Trading Platform",
    "Compliance System", "Analytics Dashboard", "Reporting Framework",
    "Client Portal", "Payment Gateway", "Fraud Detection", "Data Pipeline"
]

# Define timeframes and status options
timeframes = ["past", "current", "future"]
status_options = ["backlog", "committed", "in_progress", "completed", "cancelled"]

# Define status probabilities based on timeframe
status_probabilities = {
    "past": {
        "completed": 0.7,    # Most past projects are completed
        "cancelled": 0.25,   # Some are cancelled
        "in_progress": 0.05, # Very few might still be in progress
        "committed": 0,      # None are committed
        "backlog": 0         # None are in backlog
    },
    "current": {
        "in_progress": 0.6,  # Most current projects are in progress
        "committed": 0.2,    # Some are committed
        "backlog": 0.1,      # Few are in backlog
        "completed": 0.1,    # Few are completed
        "cancelled": 0       # None are cancelled yet
    },
    "future": {
        "backlog": 0.7,      # Most future projects are in backlog
        "committed": 0.25,   # Some are committed
        "in_progress": 0.05, # Very few might be started early
        "completed": 0,      # None are completed
        "cancelled": 0       # None are cancelled
    }
}

#%%

def generate_project_name():
    """Generate a realistic project name for financial services"""
    prefix = random.choice(project_prefixes)
    type_ = random.choice(project_types)
    return f"{prefix} {type_}"

def generate_project_id(department, index):
    """Generate a JIRA-like project ID based on department"""
    prefix = dept_to_prefix[department]
    return f"{prefix}-{index + 1000}"  # Starting from 1000 for more realistic IDs

def generate_status(timeframe):
    """Generate a status based on timeframe with appropriate probabilities"""
    probs = status_probabilities[timeframe]
    return random.choices(
        list(probs.keys()),
        weights=list(probs.values()),
        k=1
    )[0]

# Generate random data
n_records = 20  # Change this to generate more or fewer records
departments_data = random.choices(departments, k=n_records)
timeframes_data = random.choices(timeframes, k=n_records)

data = {
    'project_id': [generate_project_id(dept, i) for i, dept in enumerate(departments_data)],
    'department': departments_data,
    'project_name': [generate_project_name() for _ in range(n_records)],
    'timeframe': timeframes_data,
    'status': [generate_status(tf) for tf in timeframes_data]
}

# Create DataFrame
df = pd.DataFrame(data)

def display_dataframe(df):
    """Display DataFrame in both Jupyter and non-Jupyter environments"""
    try:
        from IPython.display import display
        # We're in a Jupyter environment
        
        # Style the DataFrame
        styled_df = df.copy()
        styled_df = styled_df.sort_values('project_id')
        
        # Define color maps for categorical columns
        timeframe_colors = {
            'past': '#ffcdd2',    # Light red
            'current': '#c8e6c9',  # Light green
            'future': '#bbdefb'    # Light blue
        }
        
        status_colors = {
            'completed': '#81c784',  # Green
            'in_progress': '#64b5f6', # Blue
            'committed': '#fff176',   # Yellow
            'backlog': '#e0e0e0',     # Grey
            'cancelled': '#ef9a9a'     # Red
        }

        def color_timeframe(val):
            return f'background-color: {timeframe_colors.get(val, "white")}'
            
        def color_status(val):
            return f'background-color: {status_colors.get(val, "white")}'
        
        display(styled_df.style\
            .set_properties(**{'text-align': 'left'})\
            .set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#f0f0f0'), 
                                           ('color', 'black'),
                                           ('font-weight', 'bold'),
                                           ('text-align', 'left'),
                                           ('padding', '8px')]},
                {'selector': 'td', 'props': [('padding', '8px')]},
            ])\
            .applymap(color_timeframe, subset=['timeframe'])\
            .applymap(color_status, subset=['status']))
    except (ImportError, ValueError):
        # We're in a regular Python environment
        print(df.sort_values('project_id').to_string())

def display_analysis(df):
    """Display analysis in both Jupyter and non-Jupyter environments"""
    try:
        from IPython.display import display
        # We're in a Jupyter environment
        
        print("\nProjects per Department:")
        dept_counts = df['department'].value_counts()
        display(dept_counts.to_frame().style.bar(color='#5fba7d', width=70))

        print("\nProjects by Timeframe:")
        time_counts = df['timeframe'].value_counts()
        display(time_counts.to_frame().style.bar(color='#5fba7d', width=70))

        print("\nProjects by Status:")
        status_counts = df['status'].value_counts()
        display(status_counts.to_frame().style.bar(color='#5fba7d', width=70))

        print("\nStatus Distribution by Timeframe:")
        status_dist = pd.crosstab(df['timeframe'], df['status'], normalize='index').round(2)
        display(status_dist.style.background_gradient(cmap='YlOrRd'))

        print("\nProjects by Department and Timeframe:")
        dept_time = pd.crosstab(df['department'], df['timeframe'])
        display(dept_time.style.background_gradient(cmap='YlOrRd'))

        print("\nExample Project IDs by Department:")
        project_ids = df.groupby('department')['project_id'].first().sort_index()
        display(project_ids.to_frame())
        
    except (ImportError, ValueError):
        # We're in a regular Python environment
        print("\nProjects per Department:")
        print(df['department'].value_counts())

        print("\nProjects by Timeframe:")
        print(df['timeframe'].value_counts())

        print("\nProjects by Status:")
        print(df['status'].value_counts())

        print("\nStatus Distribution by Timeframe:")
        print(pd.crosstab(df['timeframe'], df['status'], normalize='index').round(2))

        print("\nProjects by Department and Timeframe:")
        print(pd.crosstab(df['department'], df['timeframe']))

        print("\nExample Project IDs by Department:")
        print(df.groupby('department')['project_id'].first().sort_index())

# Display the results
print("Sample Financial Services Projects:")
print("\nShape:", df.shape)
print("\nSample Data:")
display_dataframe(df)

# Display the analysis
display_analysis(df) 
# %%
