import argparse #imports library for cmd prefixes such as -x 
import traceback #imports library to help debug "Improves error messages"
import google.protobuf.text_format as text_format #imports protobuf library to read files
import thruster_v15_pb2  #imports thruster v1.5


#Compares Protobuf and makes a dictionary
def compare_messages(msg1, msg2, prefix=''):
    differences = []

    # Convert messages to dictionaries for easier comparison
    dictionary_1 = message_to_dictionary(msg1)
    dictionary_2 = message_to_dictionary(msg2)

    # Compare dictionaries
    differences = compare_dictionary(dictionary_1, dictionary_2, prefix)

    return differences

#Compares dictionaries made and prints differences 
def compare_dictionary(dictionary1, dictionary2, prefix=''):
    differences = []

    #Check fields in the dictionary 1 and prints differences
    for field, value1 in dictionary1.items():
        if field not in dictionary2:
            differences.append(f"\n>>> {field}: {value1}\n>>> {field}: None")
        else:
            value2 = dictionary2[field]

            if value1 != value2:
                differences.append(f"\n>>> {field}: {value1}\n>>> {field}: {value2}")

    #Check fields in the dictionary 2 and prints differences
    for field, value2 in dictionary2.items():
        if field not in dictionary1:
            differences.append(f"\n>>> {field}: None\n>>> {field}: {value2}")

    return differences

#Runs through Proto file and converts to a python Dictionary
def message_to_dictionary(message):
    """Convert Protobuf message to dictionary."""
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


#Loads Protobuf files and reads them
def load_protobuf_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()


#Imports Thruster v1.5 content and returns as message
def parse_protobuf_content(content):
    message = thruster_v15_pb2.ThrusterParameters()
    text_format.Parse(content, message)
    return message


#Here is where you Compare protobuf files 
def compare_protobuf_files(file_path1, file_path2):
    try:
        content1 = load_protobuf_file(file_path1)
        content2 = load_protobuf_file(file_path2)

        message1 = parse_protobuf_content(content1)
        message2 = parse_protobuf_content(content2)

        differences = compare_messages(message1, message2)

        if not differences:
            print("Protobuf files are identical.")
        else:
            for diff in differences:
                print(diff)

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()



#Here is where you count ammount of differences 
def count_differences(file_path1, file_path2):
    try:
        content1 = load_protobuf_file(file_path1)
        content2 = load_protobuf_file(file_path2)

        message1 = parse_protobuf_content(content1)
        message2 = parse_protobuf_content(content2)

        differences = compare_messages(message1, message2)

        print(f"Number of differences: {len(differences)}")

    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()


#====== MAIN ==========

#Here is where the program runs
if __name__ == "__main__":
     #Defines custom arguments
    parser = argparse.ArgumentParser(description='Commands')                                                        
    parser.add_argument('-x', nargs=2, metavar=('file1', 'file2'), help='Runs a comparison')                         
    parser.add_argument('-c', nargs=2, metavar=('--count') , help='Counts how many differences there are')          

    args = parser.parse_args()

    if args.x:
        file_path1, file_path2 = args.x
        compare_protobuf_files(file_path1, file_path2)
    elif args.c:
        file_path1, file_path2 = args.c
        count_differences(file_path1, file_path2)
