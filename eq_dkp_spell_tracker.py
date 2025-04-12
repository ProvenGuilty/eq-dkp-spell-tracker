import os
import re
import time
import argparse
from datetime import datetime

def detect_eq_logs():
    """
    Detects EQ log files from the current directory that have been modified in the last 7 days.
    Returns a sorted list of these log files, with the most recently modified first.
    """
    log_files = [f for f in os.listdir() if f.startswith("eqlog_") and f.endswith(".txt")]
    current_time = time.time()

    # Filter logs modified in the last 7 days
    recent_logs = [
        f for f in log_files if current_time - os.path.getmtime(f) <= 7 * 86400
    ]

    # Sort by modification time (most recent first)
    recent_logs.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return recent_logs

def extract_dates_from_log(file_name):
    """
    Extracts all distinct calendar dates from the log file.
    Returns a sorted list of distinct dates (most recent first).
    """
    dates = set()
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()

        for line in lines:
            # Match the timestamp format [Day Month Date Time Year]
            match = re.match(r"\[([A-Za-z]{3}) (\w{3}) (\d{2}) (\d{2}):(\d{2}):(\d{2}) (\d{4})\]", line)
            if match:
                log_date = datetime.strptime(f"{match.group(2)} {match.group(3)} {match.group(7)}", '%b %d %Y').date()
                dates.add(log_date)

        # Sort the dates in descending order (most recent first)
        return sorted(dates, reverse=True)
    except FileNotFoundError:
        print(f"Error: The file {file_name} was not found.")
        return []

def parse_log(file_name, selected_date, debug=False):
    """
    Parses the EQ log file, calculates active time, AFK time, and skill-ups for the selected date.
    """
    total_active_time = total_afk_time = 0
    first_cast_time = last_cast_time = None
    skillups = {}
    experience_count = 0  # Counter for experience messages
    total_log_entries = 0  # Total number of log entries scanned
    last_timestamp = None  # Store timestamp of the previous cast

    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()

        total_log_entries = len(lines)  # Count the total number of log entries

        for line in lines:
            # Match date and filter by selected date
            match = re.match(r"\[([A-Za-z]{3}) (\w{3}) (\d{2}) (\d{2}):(\d{2}):(\d{2}) (\d{4})\]", line)
            if match:
                log_date = datetime.strptime(f"{match.group(2)} {match.group(3)} {match.group(7)}", '%b %d %Y').date()
                if log_date != selected_date:
                    continue  # Skip log entries that are not from the selected date

            # Track experience messages
            if "You gain party experience" in line:
                experience_count += 1
                continue

            # Process spell casting events
            if "You begin casting" in line or "Your spell fizzles" in line or "Beginning to memorize" in line:
                timestamp_str = line.split(']')[0][1:]  # Extract timestamp
                timestamp = datetime.strptime(timestamp_str, '%a %b %d %H:%M:%S %Y')

                if debug:
                    print(f"Processing: {line.strip()}")
                    print(f"Matched event at {timestamp_str} for spell: {line.split(']')[1].strip()}")

                # First cast time
                if not first_cast_time:
                    first_cast_time = timestamp
                    if debug:
                        print(f"First cast time set at: {first_cast_time}")

                last_cast_time = timestamp

                # Calculate the time difference between consecutive casts (not from the first cast)
                if last_timestamp:
                    time_diff = (timestamp - last_timestamp).total_seconds()
                    if debug:
                        print(f"Time difference between consecutive casts: {time_diff} seconds")

                    # If the gap is less than or equal to 2 minutes (120 seconds), add to active time
                    if time_diff <= 120:
                        total_active_time += time_diff
                        if debug:
                            print(f"Added {time_diff} seconds to active time.")
                    else:
                        # If the gap is greater than 2 minutes, add to AFK time
                        total_afk_time += time_diff
                        if debug:
                            print(f"Added {time_diff} seconds to AFK time.")

                last_timestamp = timestamp  # Update the last timestamp

            # Track skill-ups using regex
            skillup_match = re.search(r"You have become better at (.+?)! \((\d+)\)", line)
            if skillup_match:
                skill = skillup_match.group(1)
                skill_level = int(skillup_match.group(2))

                # Track the starting and ending levels for each skill
                if skill not in skillups:
                    skillups[skill] = {'start': skill_level, 'end': skill_level}
                else:
                    skillups[skill]['end'] = skill_level

        return total_active_time, total_afk_time, first_cast_time, last_cast_time, skillups, experience_count, total_log_entries

    except FileNotFoundError:
        print(f"Error: The file {file_name} was not found.")
        return 0, 0, None, None, {}, 0, 0


def display_report(total_active_time, total_afk_time, total_processing_time, first_cast_time, last_cast_time, skillups, experience_count, total_log_entries, verbose, debug):
    """
    Displays the final report with active time, AFK time, processing time, and skill-up information.
    """
    print(f"\nTotal active time spent casting spells: {total_active_time/60:.2f} minutes")
    print(f"Total AFK time: {total_afk_time/60:.2f} minutes")
    print(f"Total processing time: {total_processing_time:.2f} seconds")  # Keep in seconds

    # Display skill-ups
    if skillups:
        print(f"\nSkill-ups detected:")
        sorted_skillups = sorted(skillups.items(), key=lambda x: x[0])
        for skill, levels in sorted_skillups:
            total_skillups = levels['end'] - levels['start']
            print(f"{skill}: {levels['start']} -> {levels['end']} (+{total_skillups})")

    # Display total experience messages count
    print(f"\nTotal experience messages detected: {experience_count}")

    # Display additional statistics if verbose flag is set
    if verbose:
        print(f"\nStatistics:")
        print(f"Total log entries scanned: {total_log_entries}")
        print(f"First cast entry: {first_cast_time}")
        print(f"Last cast entry: {last_cast_time}")

    # If debug flag is set, display more information
    if debug:
        print("\nDebug mode enabled: Detailed processing output displayed.")
        print("Detailed logs are written to excluded_lines_*.log")


def main():
    """
    Main function that allows the user to select a log file, parse it, and display the results.
    """
    parser = argparse.ArgumentParser(description="Process EQ logs for spell casting and skill-ups.")
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output with statistics")
    parser.add_argument('-d', '--debug', action='store_true', help="Enable debug output with detailed processing information")
    args = parser.parse_args()

    logs = detect_eq_logs()

    if not logs:
        print("No EQ logs found in the last 7 days.")
        return

    print("Detected EQ log files (last 7 days):")
    for idx, log in enumerate(logs, 1):
        print(f"{idx}. {log}")

    # User selects log file or defaults to first
    try:
        log_index_input = input(f"Select a log to analyze (press Enter to default to 1): ")
        log_index = int(log_index_input) - 1 if log_index_input else 0
        selected_log = logs[log_index]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    # Extract dates from the selected log file
    available_dates = extract_dates_from_log(selected_log)

    if not available_dates:
        print(f"No valid log entries found for {selected_log}.")
        return

    print("\nSelect a date to analyze (most recent first):")
    for idx, date in enumerate(available_dates[:7], 1):
        print(f"{idx}. {date}")

    date_index_input = input(f"Select a date (press Enter to default to {available_dates[0]}): ")
    selected_date = available_dates[int(date_index_input) - 1] if date_index_input else available_dates[0]

    # Capture start time for processing
    start_time = time.time()

    # Parse the log and display the report
    total_active_time, total_afk_time, first_cast_time, last_cast_time, skillups, experience_count, total_log_entries = parse_log(selected_log, selected_date, debug=args.debug)

    # Capture end time and calculate processing time
    end_time = time.time()
    total_processing_time = end_time - start_time

    # Display the report with processing time
    display_report(total_active_time, total_afk_time, total_processing_time, first_cast_time, last_cast_time, skillups, experience_count, total_log_entries, verbose=args.verbose, debug=args.debug)


if __name__ == "__main__":
    main()
