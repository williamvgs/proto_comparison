import argparse
import traceback
import google.protobuf.text_format as text_format
import json
import importlib

# Compares Protobuf and makes a dictionary
def compare_messages(msg1, msg2, prefix=''):
    differences = []

    # Convert messages to dictionaries for easier comparison
    dictionary_1 = message_to_dictionary(msg1)
    dictionary_2 = message_to_dictionary(msg2)

    # Compare dictionaries
    differences = compare_dictionary(dictionary_1, dictionary_2, prefix)

    return differences

# Compares dictionaries made and prints differences
def compare_dictionary(dictionary1, dictionary2, prefix=''):
    differences = []

    # Check fields in the dictionary 1 and prints differences
    for field, value1 in dictionary1.items():
        if field not in dictionary2:
            differences.append(f"\n>>> {field}: {value1}\n>>> {field}: None")
        else:
            value2 = dictionary2[field]

            if value1 != value2:
                differences.append(f"\n>>> {field}: {value1}\n>>> {field}: {value2}")

    # Check fields in the dictionary 2 and prints differences
    for field, value2 in dictionary2.items():
        if field not in dictionary1:
            differences.append(f"\n>>> {field}: None\n>>> {field}: {value2}")

    return differences

# Runs through Proto file and converts to a python Dictionary
def message_to_dictionary(message):
    result = {}

    if hasattr(message, 'ListFields'):
        for field, value in message.ListFields():
            if value is not None:
                if isinstance(value, str):
                    result[field.name] = value
                elif hasattr(value, 'value') and value.HasField('value'):
                    result[field.name] = value.value
                elif hasattr(value, 'values') and value.HasField('values'):
                    result[field.name] = list(value.values)
                else:
                    result[field.name] = message_to_dictionary(value)
            else:
                result[field.name] = None

    return result

# Loads Protobuf files and reads them
def load_protobuf_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Imports Thruster v1.5 content and returns as message
def parse_protobuf_content_v15(content):
    import thruster_v15_pb2
    message = thruster_v15_pb2.ThrusterParameters()
    text_format.Parse(content, message)
    return message

# Imports Thruster v1.6 content and returns as message
def parse_protobuf_content_v16(content):
    import thruster_v16_pb2
    message = thruster_v16_pb2.ThrusterParameters()
    text_format.Parse(content, message)
    return message

# Here is where you Compare protobuf files
def compare_protobuf_files(file_path1, file_path2, save_json=False, json_file_path=None):
    try:
        content1 = load_protobuf_file(file_path1)
        content2 = load_protobuf_file(file_path2)

        # Attempt to import v1.5
        try:
            from thruster_v15_pb2 import ThrusterParameters as Thruster_v15
            message1 = parse_protobuf_content_v15(content1)
            message2 = parse_protobuf_content_v15(content2)
            differences = compare_messages(message1, message2)
        except ImportError:
            differences = []  # No differences if v1.5 is not available

        if not differences:
            print("Protobuf files are identical.")
        else:
            for diff in differences:
                print(diff)

            if save_json and json_file_path:
                save_as_json(differences, json_file_path)

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

        try:
            content1 = load_protobuf_file(file_path1)
            content2 = load_protobuf_file(file_path2)

            # Import v1.6
            from thruster_v16_pb2 import ThrusterParameters as Thruster_v16
            message1 = parse_protobuf_content_v16(content1)
            message2 = parse_protobuf_content_v16(content2)

            differences = compare_messages(message1, message2)

            if not differences:
                print("Protobuf files are identical.")
            else:
                for diff in differences:
                    print(diff)

                if save_json and json_file_path:
                    save_as_json(differences, json_file_path)
        except ImportError:
            print("Error: Both versions (1.5 and 1.6) not found.")

# Here you count the number of differences
def count_differences(file_path1, file_path2):
    try:
        content1 = load_protobuf_file(file_path1)
        content2 = load_protobuf_file(file_path2)

        # Attempt to import v1.5
        try:
            from thruster_v15_pb2 import ThrusterParameters as Thruster_v15
            message1 = parse_protobuf_content_v15(content1)
            message2 = parse_protobuf_content_v15(content2)
            differences = compare_messages(message1, message2)
        except ImportError:
            differences = []  # No differences if v1.5 is not available

        print(f"Number of differences: {len(differences)}")

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

# Save differences as JSON
def save_as_json(differences, json_file_path):
    with open(json_file_path, 'w') as json_file:
        json.dump(differences, json_file, indent=2)

    print(f"Differences saved as JSON in {json_file_path}")

# ====== MAIN ==========

# Here is where the program runs
if __name__ == "__main__":
    # Defines custom arguments
    parser = argparse.ArgumentParser(description='Commands')
    parser.add_argument('-x', nargs=2, metavar=('file1', 'file2'), help='Runs a comparison')
    parser.add_argument('-c', nargs=2, metavar=('--count'), help='Counts how many differences there are')
    parser.add_argument('-j', nargs=2, metavar=('file1', 'file2'), help='Saves differences as JSON file')
    args = parser.parse_args()

    if args.x:
        file_path1, file_path2 = args.x
        compare_protobuf_files(file_path1, file_path2)
    elif args.c:
        file_path1, file_path2 = args.c
        count_differences(file_path1, file_path2)
    elif args.j:
        file_path1, file_path2 = args.j
        json_file_path = "differences.json"  # You can customize the file path if needed
        compare_protobuf_files(file_path1, file_path2, save_json=True, json_file_path=json_file_path)
