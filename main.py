from snake import play_snake

def main_menu():
    print("Welcome to the Game Hub!")
    print("1. Snake")
    print("2. Tic-Tac-Toe")
    print("3. Flappy Bird")
    print("4. Exit")

    return input("Enter the number of your choice: ")

while True:
    choice = main_menu()
    if choice == '1':
        play_snake()
    elif choice == '2':
        # play_tic_tac_toe()
        pass
    elif choice == '3':
        # play_flappy_bird()
        pass
    elif choice == '4':
        break
    else:
        print("Invalid choice, please try again.")