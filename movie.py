import subprocess
import sys

try:
    # Try importing tabulate
    from tabulate import tabulate
except ImportError:
    # If not installed, prompt to install
    print("Installing 'tabulate'...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tabulate"])
    print("'tabulate' installed successfully. Please restart the program.")
    sys.exit()
header = ['\033[1mID\033[0m', '\033[1mNAME\033[0m', '\033[1mRATING\033[0m']

#import program applications
import sqlite3
from tabulate import tabulate
connection = sqlite3.connect("movie_program/movies.db")
cursor = connection.cursor()
header = ['ID', 'NAME', 'YEAR', 'RATING']

#Function to check if id is in database
def findID(id):
    data = [id]
    cursor.execute('SELECT movie_id FROM films WHERE movie_id =?',data)
    viewid = cursor.fetchall()
    if viewid:
        return True

#Function to check if rating is within 1 - 10
def checkrating(rating):
    if rating < 0 or rating > 10:
        return False
    else:
        return True

#function to display the database
def displaymenu():
    viewall = cursor.execute('SELECT * FROM "films"')
    rows = viewall.fetchall()
    formatted_rows = [(movie_id, movie_name, movie_year, f"{movie_rating}/10") for movie_id, movie_name, movie_year, movie_rating in rows]
    print(' \033[1mMOVIES:\033[0m')
    print(tabulate(formatted_rows, headers=header, tablefmt="simple_grid"))


while True:
    
    displaymenu()
    
    movie_menu = input('Enter \033[1m"A"\033[0m to add a new movie \nEnter \033[1m"D"\033[0m to delete a movie\nEnter \033[1m"U"\033[0m to update a movie\nEnter anything else to go back to main menu\n').lower().strip()


    if movie_menu == 'a':
        print('You chose ADD a movie.')
        enter_name = input('Enter film name\n')
        while True:
            try:
                enter_year = int(input('Enter release year\n'))
                
                break
            except ValueError:
                print('Invalid Input')
        
        while True:
            try:
                enter_rating = float(input('Enter rating of movie\n'))
                if not checkrating(enter_rating):
                    print('Please enter a value between 1 - 10')
                    continue
                break
            except ValueError:
                print('Invalid Input')

        
        
        data = [enter_name, enter_year, enter_rating]
        cursor.execute("INSERT INTO 'films' ('movie_name', 'movie_year', 'movie_rating') VALUES (?,?,?)",data)
        connection.commit()

    elif movie_menu == 'd':
        
        print('You chose DELETE')
        delete_menu = input('Enter \033[1m"A"\033[0m to single delete. \nEnter \033[1m"B"\033[0m to delete all\n')
        if delete_menu == 'A':
            while True:
                delete_id = input('Film ID to delete:\n')
                if findID(delete_id):
                    break
                else:
                    print("Couldn't find that ID")
                    
            data = [delete_id]
            cursor.execute('DELETE FROM films WHERE movie_id=?',data)
            connection.commit()
        if delete_menu == 'b':
            confirm_prompt = input('Are you sure you want to delete all movies? Y/N\n')

            if confirm_prompt == 'y':
                cursor.execute('DELETE FROM films')
                connection.commit()
            

            

    elif movie_menu == 'u':
        print('You chose UPDATE a movie.')
        while True:
            try:
                update_id = int(input('Enter a movie ID\n'))
                if findID(update_id):
                    break
                else:
                    print("Couldn't find that ID")
            except ValueError:
                print('Please enter a valid integar')
        
        
        
        update_name = input('Enter new name\n')
        while True:
            try:
                update_year = int(input('Enter release year\n'))
                
                break
            except ValueError:
                print('Invalid Input')
        
        while True:
            try:
                update_rating = float(input('Enter rating of movie\n'))
                if not checkrating(update_rating):
                    print('Please enter a value between 1 - 10')
                    continue
                break
            except ValueError:
                print('Invalid Input')

        
        data = [update_name, update_year, update_rating, update_id]
        cursor.execute('UPDATE films SET movie_name =?, movie_year =?, movie_rating =? WHERE movie_id =?',data)
    
    elif movie_menu == 'v':
        
        while True:
            displaymenu()

            main_function_menu = input('Enter \033[1m"A"\033[0m for sort movies by rating \nEnter \033[1m"B"\033[0m for sort movie by year\n').lower().strip()

            if main_function_menu == 'a':
                cursor.execute('SELECT * FROM films ORDER BY movie_rating ASC')
                list_by_rating = cursor.fetchall()
                formatted_rows = [(movie_id, movie_name, movie_year, f"{movie_rating}/10") for movie_id, movie_name, movie_year, movie_rating in list_by_rating]
                print(' \033[1mMOVIES:\033[0m')
                print(tabulate(formatted_rows, headers=header, tablefmt="simple_grid"))
                break    

    elif movie_menu == 'l':
        viewall = cursor.execute('SELECT * FROM "films"')
        viewall1 =  cursor.fetchall()
        print(' \033[1mMOVIES:\033[0m')
        print(tabulate(viewall1, headers=header, tablefmt="simple_grid"))
    else:
        break

    
