import subprocess
import sys

# Try importing tabulate, if not installed, install it using pip
try:
    from tabulate import tabulate
except ImportError:
    print("Installing 'tabulate'...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tabulate"])
    print("'tabulate' installed successfully. Please restart the program.")
    sys.exit()

# Define table header for displaying movie data
header = ['ID', 'NAME', 'YEAR', 'RATING']

# Import SQLite3 and establish a database connection
import sqlite3
from tabulate import tabulate
connection = sqlite3.connect("movie_program/movies.db")
cursor = connection.cursor()

# Function to check if a movie ID exists in the database
def findID(id):
    data = [id]
    cursor.execute('SELECT movie_id FROM films WHERE movie_id =?', data)
    viewid = cursor.fetchall()
    if viewid:
        return True

# Function to validate that the rating is between 1 and 10
def checkrating(rating):
    if rating < 0 or rating > 10:
        return False
    else:
        return True

# Function to display all movies in the database using tabulate
def displaymenu():
    viewall = cursor.execute('SELECT * FROM "films"')
    rows = viewall.fetchall()
    formatted_rows = [(movie_id, movie_name, movie_year, f"{movie_rating}/10") for movie_id, movie_name, movie_year, movie_rating in rows]
    print(' \033[1mMOVIES:\033[0m')
    print(tabulate(formatted_rows, headers=header, tablefmt="simple_grid"))

# Main program loop
while True:
    
    # Prompt user for menu action
    movie_menu = input('Enter \033[1m"A"\033[0m to add a new movie \nEnter \033[1m"D"\033[0m to delete a movie\nEnter \033[1m"U"\033[0m to update a movie\nEnter \033[1m"L"\033[0m to list all movies\nEnter anything else to go back to main menu\n').lower().strip()

    # Add a new movie
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

        # Insert new movie into the database
        data = [enter_name, enter_year, enter_rating]
        cursor.execute("INSERT INTO 'films' ('movie_name', 'movie_year', 'movie_rating') VALUES (?,?,?)", data)
        connection.commit()

    # Delete a movie or all movies
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
            cursor.execute('DELETE FROM films WHERE movie_id=?', data)
            connection.commit()
        
        if delete_menu == 'b':
            confirm_prompt = input('Are you sure you want to delete all movies? Y/N\n')
            if confirm_prompt == 'y':
                cursor.execute('DELETE FROM films')
                connection.commit()

    # Update an existing movie
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

        # Get new movie data
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

        # Update movie in the database
        data = [update_name, update_year, update_rating, update_id]
        cursor.execute('UPDATE films SET movie_name =?, movie_year =?, movie_rating =? WHERE movie_id =?', data)

    # View sorted movies
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

    # List all movies again 
    elif movie_menu == 'l':
        print('\nYou chose to VIEW movies.')

        # Ask user for sorting field
        while True:
            sort_field = input('Sort movies by: \033[1mA\033[0m - ID, \033[1mB\033[0m - Rating, \033[1mC\033[0m - Year\n').lower().strip()


            if sort_field == 'a':
                sort_column = 'movie_id'
                break
            elif sort_field == 'b':
                sort_column = 'movie_rating'
                break
            elif sort_field == 'c':
                sort_column = 'movie_year'
                break
            else:
                print('Invalid input. Please choose A, B, or C.')

        # Ask user for sort order
        while True:
            sort_order = input('Choose sort order: \033[1mA\033[0m - Ascending, \033[1mB\033[0m - Descending\n').lower().strip()

            if sort_order == 'a':
                order = 'ASC'
                break
            elif sort_order == 'b':
                order = 'DESC'
                break
            else:
                print('Invalid input. Please choose A or B.')

        # Fetch and display sorted results
        query = f'SELECT * FROM films ORDER BY {sort_column} {order}'
        cursor.execute(query)
        sorted_movies = cursor.fetchall()
        formatted_rows = [(movie_id, movie_name, movie_year, f"{movie_rating}/10") for movie_id, movie_name, movie_year, movie_rating in sorted_movies]
        
        print('\n\033[1mSORTED MOVIES:\033[0m')
        print(tabulate(formatted_rows, headers=header, tablefmt="simple_grid"))


    # Exit the loop and return to main menu
    else:
        break
