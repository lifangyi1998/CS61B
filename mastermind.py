import turtle
import sys
from Marble import Marble
from Point import Point
import random 
import time
import traceback
import datetime


screen = turtle.Screen()
screen.title('Master Mind')
global count_choose
count_choose = 0
global selected_color_list
selected_color_list = []
global number_guess_circle
number_guess_circle = []
global round_count
round_count = 0
global colors
colors = ['blue', 'red', 'green', 'yellow', 'purple', 'black']
global right_answer
right_answer = random.sample(colors, 4)
global check_answer
check_answer = [] # only store 0/1
global peglist
peglist = []
global check_button_pressed
check_button_pressed = False
global best_score
best_score = None
global best_name
best_name = None
global list_of_info
list_of_info = []
global user_name
user_name = None

print('right_answer',right_answer)

def log_error(err):
    with open("mastermind_errors.err", "a") as file:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_type = type(err).__name__
        error_traceback = traceback.format_exc()
        file.write(f"{current_time} - {error_type}: {error_traceback}\n\n")


def load_leaderboard_gif():
    try:
        screen.addshape('leaderboard_error.gif')
        leaderboard_error_turtle = turtle.Turtle('leaderboard_error.gif')

        # go to position
        leaderboard_error_turtle.penup()
        leaderboard_error_turtle.goto(0,0)

        # disappear after 3 sec
        screen.ontimer(leaderboard_error_turtle.clear(),3000)
    except Exception as e:
        log_error(e)
    

def load_file_error_gif():
    try:
        screen.addshape('file_error.gif')
        file_error_turtle = turtle.Turtle('file_error.gif')

        # go to position
        file_error_turtle.penup()
        file_error_turtle.goto(0,0)

        # display warning 4 sec
        time.sleep(4)

        # after 4 sec, disappear
        file_error_turtle.hideturtle()
        file_error_turtle.clear()
    except Exception as e:
        log_error(er)

def load_winner_gif():
    try:
        screen.addshape('winner.gif')
        winner_turtle = turtle.Turtle('winner.gif')

        # go to position
        winner_turtle.penup()
        winner_turtle.goto(0,0)

        # display warning 4 sec
        time.sleep(4)

        # after 4 sec, disappear
        winner_turtle.hideturtle()
        winner_turtle.clear()
    except Exception as e:
        log_error(e)
        load_file_error_gif()
        

def load_lose_gif():
    try:
        screen.addshape('Lose.gif')
        Lose_turtle = turtle.Turtle('Lose.gif')

        # go to position
        Lose_turtle.penup()
        Lose_turtle.goto(0,0)

        # display warning 4 sec
        time.sleep(3)

        # after 4 sec, disappear
        Lose_turtle.hideturtle()
        Lose_turtle.clear()
    except FileNotFoundError as e:
        log_error(e)
        load_file_error_gif()
        

def draw_rectangle(length, width, color, start_x, start_y):
    
    '''
    draw_rectangle function starting from up left corner
    and drawing clockwise

    parameters:
    length: int or float
        length of the rectangle
    width: int or float
        width of the rectangle
    color: str
        color of the rectangle's border
    start_x: int or float
        X coordinate for the starting position of the rectangle
    start_y: int or float
        Y coordinate for the starting position of the rectangle
    '''
    # set pen size
    turtle.pensize(7)
    # go to the starting point
    turtle.up()
    turtle.goto(start_x, start_y)
    # set the direction to east
    turtle.setheading(0)
    # put down pen
    turtle.down()
    # set color
    turtle.pencolor(color)
    # set speed
    turtle.speed(10)

    # draw rectangle
    turtle.forward(length)
    turtle.right(90)
    turtle.forward(width)
    turtle.right(90)
    turtle.forward(length)
    turtle.right(90)
    turtle.forward(width)
    turtle.right(90)

# function that draw the board
def draw_board():
    '''
    this function will draw three rectangles
    by calling draw_rectangle function.
    '''
    # rectangle on the left
    draw_rectangle(400, 550, 'black', -350, 350)
    # rectangle on the right
    draw_rectangle(250, 550, 'blue', 150, 350)
    # rectangle on the bottom
    draw_rectangle(750, 150, 'black', -350, -240)

def start_file():
    global list_of_info
    print('startfile')
    '''
    start_file function use except/try to realize:
    if BestScore.txt exist, readlines() to get list of info
    and it's format like ['Score Name', 'Score Name']
    if not, create BestScore.txt
    '''
    try:
        with open('BestScore.txt', 'r') as file:
            list_of_info = file.readlines()
            # file.close()
            print(f'after_start_file, {list_of_info}')
        return list_of_info
    except FileNotFoundError as e:
        log_error(e)
        list_of_info = []
        with open('BestScore.txt', 'a') as file:
            pass
        return list_of_info
        
# function load best score
def load_best_score():
    '''
    Displays the best scores on the game board. The function identifies the lowest 
    scores from the provided list, considering them as the best scores, and displays them.

    Parameters:
    - list_of_info (list of str): A list containing score information in the format ['Score Name', ...].
      The list can have a maximum of two elements and can also be empty.

    Functionality:
    - If 'list_of_info' is empty, the function displays a message indicating no data available.
    - Otherwise, it extracts the scores and names, finds the minimum score(s), and displays them.
    - The display includes the top one or two best scores, depending on the list length.
    '''
    global list_of_info
    try:
        # Create a turtle object for displaying the score.
        load_score_turtle = turtle.Turtle()
        # If no scores are available, display 'Leaders'
        if len(list_of_info) == 0:
            load_score_turtle.up()
            load_score_turtle.goto(160, 300)
            load_score_turtle.down()
            load_score_turtle.write('Leaders:\n', align='left', font=('Arial', 20, 'normal'))
        else:
            # Create a dictionary to store scores and corresponding names.
            score_name_dict = {}
            for item in list_of_info:
                name, score = item.strip().split()
                score_name_dict[int(score)] = name
        
            # Find and display the lowest score (best score).
            min_score = min(score_name_dict)
            min_name = score_name_dict[min_score]
            turtle.up()
            turtle.goto(160, 300)
            turtle.down()
            turtle.write(f'Leaders: \n{min_score} : {min_name} ', align='left', font=('Arial', 20, 'normal'))
            # Remove the best score and check if there is a second best score.
            del score_name_dict[min_score]
            if len(score_name_dict) != 0:
                second_min_score = min(score_name_dict)
                second_min_name = score_name_dict[second_min_score]
                turtle.up()
                turtle.goto(160, 270)
                turtle.down()
                turtle.write(f'\n{second_min_score} : {second_min_name} ', align='left', font=('Arial', 20, 'normal'))
    except Exception as e:
        log_error(e)
        load_leaderboard_gif()
        
def load_quitmsg(callback):
    try:
 
        screen.addshape('quitmsg.gif')
        quitmsg_turtle = turtle.Turtle('quitmsg.gif')

        # go to position
        quitmsg_turtle.penup()
        quitmsg_turtle.goto(0,0)

        # show 3 sec
        
        screen.ontimer(callback, 3000)

        # after 3 sec, disappear
        screen.ontimer(quitmsg_turtle.hideturtle, 3000)
        screen.ontimer(quitmsg_turtle.clear, 3000)
        
    except FileNotFoundError as e:
        log_error(e)
        load_file_error_gif()
    
    
def exit_on_click(x, y):
    try:
        if (159 < x < 346) and (-366 < y < -268):
            print('click on quit')

            # load quit msg
            try:
                load_quitmsg(screen.bye)
            except Exception as e:
                log_error(e)
                pass
            
    except Exception as e:
        log_error(e)
        pass  # ignore exceptions

 
def quit_button():
    try:
        # register quit.gif
        screen.addshape('quit.gif')

        # create a turtle to represent quit.gif
        quit_turtle = turtle.Turtle('quit.gif')

        # go to position
        quit_turtle.penup()  
        quit_turtle.goto(250, -320)

        return quit_turtle
    except Exception as e:
        log_error(e)

# define function that draw guess buttons
def draw_guess_button():
    '''
    draw_guess_button will draw six marbles
    return list of marbles

    '''
    try:
        global colors
        global list_of_guess_marbles
        # set initial coordinate for he first guess button
        x = -304
        y = -323
        # set space between each guess button
        space_between_circles = 40
        # a list storing coordinates of each circle
        list_of_guess_marbles = []
        # loop to draw six different colors guess buttons
        for each_color in colors:
            marble = Marble(Point(x, y), each_color)
            marble.draw_empty()
            marble.draw()
            # store in the list
            list_of_guess_marbles.append(marble)
            # move turtles to next after drawing one button
            x += space_between_circles

        def in_marble_click(x, y):
            
            '''
            in_marble_click will check if click is within a marble
            if yes, it will change clicked marble into white
            and record the color
            parameters:
            x: float
                x of clicks
            y: float
                y of clicks
            marble: an instance of Marble class

            return the color of clicked marble
            '''
            global number_guess_circle
            global count_choose
            global selected_color_list
            global round_count
            
            print('round_count:', round_count, '\n count_choose:', count_choose)
            if count_choose < 4:
                for marble in list_of_guess_marbles:
                    if marble.clicked_in_region(x, y):
                        print('yes, click is in region')
                        if not marble.get_color() == 'white':
                            color_selected = marble.get_color()
                            print(color_selected)
                            marble.set_color('white')
                            marble.draw()
                            selected_color_list.append(color_selected)
                            # here I want to call the marble instance in the number_guess_circle list, index [round_count][count_choose]
                            number_guess_circle[round_count][count_choose]#.set_color(color_selected)
                            marb = number_guess_circle[round_count][count_choose]
                            marb.set_color(color_selected)
                            marb.draw()
                            count_choose += 1
                        
            print(f'selected_color_list, {selected_color_list}')
            return selected_color_list

            
                
        screen.onclick(in_marble_click)

        return list_of_guess_marbles
    except turtle.Terminator as e:
        log_error(e)
        sys.exit()


# function that draw ten guesses circles
def draw_guesses_circles():
    global number_guess_circle
    # define the size of circle
    MARBLE_RADIUS = 15
    # set coordinates for the first guess circle
    x_original = -304
    x = x_original
    y_original = 280
    y = y_original
    # set total rows and columns
    rows = 10
    columns = 4
    # set space between each circle
    space_x = 40
    space_y = 50

    # nested loop to draw guesses circles
    for row in range(rows):
        cirlce_in_a_row = []
        for column in range(columns):
            marble = Marble(Point(x, y), 'white')
            marble.draw_empty()
            cirlce_in_a_row.append(marble)
            x += space_x
        number_guess_circle.append(cirlce_in_a_row)
        # set x to original to draw next row of circles
        x = x_original
        # move y to next line to draw next row of circles
        y -= space_y
    return number_guess_circle 




# function that draw pegs
def draw_pegs():
    # set the r of circle
    r = 3
    # set total columns and rows
    rows_inside = 2
    columns_inside = 2

    rows_outside = 10

    # set coordinates for the first circle
    x_original = -10
    y_original = 295
    x = x_original
    y = y_original 

    # set space between each circle
    space_inside_x = 8
    space_inside_y = 8
    space_outside_y = 33.5

    for i in range(rows_outside):
        circle_in_a_set = []
        for j in range(rows_inside):
            circle_in_a_row = []
            for h in range(columns_inside):
                marble = Marble(Point(x, y), 'white', size = r)
                circle_in_a_row.append(marble)
                marble.draw_empty()
                x += space_inside_x
            circle_in_a_set.extend(circle_in_a_row)
            y -= space_inside_y
            x = x_original
        peglist.append(circle_in_a_set)
        x = x_original
        y -= space_outside_y
    
    

def coordinate(x,y):
    print(x,y)
    return x, y
    

# function load check button
def load_check_button():
    # register checkbutton.gif
    screen.addshape('checkbutton.gif')

    # create a turtle to represent checkbutton.gif
    check_turtle = turtle.Turtle('checkbutton.gif')

    # go to position
    check_turtle.penup()  
    check_turtle.goto(5, -320)
    
    return check_turtle

# function load x button
def load_x_button():
    # register xbutton.gif
    screen.addshape('xbutton.gif')

    # create a turtle to represent checkbutton.gif
    x_turtle = turtle.Turtle('xbutton.gif')

    # go to position
    x_turtle.penup()  
    x_turtle.goto(90, -320)
    
    return x_turtle

# fuction change color of pegs

# function for check button
def check_if_correct():# 
    '''
    Compares the selected colors with the correct answer and generates feedback for each selection.
    The feedback is represented as a list of colors: 'black', 'red', and 'white', where
    - 'black' indicates a correct color in the correct position,
    - 'red' indicates a correct color in the wrong position,
    - 'white' indicates an incorrect color.

    Returns:
    - A list of strings ('black', 'red', 'white') representing feedback for each selected color.

    Global Variables:
    - right_answer (list of str): The list containing the correct sequence of colors.
    - selected_color_list (list of str): The list containing the player's selection of colors.
    - check_answer (list of str): The list used to store the feedback for each color in the selection.
    '''
    global right_answer
    global selected_color_list
    global check_answer

    try:
        # Check if four colors are selected.
        if len(selected_color_list) == 4:
            # iterate every element in selected_color_list
            for index,color in enumerate(selected_color_list):
                if color in right_answer:
                    if right_answer[index] == color:
                        # Correct color in the correct position.
                        check_answer.append('black')
                    else:
                        # Correct color but in the wrong position.
                        check_answer.append('red')
                else:
                    # Incorrect color.
                    check_answer.append('white')
            random.shuffle(check_answer)
            return check_answer
        else:
            # If not exactly four colors are selected, return an empty list.
            check_answer = []
            return check_answer
        
    except TypeError as e:
        log_error(e)
        # Handle any TypeError that might occur and return an empty list.
        check_answer = []
        return check_answer
    
# function to change color of pegs
def change_pegs_color(x,y):
    '''
    
    Handles a click event in a peg-based puzzle game, updating the colors of pegs based on the game's current state. 
    This function is triggered when the "check" button within the game's interface is clicked.

    Parameters:
    - x (int): The x-coordinate of the mouse click.
    - y (int): The y-coordinate of the mouse click.

    Functionality:
    - Checks if the click is within the "check" button's region.
    - If so, it updates the colors of the current round's pegs based on the 'check_answer' array.
    - The function also manages the game's progression, including advancing rounds, determining win/lose conditions, 
      and resetting the game state for a new round.
    
    '''
    # Global variables are declared to modify the game state across the function calls.
    global round_count
    global check_answer
    global peglist
    global check_button_pressed
    global count_choose
    global selected_color_list

    # Check the current answer against the correct one.
    check_answer = check_if_correct()

    
    # Proceed only if check_answer has 4 elements (a complete guess).
    if len(check_answer) == 4:
        # Check if the click is within the predefined region of the 'check' button.
        if abs(x - 5) <= 30 * 2 and \
           abs(y + 322 ) <= 30 * 2:
            # Mark that the check button has been pressed.
            check_button_pressed = True
            # Update the colors of the pegs based on the check_answer array.
            for i in range(0,len(check_answer)):
                peglist[round_count][i].set_color(check_answer[i])
                peglist[round_count][i].draw()
            # Check for a win condition: all pegs are correctly guessed (all 'black').
            if 'black' in check_answer and len(set(check_answer)) == 1:
                # Increment round, trigger winner sequence, compare score, and exit the game.
                round_count += 1
                load_winner_gif()
                compare_score()
                try:
                    screen.bye()
                    
                except:
                    turtle.bye()
                    sys.exit()
            else:
                # Move to the next round if no win condition is met.
                round_count += 1
                
            # Check for a lose condition: 10 rounds reached without a correct guess.   
            if round_count == 10:
                if 'red' in check_answer or 'white' in check_answer:
                    # Trigger losing sequence and exit.
                    load_lose_gif()
                    turtle.textinput(f'right answer', f'{right_answer}')
                    try:
                        screen.bye()
                    except:
                        turtle.bye()
                        sys.exit()
                else:
                    # If the answer is correct, trigger winner sequence and exit.
                    compare_score()
                    load_winner_gif()
                    try:
                        screen.bye()
                    except:
                        turtle.bye()
                        sys.exit()
                  
                    
                
            else:
                # Reset the game state for a new round.
                count_choose = 0
                draw_guess_button()
                check_answer = []
                check_button_pressed = False
                selected_color_list = []

# function that compare score and write it in txt if valid
def compare_score():
    global round_count
    global list_of_info
    '''
    Compares the current game score with historical scores recorded in a text file, 
    and updates the file if the current score is among the top two scores.

    This function reads scores from 'BestScore.txt', and if the current score (represented by 'round_count') 
    is better than at least one of the top two scores, it is added to the file.
    '''

    # Check if the number of records in the text file is less than 2
    if len(list_of_info) < 2:
        # If less than 2, directly append the current score to the file
        with open('BestScore.txt', 'a') as file:
            # input current score
            file.write(f'{user_name } {round_count}\n')
    else:
        # If there are at least two records, compare with the higher score
        scores = []
        print(f'in compare score, {list_of_info}')
        for item in list_of_info:
            name, score = item.split()
            scores.append(int(score))
        higher_score = max(scores)

        # If the current score is better (lower) than the higher score, append it to the file
        if round_count < higher_score:
            with open('BestScore.txt', 'a') as file:
            # input current score
                file.write(f'{user_name } {round_count}\n')
         

# function for X button
def xbutton_pressed(x,y):
    '''
    Handles the event when the X button is pressed in the game interface.
    This function is triggered by a click within a specific region, indicating the X button press.

    Parameters:
    - x (int): The x-coordinate of the mouse click.
    - y (int): The y-coordinate of the mouse click.

    Functionality:
    - If the click is within the X button's region and the 'check_button_pressed' is False, 
      it resets the current selection.
    - The selected colors are cleared, and the 'count_choose' is reset.
    - The guess circles for the current round are reset to their default color (white).

    Global Variables:
    - count_choose: Counter for the number of choices made in the current round.
    - check_button_pressed: A boolean flag to indicate if the check button has been pressed.
    - selected_color_list: Stores the colors selected in the current round.
    - number_guess_circle: A list of lists containing circle objects for each round.
    - round_count: Tracks the current round of the game.
    '''
    global count_choose
    global check_button_pressed
    global selected_color_list
    global number_guess_circle
    global round_count
    try:
        # Check if the click is within the X button's region.
        if abs(x - 90) <= 30 * 2 and \
           abs(y + 320 ) <= 30 * 2:
            # Proceed only if the check button hasn't been pressed.
            if not check_button_pressed:
                # Clear the selected color list and reset the selection count.
                selected_color_list.pop()
                selected_color_list = []
                count_choose = 0
                # Redraw the guess button.
                draw_guess_button()
                # Reset the color of guess circles to white for the current round.
                for i in range(0,4):
                    number_guess_circle[round_count][i].set_color('white')
                    number_guess_circle[round_count][i].draw()
    except IndexError as e:
        log_error(e)
        # Handle the IndexError if it occurs, typically from 'pop' on an empty list.
        pass



def main():
    try:
        global count_choose
        global selected_color_list
        global number_guess_circle
        global round_count
        global colors
        global right_answer
        global check_answer
        global peglist
        global check_button_pressed
        global user_name
       
        # pop-up window
        user_name = turtle.textinput('Name', 'Your name: ')
        if not user_name: # if user input nothing and click ok, quit game
            turtle.bye()
            sys.exit()

        # draw board
        draw_board()
        
        # load check button
        check_turtle = load_check_button()
        # bind load button with click
        check_turtle.onclick(change_pegs_color)

        # load x button
        x_turtle = load_x_button()
        x_turtle.onclick(xbutton_pressed)

        # load historical best score
        start_file()
        load_best_score()

        # load quit button
        quit_turtle = quit_button()
        quit_turtle.onclick(exit_on_click)
        
        # draw guess buttons
        draw_guess_button()    
        
        # draw guesses circles
        draw_guesses_circles()

        # draw guess pegs
        draw_pegs()

        turtle.mainloop()
    except Exception as e:
        log_error(e)
    
if __name__ == "__main__":
    main()
