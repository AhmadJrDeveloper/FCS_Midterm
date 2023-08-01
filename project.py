"""quit method reference:https://www.geeksforgeeks.org/python-exit-commands-quit-exit-sys-exit-and-os-_exit/
datetime importing https://stackoverflow.com/questions/15707532/import-datetime-v-s-from-datetime-import-datetime
calandar importing https://www.geeksforgeeks.org/python-calendar-module/
JSON Reading and writing https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
calendar.monthrange https://www.includehelp.com/python/calendar-monthrange-method-with-example.aspx
.strftime https://www.geeksforgeeks.org/python-strftime-function/


"""
import json
from datetime import datetime, timedelta
import calendar
data = []
#Appending the file to data list:
with open("content.txt", "r") as f:
    for line in f:
        try:
            myDict = json.loads(line.strip())  # Safely convert the line to a dictionary using json.loads()
            data.append(myDict)  # Append the dictionary to the data list
        except json.JSONDecodeError:
            print(f"Error: Unable to parse data in line: {line}")
        
#Creating function that save the data to my list
def save_new_data(fileName, data):
    with open(fileName, 'w') as file:
        for entry in data:
            json.dump(entry, file)
            file.write('\n')  
              



def date_checking(date):
    # checking the length of the date
    if len(date) != 8:
        return False, "Invalid date format. Please enter a valid date in the format YYYYMMDD."

    # Convert the date string to integers
    year = int(date[0:4])
    month = int(date[4:6])
    day = int(date[6:8])

    # checking the date input if its valid
    if not 1 <= month <= 12:
        return False, "Error: Invalid month. Please enter a valid month (1-12)."

    # Get the maximum number of days for the specified month and year
    maxDays = calendar.monthrange(year, month)[1]
    if not 1 <= day <= maxDays:
        return False, f"Error: Invalid day for this month. It should be 1-{maxDays}."

    # Get the current date and store it in a varibale
    currentDate = datetime.now()
    
    # Check if the input date is in the past or after the current date
    inputDate = datetime(year, month, day)
    if inputDate < currentDate:
        return False, "Error: You cannot enter a date in the past."

    return True, "Valid date!"



######################################################################################################################
#ADMIN FUNCTIONS:
#FUNCTION1
def display_statistics(data):
    if not data:
        print("Error: No data found.")
        return

    # counting the events and store them in a list
    eventTicketsCount = {}
    for ticket_info in data:
        event_id = ticket_info["eventId"]
        if event_id in eventTicketsCount:
            eventTicketsCount[event_id] += 1
        else:
            eventTicketsCount[event_id] = 1

    # finding the event with the most tickets
    maxTickets = -1
    eventMaxTicketes = None
    for event_id, ticket_count in eventTicketsCount.items():
        if ticket_count > maxTickets:
            maxTickets = ticket_count
            eventMaxTicketes = event_id

    #displaying result
    if eventMaxTicketes is not None:
        print(f"The event with the highest number of tickets is '{eventMaxTicketes}' with {maxTickets} tickets.")
    else:
        print("No tickets found.")
####################################################
def display_all_tickets(data):
        #get the current date
        currentDateStr = datetime.now().strftime("%Y%m%d")
        currentDate = datetime.strptime(currentDateStr, "%Y%m%d").date()

        # Step 3: Filter out old tickets (tickets with timeStamp before the current date)
        filteredData = [ticket for ticket in data if datetime.strptime(ticket['timeStamp'], "%Y%m%d").date() >= currentDate]

        # Step 4: Sort the remaining tickets based on the timeStamp
        sortedData = sorted(filteredData, key=lambda ticket: (datetime.strptime(ticket['timeStamp'], "%Y%m%d").date(), ticket['eventId']))

        # Step 5: Display the ordered events
        for ticket in sortedData:
            eventDateStr = ticket['timeStamp']
            eventDate = datetime.strptime(eventDateStr, "%Y%m%d").date()

            if eventDate == currentDate:
                eventDateFormatted = "Today"
            elif eventDate == currentDate + timedelta(days=1):
                eventDateFormatted = "Tomorrow"
            else:
                eventDateFormatted = eventDate.strftime("%Y-%m-%d")

            print(f"{eventDateFormatted}: Event ID - {ticket['eventId']}")
    
        ##################################################################
def change_ticket_prority(data, ticketId, newPriority):
     foundTicket = False
     for ticket in data:
        if ticket["ticketId"] == ticketId:
            ticket["priority"] = newPriority
            foundTicket = True
            break

     if foundTicket:
        print(f"Priority of ticket {ticketId} has been updated to {newPriority}.")
     else:
        print(f"Ticket with ID {ticketId} not found. Priority not changed.")

 ###################################################################
def disable_ticket(data,ticketId):
    foundTicket = False
    for ticket in data:
        if ticket["ticketId"] == ticketId:
            data.remove(ticket)
            foundTicket = True
            break
    if foundTicket:
        print(f"The ticket {ticketId} has been deleted!")
    else:
        print(f"The ticket {ticketId} does not exist!")
##############################################################################
def todays_events(data):
        #getting the current date and store it in a variables
        currentDateStr = datetime.now().strftime("%Y%m%d")
        currentDate = datetime.strptime(currentDateStr, "%Y%m%d").date()

        #filter out today's events (tickets with timeStamp equal to the current date)

        todayEvents = [ticket for ticket in data if datetime.strptime(ticket['timeStamp'], "%Y%m%d").date() == currentDate]

        #sort today's events based on priority
        sortedTodayEvents = sorted(todayEvents, key=lambda ticket: ticket['priority'])

        #display events
        for ticket in sortedTodayEvents:
            eventDateStr = ticket['timeStamp']
            eventDate = datetime.strptime(eventDateStr, "%Y%m%d").date()

            print(f"Today ({eventDate}): Event ID - {ticket['eventId']}, Priority - {ticket['priority']}")

        # Removing today's events from the list
        data[:] = [ticket for ticket in data if datetime.strptime(ticket['timeStamp'], "%Y%m%d").date() != currentDate]

    
####################################################################################################
#User Function:
def book_ticket(data, eventId, userName, timeStamp, priority=0):
    # searching for the maximum ticket id to increment determine the id for the new ticket
    maxTicketId = max(int(entry["ticketId"][4:]) for entry in data)

    #generating a new ticket id
    newTicketId = f"tick{maxTicketId + 1:03}"

    # creating the new ticket with all data provided from the user
    new_ticket = {
        "ticketId": newTicketId,
        "eventId": eventId,
        "userName": userName,
        "timeStamp": timeStamp,
        "priority": priority
    }

    # add the new ticker for the list
    data.append(new_ticket)





######################################################################################################################    
#Users login:
adminAttempts = 5 #creating a counter and decrement it 1 each time the admin enters a wrong password
user=(input("Enter Username:"))
password = (input("Enter Password:"))
if (user.lower() == "admin"):#admin login
    while(password != "admin123123"):
        if(adminAttempts != 1):
            password = (input("Enter correct Password:"))
            adminAttempts -= 1
        else:    
            print("Session Terminated!")
            quit()
    print("Hello Admin!")#Greeting the admin
    while True:#let the admin to choose the action
        print("-"*25)
        print("1. Display Statistics")
        print("2. Book a Ticket")
        print("3. Display all Tickets")
        print("4. Change Ticket's Priority ")
        print("5. Disable Ticket")
        print("6. Run Events")
        print("7. EXIT")
        print("-"*25)
        choice = (input("Enter a choice: "))
        if (choice == "1"):
            display_statistics(data)
        elif (choice == "2"):
             eventId = input("Enter the event ID: ")
             userName = input("Enter the username: ")
             while True:
                timeStamp = input("Enter the date as follow YYYYMMDD: ")
                is_valid, message = date_checking(timeStamp)
                if not is_valid:
                    print(message)
                else:
                    break    

               
             priority = int(input("Enter the priority (default is 0): "))
             book_ticket(data, eventId, userName, timeStamp, priority)
        elif(choice == "3"):
            display_all_tickets(data)
        elif(choice == "4"):
            ticketIdToChange = input("Enter the ticket ID you want to change the priority for: ")
            newPriorityValue = int(input("Enter the new priority value: "))
            change_ticket_prority(data, ticketIdToChange, newPriorityValue)
        elif(choice =="5"):
             deletedTicket = input("Enter the ticket ID you want to delete: ")
             disable_ticket(data,deletedTicket)
        elif(choice =="6"):
            todays_events(data)
        elif(choice == "7"):
            save = input("Do you want to save changes? enter y or n: ")
            while True:
                if save.lower() == "y":
                    save_new_data("content.txt", data)
                    print("Data has been saved.")
                    quit()
                elif save.lower() == "n":
                    print("Data has not been saved.")
                    quit()
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
        else:
            print("Please enter a number between 1 and 7")    
else:#user login
    print("Hello",user,)#Greeting the admin

    while(password != " "):
          password = (input("As a user you should enter an empty password enter 1 space only:"))
         
    while True:
         print("-"*25)
         print("1. Book a Ticket")
         print("2. Exit")
         print("-"*25)
         choice = (input("Enter a choice: "))
         if choice == "1":
             eventId = input("Enter the event ID: ")
             while True:
                timeStamp = input("Enter the date as follow YYYYMMDD: ")
                is_valid, message = date_checking(timeStamp)
                if not is_valid:
                    print(message)
                else:
                    break 
             priority = int(input("Enter the priority (default is 0): "))
             book_ticket(data, eventId, user, timeStamp, priority)
             print("Booked Done")
         elif choice == "2":    
            
             save_new_data("content.txt", data)
             print("GoodBye",user)
             quit()
         else:
              print("Please enter 1 or 2")    

                 



            




        



    

    