import sys

def read_file_to_list(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def write_list_to_file(output_path, data_list):
    with open(output_path, 'w') as file:
        for item in data_list:
            file.write(f"{item}\n")

def compare_lists(file1, file2, shared_output, unique_output):
    list1 = set(read_file_to_list(file1))
    list2 = set(read_file_to_list(file2))

    shared_items = list1.intersection(list2)
    unique_items = list1.symmetric_difference(list2)

    write_list_to_file(shared_output, sorted(shared_items))
    write_list_to_file(unique_output, sorted(unique_items))

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py <file1> <file2> <shared_output> <unique_output>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]
    shared_output = sys.argv[3]
    unique_output = sys.argv[4]

    compare_lists(file1, file2, shared_output, unique_output)

    print("Comparison complete. Shared and unique items saved to files.")

