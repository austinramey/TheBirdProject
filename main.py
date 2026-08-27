import sys
import os
from datetime import datetime, timedelta

def parse_weekly_argument(arg):
    """Parse the weekly mode argument from command line."""
    if arg is None:
        return False

    arg = str(arg).lower().strip()
    return arg in ["true", "1", "yes", "y"]


def get_iso_week_date_range(year, week):
    """
    Calculate the start and end dates for an ISO week.
    Returns (start_date, end_date) as datetime objects.
    """
    try:
        jan_1 = datetime(year, 1, 1)
        days_to_monday = (7 - jan_1.weekday()) % 7
        if days_to_monday > 3:
            days_to_monday -= 7

        first_monday = jan_1 + timedelta(days=days_to_monday)
        target_date = first_monday + timedelta(weeks=week - 1)
        start_date = target_date
        end_date = target_date + timedelta(days=6)
        return start_date, end_date

    except:
        return None, None


def get_weeks_in_year(year):
    """Get the number of ISO weeks in a year (52 or 53)."""
    dec_28 = datetime(year, 12, 28)
    return dec_28.isocalendar()[1]


def find_file_in_subdirectories(base_path, target_filename):
    """
    Search base_path and all of its subdirectories for target_filename.
    Returns the full path to the file if found, otherwise None.

    If more than one match is found (e.g. duplicate files in different
    subfolders), the first one found is used and a warning is printed
    so the user is aware duplicates exist.
    """
    matches = []

    for root, dirs, files in os.walk(base_path):
        if target_filename in files:
            matches.append(os.path.join(root, target_filename))

    if not matches:
        return None

    if len(matches) > 1:
        print(f"Warning: Found multiple copies of {target_filename}:")
        for match in matches:
            print(f"  {match}")
        print(f"Using: {matches[0]}")

    return matches[0]


def find_input_file(input_path, bird_name):
    """Search input_path (and subfolders) for the bird's input file."""
    return find_file_in_subdirectories(input_path, f"{bird_name}Input.txt")


def find_output_file(output_path, bird_name):
    """Search output_path (and subfolders) for the bird's existing output file."""
    return find_file_in_subdirectories(output_path, f"{bird_name}Output.txt")


def process_bird_observations(bird_name, useWeekly, auto_overwrite=False, input_file_override=None, output_dir_override=None):
    """
    Reads bird observation data and finds maximum observations per year-month or year-week.
    Outputs results grouped by month or week, sorted by year descending.

    Returns a dict: {"status": "ok"|"empty"|"error", "message": "..."}
    """
    # base_path = r"C:\Users\16822\Desktop\TheBirdProject\TheBirdProject"
    base_path = r"/home/austin/devroot/PersonalProjects/TheBirdProject"
    input_path = f"{base_path}/inputs"
    output_path = f"{base_path}/outputs"

    if input_file_override:
        input_file = input_file_override
    else:
        input_file = find_input_file(input_path, bird_name)
        if input_file is None:
            input_file = os.path.join(input_path, f"{bird_name}Input.txt")

            with open(input_file, "w") as f:
                pass

            print(f"Created {bird_name}Input.txt.")
            print("Format: YYYY-MM-DD [tab] observations [tab] observer_name")
            print("Use camelCase naming with no spaces or punctuation.")
            print("Run program again when data is added.")
            return {"status": "empty", "message": "Created new empty input file"}

    if output_dir_override:
        output_file = os.path.join(output_dir_override, f"{bird_name}Output.txt")
    else:
        output_file = find_output_file(output_path, bird_name)
        if output_file is None:
            output_file = os.path.join(output_path, f"{bird_name}Output.txt")

    # Determine mode
    use_weekly = parse_weekly_argument(useWeekly)

    # Initialize data structures
    if use_weekly:
        weekly_data = {}

    else:
        monthly_data = {month: {} for month in range(1, 13)}

    min_year = 2025
    max_year = 2000

    try:
        has_data = False
        warnings = []
        with open(input_file, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                parts = line.split("\t")
                if len(parts) < 3:
                    continue

                date_str = parts[0].strip()
                obs_str = parts[1].strip()

                # Extract year, month, and day
                try:
                    year_month_day = date_str.split("-")
                    year = int(year_month_day[0])
                    month = int(year_month_day[1])
                    day = int(year_month_day[2])

                except (ValueError, IndexError):
                    warnings.append(f"Invalid date format: {date_str}")
                    continue

                # Update year range tracking
                if year < min_year:
                    min_year = year

                if year > max_year:
                    max_year = year

                has_data = True

                # Convert observations to int (X = 0)
                try:
                    observations = int(obs_str)

                except ValueError:
                    observations = 0

                if use_weekly:
                    # Calculate ISO week number
                    try:
                        date_obj = datetime(year, month, day)
                        week_num = date_obj.isocalendar()[1]

                        if year not in weekly_data:
                            weekly_data[year] = {}

                        if week_num not in weekly_data[year]:
                            weekly_data[year][week_num] = observations

                        elif observations > weekly_data[year][week_num]:
                            weekly_data[year][week_num] = observations

                    except ValueError:
                        warnings.append(f"Invalid date: {date_str}")
                        continue

                else:
                    # Monthly mode
                    if month < 1 or month > 12:
                        warnings.append(f"Invalid month in date: {date_str}")
                        continue

                    if year not in monthly_data[month]:
                        monthly_data[month][year] = [observations, date_str]

                    elif observations >= monthly_data[month][year][0]:
                        monthly_data[month][year] = [observations, date_str]
                        # monthly_data[month][year] = [observations, ]

        if not has_data:
            msg = "No valid observation data found"
            if warnings:
                msg += " (" + "; ".join(warnings) + ")"
            return {"status": "empty", "message": msg}

        # Ensure we at least have 2000-2025 range
        if min_year > 2000:
            min_year = 2000

        if max_year < 2025:
            max_year = 2025

        # Month names mapping
        month_names = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December",
        }

        # Check if output file exists and prompt for overwrite
        write_to_file = True
        if os.path.exists(output_file) and not auto_overwrite:
            response = (input(f"Warning: {bird_name}Output.txt already exists. Overwrite? (y/N): ").strip().lower())
            if response not in ["y", "yes", ""]:
                print("Skipping file write. Displaying results to console.")
                write_to_file = False

        # Build results
        results = []

        if use_weekly:

            # Group by year first, then show all weeks for that year
            for year in range(max_year, min_year - 1, -1):

                # Year header
                results.append(f"{year} - {bird_name}:")

                # Get number of weeks for this specific year
                weeks_in_year = get_weeks_in_year(year)

                # Show all weeks for this year
                for week in range(1, weeks_in_year + 1):
                    # Calculate date range for this week in this specific year
                    start_date, end_date = get_iso_week_date_range(year, week)

                    if start_date and end_date:
                        start_str = start_date.strftime("%m/%d/%Y")
                        end_str = end_date.strftime("%m/%d/%Y")
                        # Get observation count for this year-week
                        obs = weekly_data.get(year, {}).get(week, 0)
                        results.append(
                            f"Week {week} - {start_str} -> {end_str} - {obs}"
                        )

                    else:
                        # Fallback if date calculation fails
                        obs = weekly_data.get(year, {}).get(week, 0)
                        results.append(f"Week {week} - {obs}")

                # Add separator between years
                results.append("")
                results.append("=" * 10)
                results.append("")

        else:
            # Monthly mode
            for month in range(1, 13):
                results.append(f"{month_names[month]} - {bird_name}:")

                for year in range(max_year, min_year - 1, -1):
                    obs = monthly_data[month].get(year, 0)
                    if type(obs) is list and obs[0] > 0: # Remove this to bring back empty years from each month format
                        results.append(f"{year}-{obs[0]} -- {obs[1]}")

                results.append("")
                results.append("=" * 10)
                results.append("")

        # Write to file if approved, always display to console
        if write_to_file:
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, "w") as f:
                for result in results:
                    f.write(result + "\n")

            mode_str = "weekly" if use_weekly else "monthly"
            print(
                f"Successfully processed data and wrote results to {bird_name}Output.txt ({mode_str} mode)"
            )

        return {"status": "ok", "message": "; ".join(warnings) if warnings else ""}

    except FileNotFoundError:
        print(f"Error: Could not find {input_file}")
        return {"status": "error", "message": f"File not found: {input_file}"}

    except Exception as e:
        print(f"Error processing file: {e}")
        return {"status": "error", "message": str(e)}


def reprocess_all(useWeekly):
    """
    Walks all *Input.txt files under inputs/, processes each one,
    writes output to the matching outputs/ subfolder, and logs any problems.
    """
    base_path = r"/home/austin/devroot/PersonalProjects/TheBirdProject"
    input_path = os.path.join(base_path, "inputs")
    output_path = os.path.join(base_path, "outputs")
    log_path = os.path.join(base_path, "reprocess_log.txt")

    use_weekly = parse_weekly_argument(useWeekly)

    ok_count = 0
    empty_count = 0
    error_count = 0
    problems = []

    input_files = []
    for root, dirs, files in os.walk(input_path):
        for fname in files:
            if fname.endswith("Input.txt"):
                input_files.append(os.path.join(root, fname))

    total = len(input_files)
    print(f"Found {total} input files. Processing...")

    for input_file in sorted(input_files):
        # Derive bird name: strip the Input.txt suffix
        bird_name = os.path.basename(input_file).replace("Input.txt", "")

        # Compute matching output subfolder
        rel_dir = os.path.relpath(os.path.dirname(input_file), input_path)
        if rel_dir == ".":
            out_dir = output_path
        else:
            out_dir = os.path.join(output_path, rel_dir)

        os.makedirs(out_dir, exist_ok=True)

        result = process_bird_observations(
            bird_name,
            useWeekly,
            auto_overwrite=True,
            input_file_override=input_file,
            output_dir_override=out_dir,
        )

        if result["status"] == "ok":
            ok_count += 1
            if result["message"]:
                problems.append((input_file, f"Warnings: {result['message']}"))
        elif result["status"] == "empty":
            empty_count += 1
            problems.append((input_file, f"Empty: {result['message']}"))
        else:
            error_count += 1
            problems.append((input_file, f"Error: {result['message']}"))

    # Write log file
    with open(log_path, "w") as f:
        f.write(f"Reprocess Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 40 + "\n\n")
        if problems:
            for filepath, issue in problems:
                f.write(f"{filepath}\n")
                f.write(f"  {issue}\n\n")
        else:
            f.write("No problems found.\n")

    # Print summary
    print("\n" + "=" * 40)
    print(f"Reprocess complete: {total} files")
    print(f"  OK:    {ok_count}")
    print(f"  Empty: {empty_count}")
    print(f"  Error: {error_count}")
    print(f"Log written to {log_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: Please provide a bird name or command.")
        print("Usage: python main.py <birdName> [weekly]")
        print("       python main.py reprocess [weekly]")
        print("Examples:")
        print(" python main.py americanCoot")
        print(" python main.py americanCoot true")
        print(" python main.py reprocess")
        print(" python main.py reprocess true")
        sys.exit(1)

    command = sys.argv[1]
    useWeekly = sys.argv[2] if len(sys.argv) > 2 else None

    if command.lower() == "reprocess":
        reprocess_all(useWeekly)
    else:
        process_bird_observations(command, useWeekly)
