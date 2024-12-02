import random

def create_random_file(file):
    try:
        f = open(file, 'w')
        for i in range(100):
            numbers = []
            for j in range(20): 
                num = random.randint(1, 100)
                numbers.append(str(num))
            f.write(' '.join(numbers) + '\n')
        f.close()
        print("File created:", file)
    except:
        print("Something went wrong creating the file.")

def process_file(input_file, output_file):
    try:
        f = open(input_file, 'r')
        lines = f.readlines()
        f.close()

        result = []
        for line in lines:
            nums = line.split()
            filtered = []
            for n in nums:
                if int(n) > 40:
                    filtered.append(n)
            result.append(filtered)

        f_out = open(output_file, 'w')
        for line in result:
            f_out.write(' '.join(line) + '\n')
        f_out.close()

        print("Filtered data saved to:", output_file)
    except:
        print("Something went wrong processing the file.")

def read_file(filename):
    try:
        f = open(filename, 'r')
        for line in f:
            print(line.strip())
        f.close()
    except:
        print("Couldn't read the file.")

if __name__ == "__main__":
    input_file = "random_numbers.txt"
    output_file = "filtered_numbers.txt"

    create_random_file(input_file)
    process_file(input_file, output_file)
    print("Filtered file contents:")
    read_file(output_file)
