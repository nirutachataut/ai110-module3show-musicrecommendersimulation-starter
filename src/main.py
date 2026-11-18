"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    profiles = [
        ("High-Energy Pop", {"genre": "pop", "mood": "happy", "energy": 0.9}),
        ("Chill Lofi", {"genre": "lofi", "mood": "chill", "energy": 0.2}),
        ("Deep Intense Rock", {"genre": "rock", "mood": "intense", "energy": 0.9}),
        ("Conflicting Sad Rock", {"genre": "rock", "mood": "sad", "energy": 0.9}),
        ("Unsupported Genre", {"genre": "shoegaze", "mood": "chill", "energy": 0.2}),
    ]

    for profile_name, user_prefs in profiles:
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\n=== {profile_name} ===")
        print(f"Preferences: {user_prefs}")
        print("Top 5 recommendations:\n")
        for rank, (song, score, reasons) in enumerate(recommendations, start=1):
            title = song.get("title", "Unknown title")
            artist = song.get("artist")
            song_name = f"{title} - {artist}" if artist else title

            print(f"{rank}. {song_name}")
            print(f"   Score: {score:.2f}")
            print("   Reasons:")
            for reason in reasons:
                print(f"     - {reason}")
            print()


if __name__ == "__main__":
    main()
