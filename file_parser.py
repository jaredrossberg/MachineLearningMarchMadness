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
    game_results = read_csv('Game Results.csv')[1:]
    results_dict = dict()
    for row in game_results:
        year = row[1]
        winner = row[5].split(' ', 1)[1]
        loser = row[7].split(' ', 1)[1]

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
    stats = read_csv('Team Stats.csv')[2:]
    stats_dict = dict()
    for row in stats:
        year = row[0]
        team = fix_school_name(row[2].replace(' NCAA', ''))
        if not year in stats_dict:
            stats_dict[year] = dict()
        stats_dict[year][team] = row

    # index of column in CSV with stat
    index_win_percentage            = stats_header.index('W-L%')
    index_sos                       = stats_header.index('SOS')
    index_total_points_scored       = stats_header.index('Tm.')
    index_total_points_allowed      = stats_header.index('Opp.')
    index_games_played              = stats_header.index('G')
    index_field_goal_percentage     = stats_header.index('FG%')
    index_three_point_percentage    = stats_header.index('3P%')
    index_free_throw_percentage     = stats_header.index('FT%')
    index_offensive_rebounds        = stats_header.index('ORB')
    index_total_rebounds            = stats_header.index('TRB')
    index_total_assists             = stats_header.index('AST')
    index_total_steals              = stats_header.index('STL')
    index_total_blocks              = stats_header.index('BLK')
    index_total_turnovers           = stats_header.index('TOV')
    index_total_personal_fouls      = stats_header.index('PF')

    # Go through each game and calculate the difference in various stats bewteen the winning and losing teams
    # Save strings with data formatted for CSV files in adjusted_data
    # Note: Each game is done twice. Once to show the winning team winning and once to show the losing team losing
    adjusted_data = []
    for year in results_dict:
        for team1 in results_dict[year]:
            for team2 in results_dict[year][team1]:
                if is_missing(team1) or is_missing(team2):
                    continue

                num_games_1 = float(stats_dict[year][team1][index_games_played])
                num_games_2 = float(stats_dict[year][team2][index_games_played])
                did_team1_win = results_dict[year][team1][team2]

                # Normalize by number of games and find difference
                diff_win_percentage = float(stats_dict[year][team1][index_win_percentage]) \
                    - float(stats_dict[year][team2][index_win_percentage])
                diff_strength_of_schedule = float(stats_dict[year][team1][index_sos]) \
                    - float(stats_dict[year][team2][index_sos])
                diff_points = (float(stats_dict[year][team1][index_total_points_scored]) / num_games_1) \
                    - (float(stats_dict[year][team2][index_total_points_scored]) / num_games_2)
                diff_points_allowed = (float(stats_dict[year][team1][index_total_points_allowed]) / num_games_1) \
                    - (float(stats_dict[year][team2][index_total_points_allowed]) / num_games_2)
                diff_field_goal_percentage = float(stats_dict[year][team1][index_field_goal_percentage]) \
                    - float(stats_dict[year][team2][index_field_goal_percentage])
                diff_three_point_percentage = float(stats_dict[year][team1][index_three_point_percentage]) \
                    - float(stats_dict[year][team2][index_three_point_percentage])
                diff_free_throw_percentage = float(stats_dict[year][team1][index_free_throw_percentage]) \
                    - float(stats_dict[year][team2][index_free_throw_percentage])
                diff_offensive_rebounds = (float(stats_dict[year][team1][index_offensive_rebounds]) / num_games_1) \
                    - (float(stats_dict[year][team2][index_offensive_rebounds]) / num_games_2)
                diff_rebounds = (float(stats_dict[year][team1][index_total_rebounds]) / num_games_1) \
                    - (float(stats_dict[year][team2][index_total_rebounds]) / num_games_2)
                diff_assists = (float(stats_dict[year][team1][index_total_assists]) / num_games_1) \
                    - (float(stats_dict[year][team2][index_total_assists]) / num_games_2)
                diff_steals = (float(stats_dict[year][team1][index_total_steals]) / num_games_1) \
                    - (float(stats_dict[year][team2][index_total_steals]) / num_games_2)
                diff_blocks = (float(stats_dict[year][team1][index_total_blocks]) / num_games_1) \
                    - (float(stats_dict[year][team2][index_total_blocks]) / num_games_2)
                diff_turnovers = (float(stats_dict[year][team1][index_total_turnovers]) / num_games_1) \
                    - (float(stats_dict[year][team2][index_total_turnovers]) / num_games_2)
                diff_fouls = (float(stats_dict[year][team1][index_total_personal_fouls]) / num_games_1) \
                    - (float(stats_dict[year][team2][index_total_personal_fouls]) / num_games_2)

                adjusted_data.append('{:f}, {:f}, {:f}, {:f}, {:f}, {:f}, {:f}, {:f}, {:f}, {:f}, {:f}, {:f}, {:f}, {:f}, {:b}'.format( \
                    diff_win_percentage, diff_strength_of_schedule, diff_points, diff_points_allowed, diff_field_goal_percentage, \
                    diff_three_point_percentage, diff_free_throw_percentage, diff_offensive_rebounds, diff_rebounds, diff_assists, \
                    diff_steals, diff_blocks, diff_turnovers, diff_fouls, did_team1_win))

    # Output array containing desired data to csv
    original_stdout = sys.stdout
    with open('Adjusted Data.csv', 'w') as f:
        sys.stdout = f
        print("Win%, SOS, PPG, APPG, FG%, 3P%, FT%, ORB, Rebounds, Assists, Steals, Blocks, Turnovers, PF, Output (1 for win, 0 for loss)")
        for i in range(len(adjusted_data)):
            print(adjusted_data[i])
    sys.stdout = original_stdout
    pass

if __name__ == '__main__':
    main()
