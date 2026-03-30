# print("Hi") 
# # result= "s" + 7
# # print(result)



# dict1 = {
#     "name":"S",
#     "age":27 
# }

# dict1["ID"]

# try: 
#     res=  10/0
# except ZeroDivisionError: 
#     print ("Error: division by zero")

# print("")
# a=10 
# b=0 
# res = a/b
# print(res)


# 1. Prompt for Input: Use the input() function to ask the user to enter a number.
# 2. Implement try-except: Place the code that converts the input to an integer inside a try block.
# 3. Handle ValueError: If a ValueError occurs during the conversion (i.e., the input is not a valid number), catch it with an except ValueError: block and print an informative error message.
# 4. Success Message: If the conversion is successful, print a message confirming the entered number.

# user_number = input("Please enter a number: ")

# try:
#     number = int(user_number) 
#     print(f"Success! You entered the number {number}.")
    
# except ValueError:
#     print("Error: That was not a valid number. Please try again.")