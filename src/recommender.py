import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load song records from a CSV file and convert numeric fields."""
    print(f"Loading songs from {csv_path}...")
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        # DictReader uses each CSV header as a dictionary key.
        songs = list(csv.DictReader(csv_file))

    for song in songs:
        # Convert numeric columns while leaving text columns as strings.
        for field in ("id", "tempo_bpm"):
            if field in song and song[field] != "":
                song[field] = int(song[field])

        for field in ("energy", "valence", "danceability", "acousticness"):
            if field in song and song[field] != "":
                song[field] = float(song[field])

    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against the user's genre, mood, and energy preferences."""
    total_score = 0.0
    reasons = []

    if song["genre"] == user_prefs["genre"]:
        total_score += 2.0
        reasons.append("genre match (+2.0)")

    if song["mood"] == user_prefs["mood"]:
        total_score += 1.0
        reasons.append("mood match (+1.0)")

    energy_score = 1.0 - abs(song["energy"] - user_prefs["energy"])
    energy_score = max(0.0, min(1.0, energy_score))
    total_score += energy_score
    reasons.append(f"energy similarity (+{energy_score:.1f})")

    return total_score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """Rank songs by score and return the top k with reasons."""
    if k <= 0 or not songs:
        return []

    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored_songs.append((song, score, reasons))

    ranked_songs = sorted(scored_songs, key=lambda recommendation: recommendation[1], reverse=True)
    return ranked_songs[:k]
