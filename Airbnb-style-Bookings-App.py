#
#
# For testing SQL Server connection in CSIL through pyodbc connection (using SQL Server standard login)
#
# Author: Johnny Zhang
#
# You should run this program on a CSIL system. (verified with Python 3.6.2 64bit)
#
# Last modified @ 2018.03.27
#
#
# Please modify this program before using.
#
# alternation includes: 
#
#       the standard SQL Server login (which is formatted as s_<username>)
#       the password for CSIL SQL Server standard login
#

import pyodbc

connection = pyodbc.connect('driver={SQL Server};server=cypress.csil.sfu.ca;uid=s_fwarraic;pwd=YP63J2b3TFt6m6M3')
#  ^^^ 2 values must be change for your own program.

#  Since the CSIL SQL Server has configured a default database for each user, there is no need to specify it (<username>354)

cursor = connection.cursor()

# to validate the connection, there is no need to change the following line
# cur.execute('SELECT username from dbo.helpdesk')
# row = cur.fetchone()
# while row:
#     print ('SQL Server standard login name = ' + row[0])
#     row = cur.fetchone()
# print("Connection Successfully Established") 
# connection.close()

#  This program will output your CSIL SQL Server standard login,
#  If you see the output as s_<yourusername>, it means the connection is a success.
#  
#  You can now start working on your assignment.
#

# functions
# search listings functions
def search_listing():
    print("------------------------------------------------")
    print("")
    print("Welcome to Search Listing")
    print("")

def display_search_listing(minPrice, maxPrice, numBedrooms, startDate, endDate):
    print("Minimum Price:  ", minPrice)
    print("Maximum Price:  ", maxPrice)
    print("Number of Bedrooms:  ", numBedrooms)
    print("Start Date:  ", startDate)
    print("End Date:  ", endDate)

    print("")

    #SQL Query  
    # SQLCommand = ("SELECT * FROM Listings AS L JOIN Calendar AS C ON L.id = C.listing_id WHERE(C.price >= ? AND C.price <= ? AND L.number_of_bedrooms = ? AND C.date >= ? AND C.date <= ?)")
    # Values = [minPrice, maxPrice, numBedrooms, startDate, endDate]
    SQLCommand = ("SELECT DISTINCT id,name,number_of_bedrooms,LEFT(description,25),MAX(price) FROM Listings,Calendar WHERE number_of_bedrooms = ? AND id=listing_id AND (date >= ? AND date <= ? )AND  id NOT IN  (SELECT listing_id FROM Calendar WHERE (date >= ? AND date <= ?) AND (price > ? OR price < ? OR available = 0)) GROUP BY id,name,LEFT(description,25),number_of_bedrooms")
    Values = [numBedrooms, startDate, endDate, startDate, endDate, maxPrice, minPrice]  
    #Processing Query  
    cursor.execute(SQLCommand, Values)  

    results = cursor.fetchone()

    i = 0   
    while results:
        i = i + 1
        print("----------------------Listing %d------------------"%i)
        print("")
        print ("id: " +  str(results[0]))  
        print ("Name: " +  str(results[1]))  
        print ("Descripttion: " +  str(results[3]))  
        print ("Number of bedrooms: " +  str(results[2]))
        print ("price: " +  str(results[4]))
        print()  
        results = cursor.fetchone() 
    if i == 0:
        print("Search Results not found please try again")
        print()

        
  
    #connection.close()

# book listing

# wrire review functions
def display_bookings(name):
    print(name)

    print("")

    #SQL Query  
    SQLCommand = ("SELECT * FROM Bookings B WHERE B.guest_name = ?")
    Values = [name] 
    #Processing Query  
    cursor.execute(SQLCommand, Values)  

    results = cursor.fetchone()

    i = 0   
    while results:
        i = i + 1
        print("----------------------Bookings %d------------------"%i)
        print("")
        print ("id: " +  str(results[0]))  
        print ("listing_id: " +  str(results[1]))  
        print ("guest_name: " +  str(results[2]))  
        print ("stay_from: " +  str(results[3]))
        print ("stay_to: " +  str(results[4]))
        print ("number_of_guests: " +  str(results[5]))
        print()  
        results = cursor.fetchone() 
    if i == 0:
        print("Search Results not found please try again")
        print()

        
  
    #connection.close()

# main program
while True:
    pass    

    print("") 
    print("--------------- Welcome to the Main Menu -----------------") 
    print("")

    print("To Search a listing press 's' and then enter")
    print("To Write a Review press 'r' and then enter")
    print("To Quit press 'q' and then enter")    

    print("")
    letter = input("Enter 's', or 'r' else enter 'q' to quit: ")
    print(letter)
    print("")

    # search listing
    if letter == 's':

        search_listing()
        print("")

        print("Please Enter the Criteria of search below: ")
        minPrice = input("Enter Minimum Price: (e.g. 90): ")
        maxPrice = input("Enter Maximum Price: (e.g. 100): ")
        numBedrooms = input("Enter Number of Bedrooms: (e.g. 2): ")
        startDate = input("Enter Start Date: (e.g. 2016-01-05): ")
        endDate = input("Enter End Date: (e.g. 2017-01-01): ")
        print("")
        display_search_listing(minPrice, maxPrice, numBedrooms, startDate, endDate)

        print("")
        print("------------------ Bookings --------------------")
        print("")
        print("To book a listing press 'b' and then enter else press m and then enter to go back to main menu")

        print("")
        letter = input("Enter 'b' else enter 'm' to go to main menu: ")
        print(letter)
        print("")

        # book listing
        if letter == 'b':
            print("Booking in progress")
            # get listing from search listing

            print("")

            print("Please Enter the id of Listings: ")
            idnum = input("Enter the id: (e.g. 10310373): ")
            
            SQLCommand = ('SELECT DISTINCT id,name,number_of_bedrooms,LEFT(description,25),MAX(price) FROM Listings,Calendar WHERE number_of_bedrooms = ? AND id=? AND (date >= ? AND date <= ? )AND  id NOT IN  (SELECT listing_id FROM Calendar WHERE (date >= ? AND date <= ?) AND (price > ? OR price < ? OR available = 0)) GROUP BY id,name,LEFT(description,25),number_of_bedrooms')
            Values = [numBedrooms, idnum, startDate, endDate, endDate, startDate, maxPrice, minPrice] 

            cursor.execute(SQLCommand, Values)  

            results = cursor.fetchone()

            print("")
            print("Displaying Selected List")
            print("")

            i = 0   
            while results:
                i = i + 1
                print("----------------------Listing %d------------------"%i)
                print("")
                print ("id: " +  str(results[0]))  
                print ("Name: " +  str(results[1]))  
                print ("Descripttion: " +  str(results[3]))  
                print ("Number of bedrooms: " +  str(results[2]))
                print ("price: " +  str(results[4]))
                print()  
                results = cursor.fetchone() 
            if i == 0:
                print("Search Results not found because incorrect id input please try again")
                print()
                break

            print("Booking Selected Listing")
            print("")
            print("Please Enter the Relevant information to book the selected listing")

            #############Database Parameters##########
            initid = input("Enter the initial id : (e.g. 13): ") 
            idnum = input("Enter the listing_id which is = id: (e.g. 10310373): ")
            guest_name = input("Please Enter Name: (e.g. Fazal): ")  
            stay_from = input("Please Enter Date of Stay from (e.g. 2016-07-23) : ")  
            stay_to = input("Please Enter Date of Stay to (e.g. 2016-10-23) : ")  
            number_of_guests = input("Please Enter the number of guests (e.g. 3) : ")  
            ##########################################  
    
            #SQL Query  
            SQLCommand = ("INSERT INTO Bookings(id, listing_id, guest_name, stay_from, stay_to, number_of_guests) VALUES (?,?,?,?,?,?)")  
            Values = [initid ,idnum, guest_name, stay_from, stay_to, number_of_guests] 

            #Processing Query  
            cursor.execute(SQLCommand,Values)   
            #Commiting any pending transaction to the database.  
            connection.commit() 

            #connection.close()

            print("")
            print("Booked Listing successful!")
            print("")



        elif letter == 'm':
            print("main menu in progress")
            # connection.close()
            # break

        

    # write review
    elif letter == 'r':
        print("") 
        print("--------------- Writing a Review -----------------") 
        print("")
        print("Please Enter your name below to access all previous bookings: ")
        name = input("Enter Your name: (e.g. Fazal): ")
        print("")
        display_bookings(name)
        print("")

        print("")
        print("--------------- Writing a Review -----------------") 
        print("")
        print("Please Enter the Relevant Information to write a review")
        print("")
        
        #############Database Parameters##########
        initId = input("Enter the initial id : (e.g. 13): ")
        idListings = input("Enter the listing_id which is = id: (e.g. 10310373): ")
        endDate = input("Please Enter stay_to Date from Bookings: (e.g. 2016-01-01): ")
        userName = input("Enter Your name: (e.g. Fazal): ") 
        currentDate = input("Please Enter todays Date: (e.g. 2019-11-29): ")
        reviewText = input("Please Write your review: (e.g. I rate this place 5 stars): ")  
        ##########################################  

        if currentDate < endDate:
            print("")
            print("not possible since current date is less than the stay_to date")
            print("Please try again.")
            print("")
            break

        
        #SQL Query  
        SQLCommand = ("INSERT INTO Reviews(id, listing_id, comments) VALUES (?,?,?)")  
        Values = [initId ,idListings, reviewText] 

        #Processing Query  
        cursor.execute(SQLCommand,Values)   
        #Commiting any pending transaction to the database.  
        connection.commit() 

        #connection.close()

        print("")
        print("Written a Review successful!")
        print("")

    # exit
    elif letter == 'q':
        print("Exited Application Successful")
        connection.close()
        break
    else:
        print("fail")

    #search listing function

