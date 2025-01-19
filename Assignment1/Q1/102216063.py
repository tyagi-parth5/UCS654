import pandas as pd
import numpy as np
import os
import sys

def validate_and_load_data(input_file):
    try:
        file_ext = os.path.splitext(input_file)[1]
        if file_ext == '.csv':
            data = pd.read_csv(input_file)
        elif file_ext == '.xlsx':
            data = pd.read_excel(input_file)
        else:
            raise ValueError("Unsupported file format. Please provide a .csv or .xlsx file.")
        
        if data.shape[1] < 3:
            raise ValueError("Input file must have at least three columns.")
        
        for col in data.columns[1:]:
            pd.to_numeric(data[col], errors='raise')

        return data
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

def topsis(input_file, weights, impacts, output_file):
    try:
        data = validate_and_load_data(input_file)
        weights = list(map(float, weights.split(',')))
        impacts = impacts.split(',')
        
        if len(weights) != len(impacts) or len(weights) != (data.shape[1] - 1):
            raise Exception("Number of weights and impacts must match the number of criteria columns.")
        if not all(impact in ['+', '-'] for impact in impacts):
            raise Exception("Impacts must be '+' or '-'.")
        
        matrix = data.iloc[:, 1:].values
        norm_matrix = matrix / np.sqrt((matrix ** 2).sum(axis=0))
        weighted_matrix = norm_matrix * weights

        ideal_best = []
        ideal_worst = []
        for i in range(len(impacts)):
            if impacts[i] == '+':
                ideal_best.append(max(weighted_matrix[:, i]))
                ideal_worst.append(min(weighted_matrix[:, i]))
            else:
                ideal_best.append(min(weighted_matrix[:, i]))
                ideal_worst.append(max(weighted_matrix[:, i]))

        dist_ideal = np.sqrt(((weighted_matrix - ideal_best) ** 2).sum(axis=1))
        dist_worst = np.sqrt(((weighted_matrix - ideal_worst) ** 2).sum(axis=1))

        scores = dist_worst / (dist_ideal + dist_worst)
        data['Topsis Score'] = scores
        data['Rank'] = pd.Series(scores).rank(ascending=False).astype(int)

        data.to_csv(output_file, index=False)
        print(f"Result saved to {output_file}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python <program.py> <InputDataFile> <Weights> <Impacts> <ResultFileName>")
    else:
        _, input_file, weights, impacts, output_file = sys.argv
        topsis(input_file, weights, impacts, output_file)
