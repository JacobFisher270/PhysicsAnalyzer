import numpy as np
import pandas as pd
from scipy import stats

import matplotlib.pyplot as plt

def load_data(file_path):
    """Load physics data from file"""
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def analyze_data(data):
    """Perform basic statistical analysis"""
    results = {
        'mean': np.mean(data),
        'std': np.std(data),
        'median': np.median(data)
    }
    return results

def visualize_data(data, property_name):
    """Create basic visualization of the data"""
    plt.figure(figsize=(10, 6))
    plt.hist(data, bins=30)
    plt.title(f'Distribution of {property_name}')
    plt.xlabel(property_name)
    plt.ylabel('Frequency')
    plt.show()

def main():
    # Example usage
    file_path = "physics_data.csv"  # Replace with your data file
    data = load_data(file_path)
    
    if data is not None:
        # Example: analyzing a specific property
        property_name = "temperature"  # Replace with your property
        if property_name in data.columns:
            results = analyze_data(data[property_name])
            print(f"Analysis results for {property_name}:")
            print(results)
            
            visualize_data(data[property_name], property_name)

if __name__ == "__main__":
    main()