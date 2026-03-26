import sys 
import os 
from datetime import datetime, timedelta 

# Indent: 0 
def parse_weekly_argument(arg): 
    # Indent: 1 
    """Parse the weekly mode argument from command line.""" 
    if arg is None: 
        # Indent: 2 
        return False 
    # Indent: 1 
    arg = str(arg).lower().strip() 
    return arg in ['true', '1', 'yes', 'y'] 

# Indent: 0 
def get_iso_week_date_range(year, week): 
    # Indent: 1 
    """ 
    Calculate the start and end dates for an ISO week. 
    Returns (start_date, end_date) as datetime objects. 
    """ 
    try: 
        # Indent: 2 
        jan_1 = datetime(year, 1, 1) 
        days_to_monday = (7 - jan_1.weekday()) % 7 
        if days_to_monday > 3: 
            # Indent: 3 
            days_to_monday -= 7 
        # Indent: 2 
        first_monday = jan_1 + timedelta(days=days_to_monday) 
        target_date = first_monday + timedelta(weeks=week-1) 
        start_date = target_date 
        end_date = target_date + timedelta(days=6) 
        return start_date, end_date 
    # Indent: 1 
    except: 
        # Indent: 2 
        return None, None 

# Indent: 0 
def get_weeks_in_year(year): 
    # Indent: 1 
    """Get the number of ISO weeks in a year (52 or 53).""" 
    dec_28 = datetime(year, 12, 28) 
    return dec_28.isocalendar()[1] 

# Indent: 0 
def process_bird_observations(bird_name, useWeekly): 
    # Indent: 1 
    """ 
    Reads bird observation data and finds maximum observations per year-month or year-week. 
    Outputs results grouped by month or week, sorted by year descending. 
    """ 
    # base_path = r"C:\Users\austin.ramey\Documents\Python\Personal Python\inputsAndOutputs" 
    # input_file = os.path.join(base_path, f"{bird_name}Input.txt") 
    # output_file = os.path.join(base_path, f"{bird_name}Output.txt") 
    base_path = r"/home/austin/devroot/PersonalProjects/TheBirdProject"
    input_path = r"/home/austin/devroot/PersonalProjects/TheBirdProject/inputs"
    input_file = os.path.join(input_path, f"{bird_name}Input.txt")
    output_path = r"/home/austin/devroot/PersonalProjects/TheBirdProject/outputs"
    output_file = os.path.join(output_path, f"{bird_name}Output.txt")

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
    # Determine mode 
    use_weekly = parse_weekly_argument(useWeekly) 

    # Initialize data structures 
    if use_weekly: 
        # Indent: 2 
        weekly_data = {} 
    # Indent: 1 
    else: 
        # Indent: 2 
        monthly_data = {month: {} for month in range(1, 13)} 

    # Indent: 1 
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

                # Extract year, month, and day 
                try: 
                    # Indent: 5 
                    year_month_day = date_str.split('-') 
                    year = int(year_month_day[0]) 
                    month = int(year_month_day[1]) 
                    day = int(year_month_day[2]) 
                # Indent: 4 
                except (ValueError, IndexError): 
                    # Indent: 5 
                    print(f"Warning: Skipping invalid date format: {date_str}") 
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
                # Convert observations to int (X = 0) 
                try: 
                    # Indent: 5 
                    observations = int(obs_str) 
                # Indent: 4 
                except ValueError: 
                    # Indent: 5 
                    observations = 0 

                # Indent: 4 
                if use_weekly: 
                    # Indent: 5 
                    # Calculate ISO week number 
                    try: 
                        # Indent: 6 
                        date_obj = datetime(year, month, day) 
                        week_num = date_obj.isocalendar()[1] 

                        if year not in weekly_data: 
                            # Indent: 7 
                            weekly_data[year] = {} 
                        # Indent: 6 
                        if week_num not in weekly_data[year]: 
                            # Indent: 7 
                            weekly_data[year][week_num] = observations 
                        # Indent: 6 
                        elif observations > weekly_data[year][week_num]: 
                            # Indent: 7 
                            weekly_data[year][week_num] = observations 
                    # Indent: 5 
                    except ValueError: 
                        # Indent: 6 
                        print(f"Warning: Skipping invalid date: {date_str}") 
                        continue 
                # Indent: 4 
                else: 
                    # Indent: 5 
                    # Monthly mode 
                    if month < 1 or month > 12: 
                        # Indent: 6 
                        print(f"Warning: Skipping invalid month in date: {date_str}") 
                        continue 

                    # Indent: 5 
                    if year not in monthly_data[month]: 
                        # Indent: 6 
                        monthly_data[month][year] = observations 
                    # Indent: 5 
                    elif observations > monthly_data[month][year]: 
                        # Indent: 6 
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
        # Build results 
        results = [] 

        if use_weekly: 
            # Indent: 3 
            # Group by year first, then show all weeks for that year 
            for year in range(max_year, min_year - 1, -1): 
                # Indent: 4 
                # Year header 
                results.append(f"{year} - {bird_name}:") 

                # Get number of weeks for this specific year 
                weeks_in_year = get_weeks_in_year(year) 

                # Show all weeks for this year 
                for week in range(1, weeks_in_year + 1): 
                    # Indent: 5 
                    # Calculate date range for this week in this specific year 
                    start_date, end_date = get_iso_week_date_range(year, week) 

                    if start_date and end_date: 
                        # Indent: 6 
                        start_str = start_date.strftime("%m/%d/%Y") 
                        end_str = end_date.strftime("%m/%d/%Y") 
                        # Get observation count for this year-week 
                        obs = weekly_data.get(year, {}).get(week, 0) 
                        results.append(f"Week {week} - {start_str} -> {end_str} - {obs}") 
                    # Indent: 5 
                    else: 
                        # Indent: 6 
                        # Fallback if date calculation fails 
                        obs = weekly_data.get(year, {}).get(week, 0) 
                        results.append(f"Week {week} - {obs}") 

                # Indent: 4 
                # Add separator between years 
                results.append("") 
                results.append("=" * 10) 
                results.append("") 
        # Indent: 2 
        else: 
            # Indent: 3 
            # Monthly mode 
            for month in range(1, 13): 
                # Indent: 4 
                results.append(f"{month_names[month]} - {bird_name}:") 

                for year in range(max_year, min_year - 1, -1): 
                    # Indent: 5 
                    obs = monthly_data[month].get(year, 0) 
                    results.append(f"{year}-{obs}") 

                # Indent: 4 
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
            mode_str = "weekly" if use_weekly else "monthly" 
            print(f"Successfully processed data and wrote results to {bird_name}Output.txt ({mode_str} mode)") 

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
        print("Usage: python BirdNumericSearch.py <birdName> [weekly]") 
        print("Examples:") 
        print(" python BirdNumericSearch.py americanCoot") 
        print(" python BirdNumericSearch.py americanCoot true") 
        print(" python BirdNumericSearch.py americanCoot false") 
        sys.exit(1) 

    # Indent: 1 
    bird_name = sys.argv[1] 
    useWeekly = sys.argv[2] if len(sys.argv) > 2 else None 
    process_bird_observations(bird_name, useWeekly)
