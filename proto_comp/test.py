import traceback
import google.protobuf.text_format as text_format
import thruster_v15_pb2  

def compare_messages(msg1, msg2, prefix=''):
    differences = []

    for field, value1 in msg1.ListFields():
        try:
            field2 = msg2.DESCRIPTOR.fields_by_name.get(field.name)

            if field2:
                value2 = getattr(msg2, field.name, None)

                if value1 != value2:
                    differences.append(f'{prefix}.{field.name} differs: {value1} != {value2}')
            else:
                differences.append(f'{prefix}.{field.name} missing in the second message')

        except Exception as e:
            print(f"An error occurred while comparing fields: {e}")

    for field, value2 in msg2.ListFields():
        try:
            if not hasattr(msg1, field.name):
                differences.append(f'{prefix}.{field.name} missing in the first message')

        except Exception as e:
            print(f"An error occurred while comparing fields: {e}")

    for subfield, submsg1 in msg1.ListFields():
        try:
            submsg2 = getattr(msg2, subfield.name, None)
            if submsg2 is not None:
                differences.extend(compare_messages(submsg1, submsg2, f'{prefix}.{subfield.name}'))

        except Exception as e:
            print(f"An error occurred while comparing nested messages: {e}")

    return differences

def load_protobuf_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def parse_protobuf_content(content):
    message = thruster_v15_pb2.ThrusterParameters()
    text_format.Parse(content, message)
    return message

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

if __name__ == "__main__":
    file_path1 = '../v1.5/35042A.prototxt'
    file_path2 = '../v1.5/35042B.prototxt'

    compare_protobuf_files(file_path1, file_path2)
