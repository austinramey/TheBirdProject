import sys 
import os 

def process_bird_observations(bird_name): 
    # Indent: 1 
    """ 
    Reads bird observation data and finds maximum observations per year-month (2000-2025+). 
    Outputs results grouped by month, sorted by year descending. 
    """ 
    # Construct filenames based on bird name 
    # base_path = r"C:\Users\austin.ramey\Documents\Python\Personal Python\inputsAndOutputs" 
    base_path = r"/home/austin/devroot/PersonalProjects/TheBirdProject"
    input_path = r"/home/austin/devroot/PersonalProjects/TheBirdProject/inputs"
    input_file = os.path.join(input_path, f"{bird_name}Input.txt")
    output_path = r"/home/austin/devroot/PersonalProjects/TheBirdProject/outputs"
    output_file = os.path.join(output_path, f"{bird_name}Output.txt")

    # Indent: 1 
    # Check if input file exists, create if not 
    if not os.path.exists(input_file): 
        # Indent: 2 
        with open(input_file, 'w') as f: 
            # Indent: 3 
            pass 
        # Indent: 2 
        print(f"Created {bird_name}Input.txt.") 
        print("Format: YYYY-MM-DD [tab] observations [tab] observer_name") 
        print("Use camelCase naming with no spaces or punctuation.") 
        print("Run program again when data is added.") 
        return 

    # Indent: 1 
    # Data structure for month-year tracking 
    # monthly_data[month][year] = max_observations 
    monthly_data = { 
    # Indent: 2 
        month: {} for month in range(1, 13) 
    } 

    # Indent: 1 
    # Track min and max years found in data 
    min_year = 2025 
    max_year = 2000 

    try: 
        # Indent: 2 
        with open(input_file, 'r') as f: 
            # Indent: 3 
            for line in f: 
                # Indent: 4 
                line = line.strip() 
                if not line: 
                    # Indent: 5 
                    continue 

                # Indent: 4 
                parts = line.split('\t') 
                if len(parts) < 3: 
                    # Indent: 5 
                    continue 

                # Indent: 4 
                date_str = parts[0].strip() 
                obs_str = parts[1].strip() 

                # Extract year and month from date 
                try: 
                    # Indent: 5 
                    year_month_day = date_str.split('-') 
                    year = int(year_month_day[0]) 
                    month = int(year_month_day[1]) 
                # Indent: 4 
                except (ValueError, IndexError): 
                    # Indent: 5 
                    continue 

                # Indent: 4 
                # Update year range tracking 
                if year < min_year: 
                    # Indent: 5 
                    min_year = year 
                # Indent: 4 
                if year > max_year: 
                    # Indent: 5 
                    max_year = year 

                # Indent: 4 
                # Skip if month is invalid 
                if month < 1 or month > 12: 
                    # Indent: 5 
                    continue 

                # Indent: 4 
                # Convert observations to int (X = 0) 
                try: 
                    # Indent: 5 
                    observations = int(obs_str) 
                # Indent: 4 
                except ValueError: 
                    # Indent: 5 
                    observations = 0 

                # Indent: 4 
                # Update max for this month-year combination 
                if year not in monthly_data[month]: 
                    # Indent: 5 
                    monthly_data[month][year] = observations 
                # Indent: 4 
                elif observations > monthly_data[month][year]: 
                    # Indent: 5 
                    monthly_data[month][year] = observations 

        # Indent: 2 
        # Ensure we at least have 2000-2025 range 
        if min_year > 2000: 
            # Indent: 3 
            min_year = 2000 
        # Indent: 2 
        if max_year < 2025: 
            # Indent: 3 
            max_year = 2025 

        # Indent: 2 
        # Month names mapping 
        month_names = { 
            # Indent: 3 
            1: "January", 2: "February", 3: "March", 4: "April", 
            5: "May", 6: "June", 7: "July", 8: "August", 
            9: "September", 10: "October", 11: "November", 12: "December" 
        } 

        # Indent: 2 
        # Check if output file exists and prompt for overwrite 
        write_to_file = True 
        if os.path.exists(output_file): 
            # Indent: 3 
            response = input(f"Warning: {bird_name}Output.txt already exists. Overwrite? (y/N): ").strip().lower() 
            if response not in ['y', 'yes', '']: 
                # Indent: 4 
                print("Skipping file write. Displaying results to console.") 
                write_to_file = False 

        # Indent: 2 
        # Build results with month grouping 
        results = [] 

        # Indent: 2 
        for month in range(1, 13): 
            # Indent: 3 
            # Month header 
            results.append(f"{month_names[month]} - {bird_name}:") 

            # Iterate years from max to min 
            for year in range(max_year, min_year - 1, -1): 
                # Indent: 4 
                # Get observations for this month-year (default 0) 
                obs = monthly_data[month].get(year, 0) 
                results.append(f"{year}-{obs}") 

            # Indent: 3 
            # Add separator (blank line + 10 equals + blank line) 
            results.append("") 
            results.append("=" * 10) 
            results.append("") 

        # Indent: 2 
        # Write to file if approved, always display to console 
        if write_to_file: 
            # Indent: 3 
            with open(output_file, 'w') as f: 
                # Indent: 4 
                for result in results: 
                    # Indent: 5 
                    f.write(result + '\n') 
            # Indent: 3 
            print(f"Successfully processed data and wrote results to {bird_name}Output.txt") 

        # Indent: 2 
        # Always display results to console 
        print("\nResults:") 
        for result in results: 
            # Indent: 3 
            print(result) 
    # Indent: 1 
    except FileNotFoundError: 
        # Indent: 2 
        print(f"Error: Could not find {input_file}") 
    # Indent: 1 
    except Exception as e: 
        # Indent: 2 
        print(f"Error processing file: {e}") 

# Indent: 0 
if __name__ == "__main__": 
    # Indent: 1 
    if len(sys.argv) < 2: 
        # Indent: 2 
        print("Error: Please provide a bird name.") 
        print("Usage: python BirdNumericSearch.py <birdName>") 
        print("Example: python BirdNumericSearch.py americanCoot") 
        sys.exit(1) 

    # Indent: 1 
    bird_name = sys.argv[1] 
    process_bird_observations(bird_name)