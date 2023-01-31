import mariadb
import dbcreds

conn = mariadb.connect(
                        user = dbcreds.user,
                        password = dbcreds.password,
                        host = dbcreds.host,
                        port = dbcreds.port,
                        database = dbcreds.database
)
cursor = conn.cursor()
def welcome():
    print("Welcome to the command line blog")
    while True:
        username = str(input("Please enter your username: "))
        password = str(input("Please enter your password: "))
        cursor.execute("CALL check_creds(?, ?)",[username, password])
        result = cursor.fetchall()
        rows = len(result)
        if rows == 0:
                print("Please enter a valid username and password")
        elif rows != 0: 
            print("Welcome! Your client id is: ", result)
            prompt()
            break

def prompt():
    print("Please make a selection:\
        \n1. Create a new post\
        \n2. Read all posts\
        \n3. Read your previous posts\
        \n4. Show all usernames\
        \n5. Search posts by username\
        \n6. Quit")
    while True:
        try:
            selection = int(input("Enter your selection: "))
        except ValueError:
            print("Please enter a number between 1 and 6")
        if selection == 1:
            new_post()
        
        elif selection == 2:
            all_posts()

        elif selection == 3:
            my_posts()

        elif selection == 4:
            all_users()

        elif selection == 5:
            search_post()

        elif selection == 6:
            print("Thanks for visiting! Goodbye!")
            break
        else:
            print("wth")

def new_post():
    client_id = input("Please enter your client id: ")
    #     # if client_id != result:
    #         # ("Invalid client id, please try again")
    title = input("Please select a title for your post: ")
    content = input("Please create the content of your post: ")
    cursor.execute("CALL new_post(?, ?, ?)", [title, content, client_id])
    conn.commit()
    print("Your post has been successfully added")

def all_posts():
    cursor.execute("CALL all_posts()")
    all = cursor.fetchall()
    print(all)

def my_posts():
    client_id = cursor.execute("CALL client_id()")
    cursor.execute("CALL my_posts(?)", [client_id])
    mine = cursor.fetchall()
    print(mine)

def all_users():
    cursor.execute("CALL all_users()")
    users = cursor.fetchall()
    print(users)
    print("Show all usernames")

def search_post():
    username = input("Please key in the username you wish to view: ")
    print(username)
    # cursor.execute("SELECT client.username, post.title, post.content FROM client JOIN post ON client.id = post.client_id", [username])
    cursor.execute("CALL select_posts(?)", [username])
    result = cursor.fetchall()
    print(result)
    

welcome()

