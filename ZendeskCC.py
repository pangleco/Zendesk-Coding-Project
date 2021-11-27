import requests
import unittest
from unittest import mock


# Get username and password, if error in login continue trying until correct : return users ticket json
def getUser():

    while True:

        domain = input("Please enter Zendesk domain (ex. if your domain is zccpangle.zendesk.com, input zccpangle): ")
        user = input("Please input your Zendesk email for login: ")
        password = input("Please input your Zendesk password: ")

        response = requests.get('https://'+domain+'.zendesk.com/api/v2/tickets', auth=(user, password))
        user = response.json()

        if "error" not in user.keys():
            break
        else:
            print("\nLogin error.")
            print("Error:",user["error"],'\n')

    return user

# creates a list of the tickets for the user : return list of tickets
def getTickets(user):

    # List of all tickets
    ls = []
    # formated by [ id, subject, status, dateCreated, assignee, requester, description]

    for ticket in user["tickets"]:

        # builds a list for each ticket with all info needed
        dateCreated = ticket["created_at"]
        id = ticket["id"]
        subject = ticket["subject"]
        status = ticket["status"]
        requester = ticket["requester_id"]
        assignee = ticket["assignee_id"]
        description = ticket["description"]
        lsTicket = [ id, subject, status, dateCreated, assignee, requester, description]
        ls.append(lsTicket)

    return ls

# Gets the option for the main menu of the ticket viewer : returns a string of the valid option
def menuOptions():



    while True:
        
        option = input("\nMenu options:\n* Type 1 to view all tickets\n* Type 2 to view a ticket\n* Type 'q' to quit\n").lower()
        
        if ((option == '1') or (option == '2' ) or (option == 'q')):
            return option
        else:
            print('\nInput "'+option+'" is not valid option.\n')
            continue

# Gets the option for the pages of tickets when viewing all tickets : returns a string of the valid option
def pageOptions():

    while True:

        option = input("\nChoose option (n = next page, p = previous page, q = quit): ").lower()
        print()

        if ((option == 'n') or (option == 'p' ) or (option == 'q')):
            return option
        else:
            print("Invalid option. ")

# Prints all tickets for viewing in a list, allows for paging (25 per page) : returns nothing
def showAllTickets(ticketList):

    i = 0
    numTickets = len(ticketList)
    while True:
        
        while i < numTickets:

            print("ID:"+str(ticketList[i][0])+' Subject "'+ticketList[i][1]+'" created by -',ticketList[i][5]," on ",ticketList[i][3])

            if ((i%25) == 24):
                i += 1
                break
            else:
                i += 1

        
        option = pageOptions()

        if option.lower() == 'q':
            break
        elif option.lower() == 'n':
            continue
        elif option.lower() == 'p':
            i = i - 50
            if i < 0:
                i = 0
            continue

# Finds ticket from id and prints ticket info if found in list of tickets : returns 1 if ticket is found 0 if not
def showTicket(ticketList,id):

    for ticket in ticketList:

        if ticket[0] == id:

            print("\nID:"+str(ticket[0])+' Subject "'+ticket[1]+'" created by -',ticket[5]," on ",ticket[3])
            print('\n'+ticket[6]+'\n')
            return 1

    return 0


# ****TESTING*****
class Testing(unittest.TestCase):

    # test that ticket can be found or not found when ticket does not exist
    def test_showTicket(self):

        ticketList = [[1, "help","open","12/21/1999","1231241","3356342","help me please"],[2, "printer dead","open","11/14/2020","1231241","3356342","help me please printer does not work"],[3, "word wont open","open","02/09/2001","1231241","3356342","help my word wont run"]]

        self.assertEqual(showTicket(ticketList,1),1,"Should be 1 since ticket can be found")

        self.assertEqual(showTicket(ticketList,101),0,"Should be 0 since ticket can not be found")



def main():

    user = getUser()
    ticketList = getTickets(user)

    # Welcome message for ticket viewer
    print("\n--Welcome to the Zendesk ticket viewer--\n")
    print("{:^40}".format("*Select a menu option to continue*\n"))

    # While loop for main menu usage
    while True:
        menuOption = menuOptions()
        if menuOption == '1':

            showAllTickets(ticketList)

        elif menuOption == '2':
        
            while True:

                id = int(input("Please enter ticket id to view:\n"))

                if showTicket(ticketList,id) == 0:
                    print("\nTicket not found, please try again.\n")
                else:
                    break

        elif menuOption == 'q':
            print("\nThank you for using the Zendesk ticket viewer!\n*Goodbye*")
            break

def testing():

    unittest.main()

#testing()
main()