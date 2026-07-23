# game:  snake water and gun 
import random

def game(comp,you):
    if comp==you:
        return None
    elif comp=='s':
        if you=='w':
            return False
        elif you=='g':
            return True
    elif comp=='w':
        if you=='s':
            return True
        elif you=='g':
            return False
    elif comp=='g':
        if you=='s':
            return False
        elif you=='w':
            return True


print("computer  turn: Snake(s) Wateer(w) Gun(g)?")
randNo=random.randint(1,3)
if randNo==1:
    comp='s'
elif randNo==2:
    comp='w'
elif randNo==3:
    comp='g'

you=input("your turn: Snake(s) Wateer(w) Gun(g): ")

if(you=='cheat'): # this is cheat code , when you enter cheat it will tell you what computer has choosed.
    print("computer choice is : ",comp)
    you=input("your turn: Snake(s) Water(w) Gun(g): ")

print(f"computer chose {comp}")
print(f"you chose {you}")

result=game(comp,you) 

if result==None:
    print("game has been tied! ")
elif result:
    print("you won! ")
else:
    print("computer won! ")