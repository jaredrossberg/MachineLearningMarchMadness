import csv
import sys

# Reads in a csv file and returns it as a 2D array
def read_csv(filename):
    rows = []
    with open(filename, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csv_reader:
            rows.append(row)
    return rows

# Fixes mismatched names between the two spreadsheets
def fix_school_name(name):
    name = name.replace(' NCAA', '')
    if name == 'Southern California':
        return 'USC'
    if name == 'Brigham Young':
        return 'BYU'
    if name == 'Louisiana State':
        return 'LSU'
    if name == 'North Carolina-Greensboro':
        return 'UNC Greensboro'
    if name == 'North Carolina':
        return 'UNC'
    if name == 'North Carolina State':
        return 'NC State'
    if name == 'UC-Santa Barbara':
        return 'UCSB'
    if name == 'Connecticut':
        return 'UConn'
    if name == 'Central Florida':
        return 'UCF'
    if name == 'Mississippi':
        return 'Ole Miss'
    if name == 'Virginia Commonwealth':
        return 'VCU'
    if name == "Saint Mary's (CA)":
        return "Saint Mary's"
    if name == 'Pennsylvania':
        return 'Penn'
    if name == 'Maryland-Baltimore County':
        return 'UMBC'
    if name == 'Texas Christian':
        return 'TCU'
    if name == 'Long Island University':
        return 'LIU'
    if name == 'East Tennessee State':
        return 'ETSU'
    if name == 'Southern Methodist':
        return 'SMU'
    if name == 'North Carolina-Wilmington':
        return 'UNC Wilmington'
    if name == 'North Carolina-Asheville':
        return 'UNC Asheville'
    if name == "Saint Joseph's":
        return "St. Joseph's"
    if name == 'Pittsburgh':
        return 'Pitt'
    if name == 'University of California':
        return 'California'
    if name == 'Massachusetts':
        return 'UMass'
    if name == 'Nevada-Las Vegas':
        return 'UNLV'
    if name == 'Detroit Mercy':
        return 'Detroit'
    if name == 'Cal State Long Beach':
        return 'Long Beach State'
    if name == 'Southern Mississippi':
        return 'Southern Miss'
    if name == 'Texas-San Antonio':
        return 'UTSA'
    if name == 'Texas-El Paso':
        return 'UTEP'
    return name

# These team do not have stats in 'Team Stats.csv'
# I chose to just throw out these games, but we could also initialize to all zeros or something
def is_missing(name):
    if name == "St. Peter's":
        return True
    False


def main():
    # Creates a map of maps that allows you to filter by year, then team, then opponent
    # to find if they won or lost
    game_results = read_csv('Game Results.csv')
    game_results_header = game_results[0]
    game_results = game_results[1:]

    index_school_name = game_results_header.index('School')
    index_opponent_name = game_results_header.index('Opponent')
    results_dict = dict()
    for row in game_results:
        year = row[1]
        winner = row[index_school_name].split(' ', 1)[1]
        loser = row[index_opponent_name].split(' ', 1)[1]

        if not year in results_dict:
            results_dict[year] = dict()
        if not winner in results_dict[year]:
            results_dict[year][winner] = dict()
        if not loser in results_dict[year]:
            results_dict[year][loser] = dict()
        results_dict[year][winner][loser] = True
        results_dict[year][loser][winner] = False

    # Creates a map of maps that allows you to filter by year then team to get
    # all of their stats for that year
    stats = read_csv('Team Stats.csv')
    stats_header = stats[1]
    stats = stats[2:]

    index_school_name = stats_header.index('School')
    stats_dict = dict()
    for row in stats:
        year = row[0]
        team = fix_school_name(row[index_school_name])
        if not year in stats_dict:
            stats_dict[year] = dict()
        stats_dict[year][team] = row

    # index of column in CSV with stat
    indexes_unnormalized = {
        'W-L%': stats_header.index('W-L%'),
        'SOS': stats_header.index('SOS'),
        'FG%': stats_header.index('FG%'),
        '3P%': stats_header.index('3P%'),
        'FT%': stats_header.index('FT%'),
    }
    indexes_normalized = {
        'PPG': stats_header.index('Tm.'),
        'Allowed PPG': stats_header.index('Opp.'),
        'ORB': stats_header.index('ORB'),
        'Rebounds': stats_header.index('TRB'),
        'Assists': stats_header.index('AST'),
        'Steals': stats_header.index('STL'),
        'Blocks': stats_header.index('BLK'),
        'Turnovers': stats_header.index('TOV'),
        'PF': stats_header.index('PF'),
    }
    index_games_played = stats_header.index('G')

    # Go through each game and calculate the difference in various stats bewteen the winning and losing teams
    # Save strings with data formatted for CSV files in adjusted_data
    # Note: Each game is done twice. Once to show the winning team winning and once to show the losing team losing
    adjusted_data = []
    for year in results_dict:
        for team1 in results_dict[year]:
            for team2 in results_dict[year][team1]:
                if is_missing(team1) or is_missing(team2):
                    continue

                stats_team1 = stats_dict[year][team1]
                stats_team2 = stats_dict[year][team2]

                num_games_1 = float(stats_team1[index_games_played])
                num_games_2 = float(stats_team2[index_games_played])

                diff = []
                for curr_stat in indexes_unnormalized:
                    index = indexes_unnormalized[curr_stat]
                    diff.append(float(stats_team1[index]) - float(stats_team2[index]))
                for curr_stat in indexes_normalized:
                    index = indexes_normalized[curr_stat]
                    diff.append((float(stats_team1[index]) / num_games_1) - (float(stats_team2[index]) / num_games_2))
                did_team1_win = results_dict[year][team1][team2]
                diff.append(did_team1_win)
                adjusted_data.append(diff)

    # Output array containing desired data to csv
    original_stdout = sys.stdout
    with open('Adjusted Data.csv', 'w') as f:
        sys.stdout = f
        for curr_stat in indexes_unnormalized:
            print('{:s},'.format(curr_stat), end='')
        for curr_stat in indexes_normalized:
            print('{:s},'.format(curr_stat), end='')

        print('Output (win=1 loss=0)')
        for row in adjusted_data:
            for i, value in enumerate(row):
                if i == len(row)-1:
                    print('{:b}'.format(value))
                else:
                    print('{:f},'.format(value), end='')
    sys.stdout = original_stdout
    pass

if __name__ == '__main__':
    main()
