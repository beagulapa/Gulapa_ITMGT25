'''Module 4: Individual Programming Assignment 1

Parsing Data

This assignment covers your ability to manipulate data in Python.
'''

def relationship_status(from_member, to_member, social_graph):
    '''Relationship Status.
    20 points.

    Let us pretend that you are building a new app.
    Your app supports social media functionality, which means that users can have
    relationships with other users.

    There are two guidelines for describing relationships on this social media app:
    1. Any user can follow any other user.
    2. If two users follow each other, they are considered friends.

    This function describes the relationship that two users have with each other.

    Please see "assignment-4-sample-data.py" for sample data. The social graph
    will adhere to the same pattern.

    Parameters
    ----------
    from_member: str
        the subject member
    to_member: str
        the object member
    social_graph: dict
        the relationship data    

    Returns
    -------
    str
        "follower" if fromMember follows toMember,
        "followed by" if fromMember is followed by toMember,
        "friends" if fromMember and toMember follow each other,
        "no relationship" if neither fromMember nor toMember follow each other.
    '''
    # Replace `pass` with your code. 
    # Stay within the function. Only use the parameters as input. The function should return your answer.
    try:
        if to_member not in social_graph[from_member]["following"]:
            if from_member in social_graph[to_member]["following"]:
                print("followed by")
            else:
                print("no relationship")
        else:
            if from_member in social_graph[to_member]["following"]:
                print("friends")
            else:
                print("follower")
    #if insufficient user data
    except:
        if from_member in social_graph:
            if to_member in social_graph[from_member]["following"]:
                print("follower")
            else:
                print("no relationship")
        else:
            if from_member in social_graph[to_member]["following"]:
                print("followed by")
            else: 
                print("no relationship")


def tic_tac_toe(board):
    '''Tic Tac Toe. 
    25 points.

    Tic Tac Toe is a common paper-and-pencil game. 
    Players must attempt to successfully draw a straight line of their symbol across a grid.
    The player that does this first is considered the winner.

    This function evaluates a tic tac toe board and returns the winner.

    Please see "assignment-4-sample-data.py" for sample data. The board will adhere
    to the same pattern. The board may by 3x3, 4x4, 5x5, or 6x6. The board will never
    have more than one winner. The board will only ever have 2 unique symbols at the same time.

    Parameters
    ----------
    board: list
        the representation of the tic-tac-toe board as a square list of lists

    Returns
    -------
    str
        the symbol of the winner or "NO WINNER" if there is no winner
    '''
    # Replace `pass` with your code. 
    # Stay within the function. Only use the parameters as input. The function should return your answer.
    #diagonal 1 is upper left to lower right \
    def diagonal1(board):
        diag1 = ''
        if len(set([board[i][i] for i in range(len(board))])) == 1:
            diag1 += [board[i][i] for i in range(len(board))][1]
        else:
            diag1 += 'NO WINNER'
        return diag1

    #diagonal 2 is upper right to lower left /
    def diagonal2(board):
        diag2 = ''
        if len(set([board[3-1-i][i] for i in range(len(board))])) == 1:
            diag2 += [board[3-1-i][i] for i in range(len(board))][1]
        else:
            diag2 += 'NO WINNER'
        return diag2

    def horizontal(board):
        hz = ''
        if 1 in [len(set(x)) for x in board]:
            hloc = [len(set(x)) for x in board].index(1)
            hz += [x for x in board][hloc][1]
        else:
            hz += 'NO WINNER'
        return hz

    def vertical(board):
        vt = ''
        if 1 in [len(set(list(i))) for i in zip(*board)]:
            vloc = [len(set(list(i))) for i in zip(*board)].index(1)
            vt += [list(i) for i in zip(*board)][vloc][1]
        else:
            vt += 'NO WINNER'
        return vt

    whole_game = [horizontal(board),vertical(board),diagonal1(board),diagonal2(board)]

    ans = ''
    if 'X' in whole_game:
        ans += 'X'
    elif 'O' in whole_game:
        ans += 'O'
    else:
        ans = 'NO WINNER'

    return ans

def eta(first_stop, second_stop, route_map):
    '''ETA. 
    25 points.

    A shuttle van service is tasked to travel along a predefined circlar route.
    This route is divided into several legs between stops.
    The route is one-way only, and it is fully connected to itself.

    This function returns how long it will take the shuttle to arrive at a stop
    after leaving another stop.

    Please see "mod-4-ipa-1-sample-data.py" for sample data. The route map will
    adhere to the same pattern. The route map may contain more legs and more stops,
    but it will always be one-way and fully enclosed.

    Parameters
    ----------
    first_stop: str
        the stop that the shuttle will leave
    second_stop: str
        the stop that the shuttle will arrive at
    route_map: dict
        the data describing the routes

    Returns
    -------
    int
        the time it will take the shuttle to travel from first_stop to second_stop
    '''
    # Replace `pass` with your code. 
    # Stay within the function. Only use the parameters as input. The function should return your answer.
    start_list = []
    for i in list(legs):
        start_list = [i[0] for i in list(legs)]
        
    end_list = []
    for i in list(legs):
        end_list = [i[1] for i in list(legs)]
    
    num_list = []
    for x in list(legs.values()):
        num_list = [x['travel_time_mins'] for x in list(legs.values())]
        
    startind = start_list.index(first_stop)
    endind = end_list.index(second_stop)
    
    minutes = 0
    if first_stop == second_stop:
        minutes = sum([t["travel_time_mins"] for t in legs.values()])
    else:
        if (first_stop,second_stop) in legs:
            minutes = legs[(first_stop,second_stop)]['travel_time_mins']
        else:
            if startind < endind:
                minutes = sum(num_list[startind:(endind+1)])
            else:
                minutes = sum(num_list[startind:endind+(len(num_list))]) + sum(num_list[0:endind+1])
    return minutes