import csv

def get_chess_data(filename):
    games = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            games.append(row)
    return games

def compute_rating_difference(game):
    white = int(game["white_rating"])
    black = int(game["black_rating"])
    return white - black

def bucket_rating_difference(diff):
    if diff <= -300:
        return "Black +300"
    elif -300 < diff <= -100:
        return "Black +100 to +300"
    elif -100 < diff <= 100:
        return "Even (-100 to +100)"
    elif 100 < diff <= 300:
        return "White +100 to +300"
    else:
        return "White +300+"

def compute_opening_win_rates(games):
    stats = {}
    for game in games:
        opening = game["opening_name"]
        diff = compute_rating_difference(game)
        bucket = bucket_rating_difference(diff)

        if opening not in stats:
            stats[opening] = {}
        
        if bucket not in stats[opening]:
            stats[opening][bucket] = {
                "white_wins": 0,
                "black_wins": 0,
                "total_games": 0
            }
       
        result = game["winner"]

        if result == "white":
            stats[opening][bucket]["white_wins"] += 1
        elif result == "black":
            stats[opening][bucket]["black_wins"] += 1

        stats[opening][bucket]["total_games"] += 1 
    
    for opening in stats:
        for bucket in stats[opening]:
            data = stats[opening][bucket]
            total = data["total_games"]

            if total > 0:
                data["white_win_rate"] = data["white_wins"] / total
                data["black_win_rate"] = data["black_wins"] / total
            else:
                data["white_win_rate"] = 0
                data["black_win_rate"] = 0

    return stats

def write_results_to_file(results, output_filename):
    with open(output_filename, "w") as f:
        for key in results:
            f.write(f"Opening: {key}\n")
            for stat_key, stat_value in results[key].items():
                f.write(f"  {stat_key}: {stat_value}\n")
            f.write("\n")

if __name__ == "__main__":
    games = get_chess_data("games.csv")
    opening_stats = compute_opening_win_rates(games)
    write_results_to_file(opening_stats, "summarized_data.txt")