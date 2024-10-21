# Hamza Al Shaer 1211162 sec5
# Kareem Al qutob 1211756 sec5
# Lab linux

from datetime import datetime
class Patient:
    def __init__(self, id):
        self.id = id
        self.records = []

    def add_patient(self, patient_id):
        if patient_id in self.patients:
            print(f"Patient with ID {patient_id} already exists.")
        else:
            self.patients[patient_id] = {}
            print(f"Patient with ID {patient_id} added successfully.")

    def get_patient(self, patient_id):
        return self.patients.get(patient_id, "Patient not found.")


class TestRecord:
    def __init__(self, patient_id, test_name, date, time, result, unit, status, end_date=None, end_time=None):
        self.patient_id = patient_id
        self.test_name = test_name
        self.date = date
        self.time = time
        self.result = result
        self.unit = unit
        self.status = status
        self.end_date = end_date
        self.end_time = end_time

    # read all recored has been save in file midecal reocerd

    def print_record(self):
        start_datetime = f"{self.date} {self.time}"

        # Construct the result string based on whether the end date and time are present
        if self.end_date is not None and self.end_time is not None:
            end_datetime = f", {self.end_date} {self.end_time}"
        else:
            end_datetime = ""

        # Format the complete output string
        output = f"{self.patient_id}: {self.test_name}, {start_datetime}, {self.result}, {self.unit}, {self.status}{end_datetime}"

        # Print the output string
        print(output)


class Test:
    def __init__(self, Testname, TestAcronym, unit, turnAround, upperRange=None, LowerRange=None):
        self.Testname = Testname
        self.TestAcronym = TestAcronym
        self.upperRange = upperRange
        self.LowerRange = LowerRange
        self.unit = unit
        self.turnAround = turnAround

    def print_test(self):
        print(f"Test Name: {self.Testname}")
        print(f"Test Acronym: {self.TestAcronym}")
        print(f"Upper Range: {self.upperRange}")
        print(f"Lower Range: {self.LowerRange}")
        print(f"Unit: {self.unit}")
        print(f"Turn Around: {self.turnAround}")


import re


def load_records_from_file(filename):
    records = []
    with open(filename, "r") as file:
        for line in file:
            match = re.match(
                r'(\d{7}): (\w+), (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}), ([\d.]+), ([\w\s/]+), (\w+)(?:, (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}))?',
                line
            )
            if match:
                patient_id = match.group(1)
                test_name = match.group(2)
                start_day = match.group(3)
                start_time = match.group(4)
                result = match.group(5)
                unit = match.group(6)
                status = match.group(7)

                # Optional end date and time
                end_date = match.group(8) if match.group(8) else None
                end_time = match.group(9) if match.group(9) else None

                # Create a TestRecord instance and append it to the records list
                record = TestRecord(patient_id, test_name, start_day, start_time, result, unit, status, end_date,
                                    end_time)
                records.append(record)

    return records


# -------------------------------------------------------------------------------------------------
# validation of iputs
def get_valid_input(prompt, validation_func, error_message):
    while True:
        user_input = input(prompt)
        if validation_func(user_input):
            return user_input
        print(error_message)


def get_valid_input2(prompt, validation_func, name, error_message):
    while True:
        user_input = input(prompt)
        if validation_func(user_input, name):
            return user_input
        print(error_message)


def Valid_ID_Record(id_str):
    return re.fullmatch(r'\d{7}', id_str) is not None


def Valid_Test_Name(name):
    # not empty and not digit
    return bool(name) and not any(char.isdigit() for char in name)


def Valid_Test_Name_Record(name):
    if len(name) != 3 or not name.isalpha() or not name.isupper():
        return False

    # check if the test name record found in midicalTest file as test
    with open("medicalTest.txt", "r") as file:
        for line in file:
            # Extract the symbolic name from the line
            match = re.search(r'\b([A-Z]{3})\b', line)
            if match and match.group(1) == name:
                return True

    print("This not Found in System")
    return False


def Valid_Symbolic_Name(symbolic_name):
    # not empty must 3 char and capital later
    return bool(symbolic_name) and len(symbolic_name) == 3 and symbolic_name.isupper()


def Valid_range(range_values):
    form_rang = r'^[><]\s*\d+(\.\d+)?(\s*,\s*[><]\s*\d+(\.\d+)?)?$'
    return bool(range_values) and re.match(form_rang, range_values)


def Valid_Unit(unit):
    return bool(unit) and not any(char.isdigit() for char in unit) and re.match(r'^[\w\s/]+$', unit)


def Valid_Unit2(unit, test_name):
    if not Valid_Unit(unit):
        print("Error: Invalid unit format.")
        return False

    unit = unit.strip()  # Strip any extra spaces from the unit

    with open("medicalTest.txt", "r") as file:
        for line in file:
            # Extract the full test name and units from the line
            match = re.search(r'(.*?);.*Unit:\s*([\w\s/,-]+)', line)
            if match:
                file_test_name = match.group(1).strip()
                file_units = match.group(2).strip().split(',')

                # Clean up the units
                file_units = [u.strip() for u in file_units]
                symbolic_test_name_match = re.search(r'\b([A-Z]{3})\b', file_test_name)

                if symbolic_test_name_match:
                    file_symbolic_name = symbolic_test_name_match.group(1)

                    # Check if the symbolic test name matches
                    if file_symbolic_name == test_name:
                        # Check if the provided unit matches any of the units in the file
                        if unit in file_units:
                            print("Unit matches.")
                            return True
                        else:
                            print("Error: The unit you entered does not match the unit for the test name you entered.")
                            return False

    print("Error: Test name not found in the medicalTest.txt file.")
    return False


def Valid_Turnaround_Time(turnaround_time):
    return bool(turnaround_time) and re.match(r'^\d{2}-\d{2}-\d{2}$', turnaround_time)


def Valid_Date(date):
    # Check if the date_str matches the YYYY-MM-DD format
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', date):
        try:
            datetime.strptime(date, '%Y-%m-%d')
            return True
        except ValueError:
            return False
    return False


def Valid_Time(time):
    if re.fullmatch(r'\d{2}:\d{2}', time):
        try:
            datetime.strptime(time, '%H:%M')
            return True
        except ValueError:
            return False


def Valid_Status(status):
    return status in {"completed", "pending", "reviewed"}


def Valid_Result(result_str):
    # take integer of floating point and d --> must dicimal not char
    return re.fullmatch(r'^\d+(\.\d+)?$', result_str) is not None


def patients_dict(*recs):
    patients = {}
    for record in recs:
        for rec in record:
            pid = getattr(rec, 'patient_id')
            if pid in patients:
                patients[pid].records.append(rec)
            else:
                p = Patient(pid)
                p.records.append(rec)
                patients[pid] = p
    return patients


def Add_New_Medical_test(tests):
    test_name = get_valid_input("Enter the name of the new medical test: ", Valid_Test_Name,
                                "Invalid input. Test name should not be empty or contain numbers.")
    symbolic_TestName = get_valid_input("Enter the symbolic name of the new medical test (3 Capital Letters): ",
                                        Valid_Symbolic_Name,
                                        "Invalid input. Symbolic name should be exactly 3 Caplital letters.")
    range_values = get_valid_input("Enter the range of the test (e.g., > 70, < 99): ", Valid_range,
                                   "Invalid input. Range should follow the format: > 70, < 99.")
    unit = get_valid_input("Enter the unit of measurement (e.g., mg/dL): ", Valid_Unit,
                           "Invalid input. Unit should be non-empty and can contain letters and/or slashes.")
    turnaround_time = get_valid_input("Enter the turnaround time (e.g., 00-12-06): ", Valid_Turnaround_Time,
                                      "Invalid input. Turnaround time should follow the format: 00-12-06.")

    new_test_entry = f"{test_name} ({symbolic_TestName}); Range: {range_values}; Unit: {unit}, {turnaround_time}\n"

    print(new_test_entry)
    # divide to upper and lower
    lower = None
    upper = None
    if "," in range_values:
        raange = range_values.split(",")
        if len(raange) == 2:
            lower = raange[0].strip()
            upper = raange[1].strip()
    elif ">" in range_values or "<" in range_values:
        if ">" in range_values:
            lower = range_values.strip()
        if "<" in range_values:
            upper = range_values.strip()
    else:
        if ">" in range_values:
            lower = range_values.strip()
        if "<" in range_values:
            upper = range_values.strip()
    with open("medicalTest.txt", "a") as file:
        file.write(new_test_entry)
    t = Test(test_name, symbolic_TestName, unit, turnaround_time, lower, upper)
    tests.append(t)

    print("Medical test added successfully.")


def Add_New_Medical_Record(records, patientsDict, Tests):
    ID_Record = get_valid_input("Enter the 7-digit medical record ID: ", Valid_ID_Record,
                                "Error: ID must be a 7-digit number. Please try again.")
    Test_name = get_valid_input("Enter the 3-character test name: ", Valid_Test_Name_Record,
                                "Error: Test name must be exactly 3 letters. Please try again.")
    Start_Date = get_valid_input("Enter the date (YYYY-MM-DD): ", Valid_Date,
                                 "Error: Date must be in the format YYYY-MM-DD. Please try again.")
    Start_time = get_valid_input("Enter the time (HH:MM): ", Valid_Time,
                                 "Error: Time must be in the format HH:MM. Please try again.")
    result = get_valid_input("Enter the result value: ", Valid_Result,
                             "Error: Result must be a valid number (integer or floating-point). Please try again.")
    unit = get_valid_input2("Enter the unit of measurement: ", Valid_Unit2, Test_name,
                            "Error: Invalid unit. Please try again.")
    status = get_valid_input("Enter the status (completed, pending, reviewed): ", Valid_Status,
                             "Error: Status must be 'completed', 'pending', or 'reviewed'. Please try again.")

    # Find the test in the Tests list to get the turnaround time
    turnaround_time = None
    for test in Tests:
        if test.TestAcronym == Test_name:
            turnaround_time = test.turnAround
            break

    if turnaround_time is None:
        raise ValueError(f"Turnaround time for test {Test_name} not found.")

    # Convert turnaround time to timedelta
    hours, minutes, seconds = map(int, turnaround_time.split('-'))
    turnaround_delta = timedelta(hours=hours, minutes=minutes, seconds=seconds)

    # Calculate end datetime if status is completed
    if status == "completed":
        start_datetime_str = f"{Start_Date} {Start_time}"
        start_datetime = datetime.strptime(start_datetime_str, "%Y-%m-%d %H:%M")
        end_datetime = start_datetime + turnaround_delta
        End_Date = end_datetime.strftime("%Y-%m-%d")
        End_Time = end_datetime.strftime("%H:%M")
    else:
        End_Date = None
        End_Time = None

    # Create a TestRecord object
    r = TestRecord(ID_Record, Test_name, Start_Date, Start_time, result, unit, status, End_Date, End_Time)

    # Construct the new record entry string
    new_record_entry = f"{ID_Record}: {Test_name}, {Start_Date} {Start_time}, {result}, {unit}, {status}"
    if status == "completed":
        new_record_entry += f", {End_Date} {End_Time}"
    new_record_entry += "\n"

    # Append the new record entry to the file
    with open("midecalRecord.txt", "a") as file:
        file.write(new_record_entry)

    # Add the record to the records list
    records.append(r)

    # Add the record to the patient's records in patientsDict
    if ID_Record in patientsDict:
        patientsDict[ID_Record].records.append(r)
    else:
        p = Patient(ID_Record)
        p.records.append(r)
        patientsDict[ID_Record] = p

    print("Medical record added successfully.")

def load_tests_from_file(filename):
    tests = []
    with open(filename, "r") as file:
        for line in file:
            match = re.match(
                r'(.*?)(?: \((.*?)\))?; Range: ([<>]\s*\d+(?:\.\d+)?)(?:, ([<>]\s*\d+(?:\.\d+)?))?; Unit: ([\w\s/]+), (\d{2}-\d{2}-\d{2})',
                line
            )
            if match:
                test_name = match.group(1)
                test_acronym = match.group(2)

                # Identify ranges, only one of these might be present
                range1 = match.group(3)
                range2 = match.group(4)

                # Determine which is the upper and lower range
                lower_range = None
                upper_range = None
                if range1 and range1.startswith("<"):
                    lower_range = range1
                elif range1 and range1.startswith(">"):
                    upper_range = range1

                if range2 and range2.startswith("<"):
                    lower_range = range2
                elif range2 and range2.startswith(">"):
                    upper_range = range2

                unit = match.group(5)
                turn_around = match.group(6)

                t = Test(
                    Testname=test_name,
                    TestAcronym=test_acronym,
                    upperRange=upper_range,
                    LowerRange=lower_range,
                    unit=unit,
                    turnAround=turn_around
                )
                tests.append(t)
    return tests


def update_record_test(records, patientsdict):
    while True:
        patient_id = input("Enter the Patient ID to update records: ")

        # Check if the Patient ID is exactly 7 digits and numeric
        if len(patient_id) != 7 or not patient_id.isdigit():
            print("Error: Patient ID must be exactly 7 digits.")
            continue

        if patient_id not in patientsdict.keys():
            print("Error: No records found for this Patient ID.")
            continue

        break

    # Display all records for the patient
    p = patientsdict[patient_id]

    for idx, record in enumerate(p.records, 1):
        print(f"{idx}. ", end="")
        record.print_record()

    while True:
        try:
            record_num = int(input("Enter the number of the record you want to update: ")) - 1
            if record_num < 0 or record_num >= len(p.records):
                raise ValueError("Invalid record number.")
            break  # Exit loop if the input is valid
        except ValueError as e:
            print(f"Error: {e}. Please enter a valid record number.")

    record_to_update = p.records[record_num]

    while True:
        print("Which part would you like to update?")
        print("1. Test Name")
        print("2. Start Date")
        print("3. Start Time")
        print("4. Result")
        print("5. Unit")
        print("6. Status")
        if getattr(record_to_update, 'end_date') is not None:
            print("7. End Date")
            print("8. End Time")
        print("9. Exit and save changes")

        try:
            field_num = int(input("Enter the number of the field you want to update: "))

            field_map = {
                1: "test_name",
                2: "date",
                3: "time",
                4: "result",
                5: "unit",
                6: "status",
                7: "end_date",
                8: "end_time"
            }

            if field_num not in field_map and field_num != 9:
                print("Error: Invalid field number.")
                continue

            if field_num == 9:
                break

            field_name = field_map[field_num]
            new_value = input(f"Enter the new value for {field_name.replace('_', ' ').title()}: ")

            # Validate inputs based on field type
            if field_name == "test_name":
                while not re.match(r'^[A-Z]{3}$', new_value):
                    print("Error: Test Name must be exactly 3 uppercase letters.")
                    new_value = input(f"Enter the new value for {field_name.replace('_', ' ').title()}: ")

                # Check if the new Test Name exists in medicalTest.txt
                valid_test_name = False
                while not valid_test_name:
                    with open("medicalTest.txt", "r") as file:
                        found = False
                        for line in file:
                            match = re.search(r'\b([A-Z]{3})\b', line)
                            if match and match.group(1) == new_value:
                                found = True
                                break
                        if found:
                            valid_test_name = True
                        else:
                            print("Error: This Test Name is not found in the system. Please enter again.")
                            new_value = input(f"Enter the new value for {field_name.replace('_', ' ').title()}: ")

            elif field_name in {"date", "end_date"}:
                if not re.match(r'^\d{4}-\d{2}-\d{2}$', new_value):
                    print("Error: Date must be in the format YYYY-MM-DD.")
                    continue

            elif field_name in {"time", "end_time"}:
                if not re.match(r'^\d{2}:\d{2}$', new_value):
                    print("Error: Time must be in the format HH:MM.")
                    continue

            elif field_name == "result":
                if not re.match(r'^[\d.]+$', new_value):
                    print("Error: Result must be a number.")
                    continue

            # Update the record using setattr
            setattr(record_to_update, field_name, new_value)

            # Handle status change
            if field_name == "status":
                if new_value == "completed":
                    end_date = input("Enter the End Date (YYYY-MM-DD): ")
                    end_time = input("Enter the End Time (HH:MM): ")
                    setattr(record_to_update, "end_date", end_date)
                    setattr(record_to_update, "end_time", end_time)
                else:
                    setattr(record_to_update, "end_date", None)
                    setattr(record_to_update, "end_time", None)

            print(f"{field_name.replace('_', ' ').title()} updated successfully.")

        except ValueError:
            print("Error: Please enter a valid number.")

    print("All updates have been saved.")


def save_update_records_to_file(records, file_name):
    with open(file_name, "w") as file:
        for record in records:
            record_line = (f"{record.patient_id}: {record.test_name}, {record.date} {record.time}, "
                           f"{record.result}, {record.unit}, {record.status}")
            if record.end_date and record.end_time:
                record_line += f", {record.end_date} {record.end_time}"
            file.write(record_line + "\n")


def update_medicalTest(tests):
    try:
        # Display the contents of the file with line numbers
        with open("medicalTest.txt", "r") as file:
            lines = file.readlines()
            for idx, line in enumerate(lines, 1):
                print(f"{idx}. {line.strip()}")

        # Get the index of the medical test to update
        while True:
            try:
                index = int(input("Enter the index of the medical test you want to update: "))
                if 1 <= index <= len(lines):
                    break
                else:
                    print(f"Error: Index must be between 1 and {len(lines)}.")
            except ValueError:
                print("Error: Please enter a valid number.")

        # Show the medical test selected for update
        selected_test = lines[index - 1].strip()
        print(f"Selected Test: {selected_test}")

        print("What would you like to update?")
        print("1. Name")
        print("2. Symbolic Name")
        print("3. Range")
        print("4. Unit")
        print("5. Time")

        while True:
            try:
                choice = int(input("Enter the number corresponding to the field you want to update: "))
                if 1 <= choice <= 5:
                    break
                else:
                    print("Error: Please choose a number between 1 and 5.")
            except ValueError:
                print("Error: Please enter a valid number.")

        # Split the selected test by ';' to get the different parts
        parts = re.split(r';\s*', selected_test)

        # Find the corresponding Test object in the tests list
        symbolic_name_match = re.search(r'\((\w+)\)', parts[0])
        if symbolic_name_match:
            symbolic_name = symbolic_name_match.group(1)
            test_obj = next((t for t in tests if t.TestAcronym == symbolic_name), None)
        else:
            print("Error: Could not find symbolic name in the selected test.")
            return

        if not test_obj:
            print("Error: No corresponding Test object found.")
            return

        if choice == 1:
            while True:
                new_value = input("Enter the new Name: ")
                if any(char.isdigit() for char in new_value):
                    print("Error: Name cannot contain digits. Please enter a valid name.")
                    continue
                else:
                    symbolic_start = parts[0].find('(')
                    if symbolic_start != -1:
                        parts[0] = new_value + " " + parts[0][symbolic_start:]
                        test_obj.Testname = new_value
                        break

        elif choice == 2:
            while True:
                new_value = input("Enter the new Symbolic Name (3 capital letters): ")
                if re.match(r'^[A-Z]{3}$', new_value):
                    parts[0] = re.sub(r'\(\w+\)', f"({new_value})", parts[0])
                    test_obj.TestAcronym = new_value
                    break
                else:
                    print("Error: Symbolic Name must be exactly 3 capital letters.")

        elif choice == 3:
            while True:
                new_value = input("Enter the new Range (e.g., '> 90', '<90', '>80,<70'): ")
                if re.match(r'^[<>]\s*\d+(\.\d+)?(,\s*[<>]\s*\d+(\.\d+)?)?$', new_value):
                    parts[1] = f"Range: {new_value}"
                    ranges = new_value.split(',')
                    test_obj.LowerRange = ranges[0].strip() if ranges[0].strip().startswith('>') else None
                    test_obj.upperRange = ranges[-1].strip() if ranges[-1].strip().startswith('<') else None
                    break
                else:
                    print("Error: Invalid range format.")

        elif choice == 4:
            while True:
                new_value = input("Enter the new Unit: ")
                if re.search(r'\d', new_value):
                    print("Error: Unit cannot contain digits.")
                else:
                    parts[2] = f"Unit: {new_value}, {parts[2].split(', ', 1)[-1]}"
                    test_obj.unit = new_value
                    break

        elif choice == 5:
            while True:
                new_value = input("Enter the new Time (HH-MM-SS): ")
                if re.match(r'^\d{2}-\d{2}-\d{2}$', new_value):
                    parts[2] = f"{parts[2].split(', ', 1)[0]}, {new_value}"
                    test_obj.turnAround = new_value
                    break
                else:
                    print("Error: Time must be in the format HH-MM-SS.")

        lines[index - 1] = '; '.join(parts) + '\n'
        with open("medicalTest.txt", "w") as file:
            file.writelines(lines)

        print("Medical test updated successfully.")

    except FileNotFoundError:
        print("Error: medicalTest.txt file not found.")


def general_filter(recs, field, value):
    filtered_recs = []
    for rec in recs:
        if getattr(rec, field) == value:
            filtered_recs.append(rec)
    return filtered_recs


# filter for abnormal
def abnormal_filter(recs, tests):
    filtered_recs = []
    for rec in recs:
        type = getattr(rec, 'test_name')
        for test in tests:
            if getattr(test, 'TestAcronym') == type:
                filterTest = test
                if getattr(filterTest, 'upperRange') is not None:
                    uprange = getattr(filterTest, 'upperRange')
                    uprange = float(uprange.replace(">", "").strip())
                    print(uprange)
                    if float(getattr(rec, 'result')) > uprange:
                        filtered_recs.append(rec)
                        break
                if getattr(filterTest, 'LowerRange') is not None:
                    lowrange = getattr(filterTest, 'LowerRange')
                    lowrange = float(lowrange.replace("<", "").strip())
                    if float(getattr(rec, 'result')) < lowrange:
                        filtered_recs.append(rec)
    return filtered_recs


def period(rec, date1, time1, date2, time2):
    filtered_recs = []
    for rec in recs:
        if getattr(rec, 'date') >= date1:
            if getattr(rec, 'date') == date1:
                if getattr(rec, 'time') <= time1:
                    continue
            if getattr(rec, 'end_date') is not None:
                if getattr(rec, 'end_date') <= date2:
                    if getattr(rec, 'end_date') == date2:
                        if getattr(rec, 'end_date') >= time2:
                            continue
                    filtered_recs.append(rec)
    return filtered_recs



from datetime import datetime, timedelta


def filterTT(records, time1, time2):
    filtered_recs = []
    dateformat2 = "%d-%H-%M"

    # Parse the time intervals as timedelta
    days1, hours1, minutes1 = map(int, time1.split('-'))
    days2, hours2, minutes2 = map(int, time2.split('-'))
    interval1 = timedelta(days=days1, hours=hours1, minutes=minutes1)
    interval2 = timedelta(days=days2, hours=hours2, minutes=minutes2)

    # Ensure interval1 is the smaller (earlier) interval
    if interval1 > interval2:
        interval1, interval2 = interval2, interval1

    # Loop through each record
    for rec in records:
        if getattr(rec, 'end_date') is None or getattr(rec, 'end_time') is None:
            continue

        # Concatenate date and time strings
        start = f"{rec.date} {rec.time}"
        end = f"{rec.end_date} {rec.end_time}"

        # Define the format for datetime parsing
        dateformat = "%Y-%m-%d %H:%M"

        # Convert start and end to datetime objects
        start_datetime = datetime.strptime(start, dateformat)
        end_datetime = datetime.strptime(end, dateformat)

        # Calculate the difference between end and start
        difference = end_datetime - start_datetime

        # Check if the difference falls within the specified intervals
        if interval1 <= difference <= interval2:
            filtered_recs.append(rec)

    return filtered_recs


from datetime import date

recs = load_records_from_file("midecalRecord.txt")
r = filterTT(recs, "00-01-06", "09-12-12")
for rr in r:
    rr.print_record()


def Min_Max_Avg_result(recs, tests):
    for test in tests:
        acronym = test.TestAcronym
        max_value = float('-inf')  # to any first number take it as max
        min_value = float('inf')  # to any first number take it as min
        sum_value = 0
        count = 0
        # check in all recoreds
        for rec in recs:
            if rec.test_name == acronym:
                result = float(rec.result)

                if result > max_value:
                    max_value = result
                if result < min_value:
                    min_value = result

                sum_value += result
                count += 1

        if count > 0:
            avg_value = sum_value / count
            print(f"Test {acronym}: Max = {max_value}, Min = {min_value}, Avg = {avg_value:.2f}")
        else:
            print(f"Test {acronym} not found in records. Max=0, Min =0, Avg = 0")


def Min_Max_Avg_TurnAround(tests):
    max_turnaround = timedelta(days=0, hours=0, minutes=0)
    min_turnaround = timedelta(days=365 * 10)  # Large enough finite value
    total_turnaround = timedelta(days=0, hours=0, minutes=0)
    count = 0

    for test in tests:
        dd, hh, mm = map(int, test.turnAround.split('-'))

        turnaround_time = timedelta(days=dd, hours=hh, minutes=mm)

        if turnaround_time > max_turnaround:
            max_turnaround = turnaround_time
        if turnaround_time < min_turnaround:
            min_turnaround = turnaround_time

        total_turnaround += turnaround_time
        count += 1
    avg_turnaround = total_turnaround / count if count > 0 else timedelta(days=0, hours=0, minutes=0)

    # Convert results back to the format dd-hh-mm for output
    max_turnaround_str = f"{max_turnaround.days:02d}-{max_turnaround.seconds // 3600:02d}-{(max_turnaround.seconds // 60) % 60:02d}"
    min_turnaround_str = f"{min_turnaround.days:02d}-{min_turnaround.seconds // 3600:02d}-{(min_turnaround.seconds // 60) % 60:02d}"
    avg_turnaround_str = f"{avg_turnaround.days:02d}-{avg_turnaround.seconds // 3600:02d}-{(avg_turnaround.seconds // 60) % 60:02d}"

    print(f"Max Turnaround Time: {max_turnaround_str}")
    print(f"Min Turnaround Time: {min_turnaround_str}")
    print(f"Avg Turnaround Time: {avg_turnaround_str}")


def filters(recs, tests):
    filtered = []
    print("Chooes the type of filter  (1-6) :")
    print("1.Patient ID")
    print("2.Test Name")
    print("3.Abnormal tests")
    print("4.within a specific period (start and end dates)")
    print("5.Test status")
    print("6.Test turnaround time within a period (minimum and maximum turnaround time)")

    ch1 = input()
    if ch1 == '1':
        ID = get_valid_input("Enter the ID of patinet you want filter it :", Valid_ID_Record,
                             "Error: ID must be a 7-digit number. Please try again.")
        filtered = general_filter(recs, "patient_id", ID)
        for f in filtered:
            f.print_record()
    elif ch1 == '2':
        NAME = get_valid_input("Enter the 3-character test name: ", Valid_Test_Name_Record,
                               "Error: Test name must be exactly 3 letters. Please try again.")
        filtered = general_filter(recs, "test_name", NAME)
        for f in filtered:
            f.print_record()
    elif ch1 == '3':
        filtered = abnormal_filter(recs, tests)
        for f in filtered:
            f.print_record()
    elif ch1 == '4':
        Start_Date = get_valid_input("Enter the start date (YYYY-MM-DD): ", Valid_Date,
                                     "Error: Date must be in the format YYYY-MM-DD. Please try again.")
        Start_time = get_valid_input("Enter the start time (HH:MM): ", Valid_Time,
                                     "Error: Time must be in the format HH:MM. Please try again.")
        END_Date = get_valid_input("Enter the end date (YYYY-MM-DD): ", Valid_Date,
                                   "Error: Date must be in the format YYYY-MM-DD. Please try again.")
        END_time = get_valid_input("Enter the end time (HH:MM): ", Valid_Time,
                                   "Error: Time must be in the format HH:MM. Please try again.")
        filtered = period(recs, Start_Date, Start_time, END_Date, END_time)
        for f in filtered:
            f.print_record()
    elif ch1 == '5':
        status = get_valid_input("Enter the status (completed, pending, reviewed): ", Valid_Status,
                                 "Error: Status must be 'completed', 'pending', or 'reviewed'. Please try again.")
        filtered = general_filter(recs, "status", status)
        for f in filtered:
            f.print_record()
    elif ch1 == '6':
        Start_time1 = get_valid_input("Enter the start turnaround time (e.g., 00-12-06): ", Valid_Turnaround_Time,
                                      "Invalid input. Turnaround time should follow the format: 00-12-06.")
        End_time1 = get_valid_input("Enter the end turnaround time (e.g., 00-12-06): ", Valid_Turnaround_Time,
                                    "Invalid input. Turnaround time should follow the format: 00-12-06.")
        filtered = filterTT(recs, Start_time1, End_time1)
        for f in filtered:
            f.print_record()
    else:
        print("invalid choise , enter agian")
        filters(recs, tests)
    while True:
        x = input(" Tou want use the filter options again ? yes or no ")
        x = x.upper()
        if x == "YES":
            filters(filtered,tests)
            break
        elif x == "NO":
                print("select the service you want make (1-2) :")
                print("1.Maximum and Minimum and Aerage for tests Results")
                print("2.Maximum and Minimum and Aerage for Turnaround Time")
                while True:
                    ch2 = input()
                    if ch2 == '1':
                        Min_Max_Avg_result(recs, tests)
                        break
                    elif ch2 == '2':
                        Min_Max_Avg_TurnAround(tests)
                        break
                    else:
                        print("Enter the valied number")
                        continue
                break
        else:
            continue



recs = load_records_from_file("midecalRecord.txt")
patientsdic = patients_dict(recs)
tests = load_tests_from_file("medicalTest.txt")


while True:
    print("select the service you want make (1-9) :")
    print("1.Add new medical test")
    print("2.Add a new medical test record")
    print("3.Update patient records including all fields")
    print("4.Update medical tests in the medicalTest file")
    print("5.Filter medical tests")
    print("6.exit")
    choice = input()

    if choice == '1':
        Add_New_Medical_test(tests)
    elif choice == '2':
        Add_New_Medical_Record(records=recs, patientsDict=patientsdic, Tests=tests)
    elif choice == '3':
        update_record_test(recs, patientsdic)
        save_update_records_to_file(recs, "midecalRecord.txt")
    elif choice == '4':
        update_medicalTest(tests)
    elif choice == '5':
        filters(recs, tests)
    elif choice == '6':
        exit(0)
        break