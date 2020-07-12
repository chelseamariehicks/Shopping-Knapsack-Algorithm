#############################################################################
# Author: Chelsea Marie Hicks
# OSU Email: hicksche@oregonstate.edu
# Course number/section: CS 325-401
# Assignment: Homework 3            Due Date: April 19, 2020 by 11:59 PM
#
# Description: Program reads inputs from a file named shopping.txt which
#       consists of test cases providing the following information:
#       -T(1<=T<=100) is test case number in first line of file
#       -N(1<=N<=100) is the number of items in the test case on line 2
#       -The next N lines contain integer value pairs for the price
#       and weight of the item; P(1<=P<=5000) and W(1<=W<=100)
#       -F(1<=F<=30) is the number of people in the family in the next line
#       which is followed by F lines containing the maximum weight M (1<=M<=200)
#       
#       With this information, select the items for each family member to
#       to carry to maximize the total price of all the items the family 
#       takes in the shopping spree, with each family member being able to
#       take at most one of each item, if allowed based on the weight they
#       can carry. The output for the program will be written to a file
#       results.txt that contains for each test case the maximum total price
#       of all goods the family can carry and the item numbers N that they
#       should select.
#############################################################################

#algorithm for determining the the items with the maximum benefit for each person
#makes use of pseudocode from lecture on 0-1 Knapsack 
def shoppingSpree(W, P, N, M, data_table):
    #create matrix, B for bag, for storing the values so we can keep checking it the 
    #maximum value is found including or excluding an item
    B = [[0 for x in range(M + 1)] for x in range(N+1)] 

    #for loop to cover all items, this code mostly comes from the 0-1 Knapsack lecture
    #and the Geeks for Geeks Knapsack page (https://www.geeksforgeeks.org/0-1-knapsack-problem-dp-10/)
    for i in range(N + 1):
        for j in range(M+1):
            if i == 0 or j == 0:
                B[i][j] = 0
            #use it
            elif W[i-1] <= j:
                B[i][j] = max(P[i-1] + B[i-1][j-W[i-1]], B[i-1][j])
            #don't use it
            else:
                B[i][j] = B[i-1][j]
    
    result = B[N][M]
    weight = M

    #insert the items carried by family members into the data_table
    for r in range(N, 0, -1):
        if result <= 0:
            break
        elif result > 0 and result == B[r-1][weight]:
            continue
        else:
            data_table.append(r)
            result -= P[r - 1]
            weight -= W[r - 1]
    return B[N][M]

def main():
    #open file with input data
    data_file = open("shopping.txt")
    
    #initialize variables equal to zero
    test_cases = 0
    items = 0
    family_members = 0
    max_weight = 0

    #set test_cases equal to first integer in input file
    test_cases = int(data_file.readline())

    #acquire data from input file for each test case
    for case in range(test_cases):
        prices = []
        weights = []

        #set items equal to the number of items specified in input file in the next line
        items = int(data_file.readline())

        #for loop to set the price and weight for each item in the list
        for item in range(items):
            item_values = data_file.readline().split(' ')
            prices.append(int(item_values[0]))
            weights.append(int(item_values[1]))
    
        #initialize current maximum price to 0
        current_max_price = 0

        #set the number of family members from input data
        family_members = int(data_file.readline())

        #create table for storing data of each family member
        data_storage = [[] for i in range(family_members)]

        #for loop to call shoppingSpree on each family member and update the current_max_price
        for person in range(family_members):
            max_weight = int(data_file.readline())
            current_max_price += shoppingSpree(weights, prices, items, max_weight, data_storage[person])

        #write results to file named results.txt
        with open("results.txt", "a") as results:
            results.write("Test case: " + str(case + 1) + "\n")
            results.write("Total price: " + str(current_max_price) + "\n")
            results.write("Items carried by family member: \n")
            for person in range(family_members):
                results.write(str(person + 1) + ": " ),
                for item in data_storage[person]:
                    results.write(str(item) + " ")
                results.write("\n")
            results.write("\n")

    data_file.close()
    results.close()

main()
            