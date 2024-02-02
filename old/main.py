import argparse
import traceback
import google.protobuf.text_format as text_format
import thruster_v15_pb2
import thruster_v16_pb2
import json

def compare_messages(msg1, msg2, prefix=''):
    differences = []
    dictionary_1 = message_to_dictionary(msg1)
    dictionary_2 = message_to_dictionary(msg2)
    differences = compare_dictionary(dictionary_1, dictionary_2, prefix)
    return differences

def compare_dictionary(dictionary1, dictionary2, prefix=''):
    differences = []
    for field, value1 in dictionary1.items():
        if field not in dictionary2:
            differences.append(f"\n>>> {field}: {value1}\n>>> {field}: None")
        else:
            value2 = dictionary2[field]
            if value1 != value2:
                differences.append(f"\n>>> {field}: {value1}\n>>> {field}: {value2}")

    for field, value2 in dictionary2.items():
        if field not in dictionary1:
            differences.append(f"\n>>> {field}: None\n>>> {field}: {value2}")

    return differences

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

def load_protobuf_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def parse_protobuf_content(content, thruster_module):
    message = thruster_module.ThrusterParameters()
    text_format.Parse(content, message)
    return message

def import_thruster_module(thruster_name):
    if thruster_name.lower() == 'thruster_name':
        import thruster_v15_pb2 as thruster_module
    elif thruster_name.lower() == 'thrustername':
        import thruster_v16_pb2 as thruster_module
    else:
        raise ValueError(f"Invalid thruster name: {thruster_name}")
    return thruster_module

def compare_protobuf_files(file_path1, file_path2, thruster_name, save_json=False, json_file_path=None):
    try:
        content1 = load_protobuf_file(file_path1)
        content2 = load_protobuf_file(file_path2)

        thruster_module = import_thruster_module(thruster_name)

        message1 = parse_protobuf_content(content1, thruster_module)
        message2 = parse_protobuf_content(content2, thruster_module)

        differences = compare_messages(message1, message2)

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

def count_differences(file_path1, file_path2, thruster_name):
    try:
        content1 = load_protobuf_file(file_path1)
        content2 = load_protobuf_file(file_path2)

        thruster_module = import_thruster_module(thruster_name)

        message1 = parse_protobuf_content(content1, thruster_module)
        message2 = parse_protobuf_content(content2, thruster_module)

        differences = compare_messages(message1, message2)

        print(f"Number of differences: {len(differences)}")

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

def save_as_json(differences, json_file_path):
    with open(json_file_path, 'w') as json_file:
        json.dump(differences, json_file, indent=2)

    print(f"Differences saved as JSON in {json_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Commands')
    parser.add_argument('-x', nargs=3, metavar=('file1', 'file2', 'thruster_name'), help='Runs a comparison')
    parser.add_argument('-c', nargs=3, metavar=('--count'), help='Counts how many differences there are')
    parser.add_argument('-j', nargs=3, metavar=('file1', 'file2', 'thruster_name'), help='Saves differences as JSON file')
    args = parser.parse_args()

    if args.x:
        file_path1, file_path2, thruster_name = args.x
        compare_protobuf_files(file_path1, file_path2, thruster_name)
    elif args.c:
        file_path1, file_path2, thruster_name = args.c
        count_differences(file_path1, file_path2, thruster_name)
    elif args.j:
        file_path1, file_path2, thruster_name = args.j
        json_file_path = "differences.json"  # You can customize the file path if needed
        compare_protobuf_files(file_path1, file_path2, thruster_name, save_json=True, json_file_path=json_file_path)
