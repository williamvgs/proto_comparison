import argparse

def fetch_files(file_path1, file_path2):
    with open(file_path1, 'r') as file:
        file_content2 = file.readlines()

    with open(file_path2, 'r') as file:
        file_content1 = file.readlines()

    return file_content1, file_content2

def compare(file_content1, file_content2):
    differences = []
    max_lines = max(len(file_content1), len(file_content2))

    for i in range(max_lines):
        line1 = file_content1[i].strip() if i < len(file_content1) else ''
        line2 = file_content2[i].strip() if i < len(file_content2) else ''

        if line1 != line2:
            differences.append((line1, line2))

    return differences

def compare_case_insensitive(file_content1, file_content2):
    differences = []
    max_lines = max(len(file_content1), len(file_content2))

    for i in range(max_lines):
        line1 = file_content1[i].strip().lower() if i < len(file_content1) else ''
        line2 = file_content2[i].strip().lower() if i < len(file_content2) else ''

        # Compare lines after converting to lowercase
        if line1 != line2:
            differences.append((line1, line2))

    return differences

def compare_with_line_numbers(file_content1, file_content2):
    differences = []
    max_lines = max(len(file_content1), len(file_content2))

    for i in range(max_lines):
        line1 = file_content1[i].strip() if i < len(file_content1) else ''
        line2 = file_content2[i].strip() if i < len(file_content2) else ''

        if line1 != line2:
            differences.append((i + 1, line1, line2))  # Include line number in the result

    return differences


def main():
    parser = argparse.ArgumentParser(description='Process two files.')
    parser.add_argument('-x', nargs='*', help='Runs a case-sensitive comparison')
    parser.add_argument('-c', nargs='*', help='Counts how many differences there are')
    parser.add_argument('-i', nargs='*', help='Runs a case-insensitive comparison')
    parser.add_argument('-xn', nargs='*', help='Runs a case-sensitive comparison and shows what line the difference is on ')
    parser.add_argument('-e', '--exit', action='store_true', help='Exit the program after the current iteration')

    while True:
        args = parser.parse_args()


        if args.x:
            file_path1, file_path2 = args.x
            file_content1, file_content2 = fetch_files(file_path1, file_path2)
            differences = compare(file_content1, file_content2)
            for diff in differences:
                print(f">>> {diff[0]}\n>>> {diff[1]}\n")
        elif args.c:
            file_path1, file_path2 = args.c
            differences = compare(file_path1, file_path2)
            count = len(differences)
            print(f"\nNumber of differences: {count}")
        elif args.i:
            file_path1, file_path2 = args.i
            file_content1, file_content2 = fetch_files(file_path1, file_path2)
            differences = compare_case_insensitive(file_content1, file_content2)
            for diff in differences:
                print(f">>> {diff[0]}\n>>> {diff[1]}\n")
        elif args.xn:
            file_path1, file_path2 = args.xn
            file_content1, file_content2 = fetch_files(file_path1, file_path2)
            differences = compare_with_line_numbers(file_content1, file_content2)
            for diff in differences:
                print(f"Line {diff[0]}: >>> {diff[1]}\nLine {diff[0]}: >>> {diff[2]}\n")
        elif args.e:
            break
        else:
            print("Please provide appropriate options. Use -h for help.")

if __name__ == "__main__":
    main()
