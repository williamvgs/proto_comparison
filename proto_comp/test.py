import google.protobuf.text_format as text_format
import thruster_v15_pb2  

def compare_protobuf_files(file_path1, file_path2):
    try:
        # Load the content of the protobuf files
        with open(file_path1, 'r') as file1:
            content1 = file1.read()

        with open(file_path2, 'r') as file2:
            content2 = file2.read()

        # Parse the content into protobuf messages
        message1 = thruster_v15_pb2.ThrusterParameters()  
        text_format.Parse(content1, message1)

        message2 = thruster_v15_pb2.ThrusterParameters() 
        text_format.Parse(content2, message2)

        # Compare the messages
        result = compare_messages(message1, message2)

        if not result:
            print("Protobuf files are identical.")
        else:
            for diff in result:
                print(diff)

    except Exception as e:
        print(f"An error occurred: {e}")

def compare_messages(msg1, msg2, prefix=''):
    differences = []

    # Iterate through the fields of the message
    for field, value1 in msg1.ListFields():
        try:
            # Find the corresponding field in msg2 dynamically
            field2 = msg2.DESCRIPTOR.fields_by_name.get(field.name)

            if field2:
                value2 = getattr(msg2, field.name, None)

                # Check if the values are equal
                if value1 != value2:
                    differences.append(f'{prefix}.{field.name} differs: {value1} != {value2}')
            else:
                differences.append(f'{prefix}.{field.name} missing in the second message')

        except Exception as e:
            print(f"An error occurred while comparing fields: {e}")

    # Check for fields present in the second message but not in the first
    for field, value2 in msg2.ListFields():
        try:
            if not hasattr(msg1, field.name):
                differences.append(f'{prefix}.{field.name} missing in the first message')

        except Exception as e:
            print(f"An error occurred while comparing fields: {e}")

    # Recursively check nested messages
    for subfield, submsg1 in msg1.ListFields():
        try:
            submsg2 = getattr(msg2, subfield.name, None)
            if submsg2 is not None:
                differences.extend(compare_messages(submsg1, submsg2, f'{prefix}.{subfield.name}'))

        except Exception as e:
            print(f"An error occurred while comparing nested messages: {e}")

    return differences

if __name__ == "__main__":
    file_path1 = 'v1.5/35042A.prototxt'
    file_path2 = 'v1.5/35042B.prototxt'

    result = compare_protobuf_files(file_path1, file_path2)

    if not result:
        print("Protobuf files are identical.")
    else:
        for diff in result:
            print(diff)
