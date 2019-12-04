# from csv import reader

# with open("fighters.csv") as csv:
#     data = reader(csv)
#     next(data)
#     for x in data:
#         print(f"{x[1]} has {x[2]} cm dicks in average")

'''
add_user("Dwayne", "Johnson") # None
# CSV now has two data rows:

# First Name,Last Name
# Colt,Steele
# Dwayne,Johnson
'''
# from csv import writer

# def add_user(first,last):
#     with open("users.csv","a") as file:
#         csv_writer = writer(file)
#         csv_writer.writerow([first,last])


# add_user("Klim","Chugunkin")

'''
print_users() # None
# prints to the console:
# Colt Steele
'''

# from csv import reader

# def print_users():
#     with open("users.csv") as file:
#         data = file.readlines()
#     for line in data:
#         line = line.split(",")
#         print( f"{line[0]} {line[1]}" )

# print_users()


'''
find_user("Colt", "Steele") # 1
find_user("Alan", "Turing") # 3
find_user("Not", "Here") # 'Not Here not found.'
'''
from csv import reader

def find_user(first,last):
    with open("users.csv") as file:
        csv_reader = reader(file)
        index = 0
        for row in csv_reader:
            index += 1
            if row[0] == first and row[1] == last:
                return print(index)
            else:
                continue
            return print(f"{first} {last} not found")

find_user("Klim","Chugunkin")
find_user("Name","Surname")
find_user("Vasya","Pupkin")

