from pkgutil import get_data
import random as r
import json
import discord

player_file = 'player_data.json'
game_file = 'game_data.json'

#Discord Functions
async def find_queue(queues):
    for x in queues:
        if len(x.players) < 6:
            return x

def create_match_id(queues):
    while True:
        found = False
        new_match_id = r.randint(1, 100)
        for x in queues:
            if new_match_id == x.match_id:
                found = True
                break
        if not found:
            return new_match_id

async def make_random_teams(players):
    new_list = players
    r.shuffle(new_list)
    return [new_list[x] for x in range(0, 3)], [new_list[x] for x in range(3, 6)]

async def get_captains(players):
    new_list = players
    r.shuffle(new_list)
    return new_list[0], new_list[1], [new_list[0]], [new_list[1]]


#File functions
def load_dict(file):
    with open(file, 'r') as file:
        data = json.load(file)
        return data

def check_user(id):
    data = load_dict(player_file)
    for key in data:
        if data[key]['user_id'] == id:
            return True
    return False

def create_user(user, name):
    data = load_dict(player_file)
    with open(player_file, 'w') as file:
        data[name] = {"discord_name": user.name, "user_id": str(user.id), "points": 2000, "games_played": 0, "wins": 0, "losses": 0}
        json.dump(data, file, indent = 4)

def create_lb():
    data = load_dict(player_file)
    player_data = [(data[x]['user_id'], data[x]['points']) for x in data]
    player_data.sort(key = lambda x: x[1])
    player_data.reverse()
    return player_data

def get_player_data(user):
    data = load_dict(player_file)
    player_name = get_name(user)
    return data[player_name]['points']

def get_name(user):
    data = load_dict(player_file)
    for x in data:
        if data[x]['user_id'] == str(user.id):
            return str(x)

def check_name(chosen_name):
    data = load_dict(player_file)
    for x in data:
        if data[x]['discord_name'] == chosen_name:
            return True

def get_captain_picks_data(players):
    return [(x, get_player_data(x)) for x in players]

def get_match_id():
    data = load_dict(game_file)
    if len(data) == 0:
        return 1
    highest = 1
    for x in data:
        num = x.split()
        if highest < int(num[1]):
            highest = int(num[1])
    return highest + 1


def write_match(queue):
    data = load_dict(game_file)
    if queue.category == 'captains':
        data[f"game {str(queue.match_id)}"] = {"category": queue.category, "already_reported": "False", "players": [get_name(x) for x in queue.players], "team_one": [get_name(x) for x in queue.team_one], "team_two": [get_name(x) for x in queue.team_two], "captain_one": get_name(queue.captain_one), "captain_two": get_name(queue.captain_two)}
    else:
        data[f"game {str(queue.match_id)}"] = {"category": queue.category, "already_reported": "False", "players": [get_name(x) for x in queue.players], "team_one": [get_name(x) for x in queue.team_one], "team_two": [get_name(x) for x in queue.team_two], "captain_one": None, "captain_two": None}
    with open(game_file, 'w') as file:
        json.dump(data, file, indent = 4)


def balance_teams(players):
    def combs(a):
        if len(a) == 0: return [[]]
        cs = []
        for c in combs(a[1:]): cs += [c, c+[a[0]]]
        return cs
    data = load_dict(player_file)
    player_names = [get_name(x) for x in players]
    player_data, closest_set, best_value = [(x, data[x]['points']) for x in player_names], None, None
    combos = [x for x in combs([x[1] for x in player_data]) if len(x) == 3]
    for i in combos:
        team_two = [x[1] for x in player_data]
        for x in i:
            team_two.pop(team_two.index(x))
        team_one_points, team_two_points = sum(i), sum(team_two)
        abs_value = abs(team_one_points - team_two_points) / 3
        if best_value == None:
            best_value = abs_value
            closest_set = [i, team_two]
        else:
            if abs_value < best_value:
                best_value, closest_set = abs_value, [i, team_two]
    team_one_values, team_two_values, team_one, team_two, taken_users = closest_set[0], closest_set[1], [], [], []
    for value in team_one_values:
        for x in player_data:
            if x[1] == value and x[0] not in taken_users:
                taken_users.append(x[0])
                team_one.append(x[0])
    for value in team_two_values:
        for x in player_data:
            if x[1] == value and x[0] not in taken_users:
                taken_users.append(x[0])
                team_two.append(x[0])
    return team_one, team_two

def get_game_count():
    data = load_dict(game_file)
    available = 0
    for x in data:
        if data[x]['already_reported'] == str("False"):
            available += 1
    return available

def check_games():
    available = get_game_count()
    if available > 0:
        return True


async def report_game(ctx, game_id, team_winner):
    try:
        game_data = load_dict(game_file)
        player_data = load_dict(player_file)
        game = game_data[game_id]
    except:
        await ctx.respond(f"Could not find game {game_id} please try again.")
    else:
        team_one, team_two = [x for x in game['team_one']], [x for x in game['team_two']]
        embed = discord.Embed(title = f"Successfully reported game {game_id}", color = discord.Color.blue())
        if team_winner == 'Team 1':
            for x in team_one:
                member = ctx.guild.get_member(int(player_data[x]['user_id']))
                points = get_player_data(member) + 10
                player_data[x]['points'] = points
            for x in team_two:
                member = ctx.guild.get_member(int(player_data[x]['user_id']))
                points = get_player_data(member) - 10
                player_data[x]['points'] = points
            embed.add_field(name = "Winning team", value = ' '.join([x for x in team_one]))
            embed.add_field(name = "Losing Team", value = ' '.join([x for x in team_one]))
                

        elif team_winner == 'Team 2':
            for x in team_one:
                member = ctx.guild.get_member(int(player_data[x]['user_id']))
                points = get_player_data(member) - 10
                player_data[x]['points'] = points
            for x in team_two:
                member = ctx.guild.get_member(int(player_data[x]['user_id']))
                points = get_player_data(member) + 10
                player_data[x]['points'] = points
        
        game['already_reported'] = 'True'
        with open(game_file, 'w') as file:
            json.dump(game_data, file, indent = 4)
        with open(player_file, 'w') as file:
            json.dump(player_data, file, indent = 4)


        
        
                 
    
