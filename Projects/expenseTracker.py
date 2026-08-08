print("----------------- * Welcome to Expense Tracker * ----------------- ");
expense_record={}
print( expense_record)




def addExpense():
    date=input("date: ")
    category=input("category: ")
    amount=float(input("amount: "))
    description=input("description: ")
    expense_record={"date":date, "category":category, "amount":amount, "description":description}





def viewExpense():
    pass
def calculateExpense():
    pass


while True:
    print("1. Add Expense.");
    print("2. View Expenses.");
    print("3. Calculate total spending amount.");
    print("4. Exit.");

    choice=int(input("Enter your Choice: "));

    match choice:
        case 1: addExpense();
        case 2:viewExpense();
        case 3:calculateExpense();
        case 4: break;
        case _: print("Invalid input");


print( expense_record)



