BERTHS = ["SU", "LB", "MB", "UB", "LB", "MB", "UB", "SL"]

def parse_pnr(pnr):
    if not isinstance(pnr, str) or len(pnr) != 10 or not pnr.isascii() or not pnr.isdigit():
        raise ValueError("PNR must be exactly 10 ASCII digits")
    return int(pnr[0]), int(pnr[1:])

def journey_distance(distances_csv):
    if not isinstance(distances_csv, str):
        raise ValueError("Distances must be provided as a comma-separated string")
    parts = distances_csv.split(',')
    if not parts or any(not part.strip() for part in parts):
        raise ValueError("Distances must contain one or more integer values")
    try:
        distances = [int(part.strip()) for part in parts]
    except ValueError as exc:
        raise ValueError("Every distance must be an integer") from exc
    return distances[-1] - distances[0]

def berth_type(seat):
    if not isinstance(seat, str):
        raise ValueError("Seat must be provided as COACH-NUMBER")
    parts = seat.split('-')
    if len(parts) != 2:
        raise ValueError("Seat must contain one coach and one seat number")
    coach, number = (part.strip() for part in parts)
    if not coach:
        raise ValueError("Coach must not be empty")
    if not number.isascii() or not number.isdigit():
        raise ValueError("Seat number must be a positive integer")
    try:
        number = int(number)
    except ValueError as exc:
        raise ValueError("Seat number must be a positive integer") from exc
    if number <= 0:
        raise ValueError("Seat number must be a positive integer")
    return coach.upper(), BERTHS[number % 8]

def main():
    print("==== Running parse_pnr ====")
    user_input = input("Enter a 10 digit PNR (e.g. 4521367890): ")
    result = parse_pnr(user_input)
    print("Zone and Number:", result)

    print("\n==== Running journey_distance ====")
    user_input = input("Enter station distances as CSV (e.g. 0,120,340): ")
    result = journey_distance(user_input)
    print("Total Distance:", result)

    print("\n==== Running berth_type ====")
    user_input = input("Enter coach and seat (e.g. S3-45): ")
    result = berth_type(user_input)
    print("Coach and Berth:", result)

if __name__ == "__main__":
    main()
