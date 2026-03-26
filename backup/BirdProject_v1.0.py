import sys 
import os 

def process_bird_observations(bird_name): 
    """ 
    Reads bird observation data and finds maximum observations per year (2000-2025). 
    Outputs results sorted by year descending. 

    Takes bird_name parameter from command line 
    """ 
    # Construct filenames based on bird name 
    base_path = r"/home/austin/devroot/PersonalProjects/TheBirdProject/birdTest" 
    input_file = os.path.join(base_path, f"{bird_name}Input.txt") 
    output_file = os.path.join(base_path, f"{bird_name}Output.txt") 

    # Check if input file exists, create if not 
    if not os.path.exists(input_file): 
        with open(input_file, 'w') as f: 
            pass # Create empty file 
        print(f"Created {bird_name}Input.txt.") 
        print("Format: YYYY-MM-DD [tab] observations [tab] observer_name") 
        print("Use camelCase naming with no spaces or punctuation.") 
        print("Run program again when data is added.") 
        return 

    # Initialize dictionary for years 2000-2025 with 0 observations 
    year_max = {year: 0 for year in range(2000, 2026)} 

    try: 
        with open(input_file, 'r') as f: 
            for line in f: 
                line = line.strip() 
                if not line: 
                    continue 

                # Split line by tabs 
                parts = line.split('\t') 
                if len(parts) < 3: 
                    continue 

                date_str = parts[0].strip() 
                obs_str = parts[1].strip() 

                # Extract year from date (YYYY-MM-DD format) 
                try: 
                    year = int(date_str.split('-')[0]) 
                except (ValueError, IndexError): 
                    continue 

                # Skip if year outside our range 
                if year not in year_max: 
                    continue 

                # Convert observations to int (X = 0) 
                try: 
                    observations = int(obs_str) 
                except ValueError: 
                    observations = 0 

                # Update max for this year 
                if observations > year_max[year]: 
                    year_max[year] = observations 

        # Check if output file exists and prompt for overwrite 
        # TODO: Check indent here
        write_to_file = True 
        if os.path.exists(output_file): 
            response = input(f"Warning: {bird_name}Output.txt already exists. Overwrite? (y/N): ").strip().lower() 
            if response not in ['y', 'yes', '']: 
                print("Skipping file write. Displaying results to console.") 
                write_to_file = False 

        # Sort by year descending 
        results = [] 
        for year in sorted(year_max.keys(), reverse=True): 
            results.append(f"{year} - {year_max[year]}") 

        # Write to file if approved, always display to console 
        if write_to_file: 
            with open(output_file, 'w') as f: 
                for result in results: 
                    f.write(result + '\n') 
                print(f"Successfully processed data and wrote results to {bird_name}Output.txt") 

        # Always display results to console 
        print("\nResults:") 
        for result in results: 
            print(result) 

    except FileNotFoundError: 
        print(f"Error: Could not find {input_file}") 
    except Exception as e: 
        print(f"Error processing file: {e}") 

# Main execution with command line argument handling 
if __name__ == "__main__": 
    if len(sys.argv) < 2: 
        print("Error: Please provide a bird name.") 
        print("Usage: python BirdNumericSearch.py <birdName>") 
        print("Example: python BirdNumericSearch.py americanCoot") 
        sys.exit(1) 

    bird_name = sys.argv[1] 
    process_bird_observations(bird_name) 
