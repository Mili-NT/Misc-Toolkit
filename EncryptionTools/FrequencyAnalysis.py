import string
from os import path
from concurrent.futures import ThreadPoolExecutor

def file_input():
    def resource_assignment(tc):
        while True:
            finput = input("Enter the path to file (including file extension): ")
            if path.isfile(finput) is True:
                thread_dict["thread{0}".format(str(tc))] = finput
                break
            else:
                print("Not a file.")
                continue


    thread_dict = {}

    while True:
        try:
            threadnum = int(input("Enter the number of threads (one thread per file): "))
            if threadnum <= 0:
                print("Must be greater than 0.")
                continue
            else:
                print(f"Threads: {threadnum}")
                break
        except ValueError:
            print("Must be an integer.")
            continue

    for t in range(threadnum):
        resource_assignment(t)

    return thread_dict, threadnum

def frequency_analysis(filepath):
    def get_filename():
        filename = ''
        plain_filename = ''
        for char in filepath[::-1]:
            if char is "\\":
                break
            else:
                filename += char
        filename = filename[::-1]
        for schar in filename:
            if schar is ".":
                break
            else:
                plain_filename += schar
        return plain_filename

    def letter_analysis():
        letterfreq_dict = {}
        for letter in string.ascii_uppercase:
            letterfreq_dict.update({letter:0})
        with open(filepath) as readfile:
            for line in readfile:
                for character in line:
                    if character.isalnum() is False and character.isdigit() is False:
                        pass
                    else:
                        letterfreq_dict[character] += 1
        return letterfreq_dict

    def proccess_and_display():
        filename = get_filename()
        if displaymode is 'print':
            print(f"----------Frequency Analysis for {filename}----------\n\n")
            letterfreq_dict = letter_analysis()
            master_list.append(letterfreq_dict)
            print("Letter Frequency Analysis:")
            sorted_tuples = sorted(letterfreq_dict.items(), key=lambda x: x[1], reverse=True)
            for tup in sorted_tuples:
                print(f"{tup[0]} occurs {tup[1]} times.")
                print('\n')
        else:
            savename = f"{filename}_analysis.txt"
            print(f"Saving to: {savename}")
            with open(savename, 'w+') as file:
                letterfreq_dict = letter_analysis()
                master_list.append(letterfreq_dict)
                file.write("Letter Frequency Analysis:\n")
                sorted_tuples = sorted(letterfreq_dict.items(), key=lambda x: x[1], reverse=True)
                for tup in sorted_tuples:
                    file.write(f"{tup[0]} occurs {tup[1]} times.")
                    file.write('\n')

    proccess_and_display()

def post_analysis_calculations():
    averages_dict = {}
    percentages_dict = {}
    total = 0
    for k in master_list[0]:
        averages_dict[k] = sum(d[k] for d in master_list) / threadcount
    for i in master_list:
        for v in i.values():
            total += v
    for k in master_list[0]:
        percentages_dict[k] = (sum(d[k] for d in master_list) * 100 / total)

    if displaymode is 'print':
        for k,v in averages_dict.items():
            print(f"{k} has a {v} mean occurrence rate\n")
        for k,v in percentages_dict.items():
            print(f"{k} is {v}% of the provided text.")
    elif displaymode is 'save':
        with open("PostAnalysisCalculations.txt", 'w+') as file:
            for k, v in averages_dict.items():
                file.write(f"{k} has a {v} mean occurrence rate\n")
            print('\n\n')
            for k, v in percentages_dict.items():
                file.write(f"{k} is {v}% of the provided text.\n")
    else:
        print("Error: display mode not set")
if __name__ == '__main__':

    while True:
        display_choice = input("[s]ave results to file, or [p]rint them out on screen: ")
        if display_choice.lower() == 's':
            displaymode = 'save'
            break
        elif display_choice.lower() == 'p':
            displaymode = 'print'
            break
        else:
            print("invalid input.")
            continue

    threads, threadcount = file_input()
    master_list = []
    executor = ThreadPoolExecutor(max_workers=threadcount)

    for val in threads.values():
        executor.submit(frequency_analysis(val))

    post_analysis_calculations()
