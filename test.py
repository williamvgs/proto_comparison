import difflib

def compare_prototxt_files(file_path_old, file_path_new):
    with open(file_path_old, 'r') as f_old, open(file_path_new, 'r') as f_new:
        lines_old = f_old.readlines()
        lines_new = f_new.readlines()

        # Create a unified diff
        diff_lines = difflib.unified_diff(lines_old, lines_new, lineterm='')

        # Convert the diff lines back to a string
        diff_str = '\n'.join(diff_lines)

        return diff_str

# Example usage:
old_prototxt_path = 'C:/Users/William/Documents/brunvoll_utplasering/v1.6/Thruster_protocol_D.prototxt'
new_prototxt_path = 'C:/Users/William/Documents/brunvoll_utplasering/v1.6/Thruster_protocol_E.prototxt'

diff_str = compare_prototxt_files(old_prototxt_path, new_prototxt_path)

# Print or save the diff string as needed
print(diff_str)
