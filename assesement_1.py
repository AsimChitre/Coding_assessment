"""Reading a key-value pair input from a file and flatten the data for data ingestion"""

input_file = open('input_file.txt', 'r', encoding='utf-8')
dictionary = []
for line in input_file:
    lines = line.split("^^")                  #splitting the data into different columns
    row = ""
    header = ""
    for i, column in enumerate(lines):
        key, values = column.split("=", 1)  # here, we have to do just 1 split (key:[values])
        translating_table = (str.maketrans("", "", "^="))
        values = values.translate(translating_table)
        if i != 0:                              #all other rows
            header = header + "|" + key
            row = row + "|" + values
        else:                                   #header row
            header = key
            row = values

    dictionary.append(row)

with open("final_output.txt", 'w', encoding='utf-8') as final:
    final.write(header)
    final.write("\n")
    final.writelines(dictionary)



