from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

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

    def _score(self, user: UserProfile, song: Song) -> float:
        genre_score = 1.0 if song.genre == user.favorite_genre else 0.0
        mood_score = 1.0 if song.mood == user.favorite_mood else 0.0
        energy_score = 1.0 - abs(song.energy - user.target_energy)
        acousticness_score = song.acousticness if user.likes_acoustic else 1.0 - song.acousticness
        return (0.40 * genre_score) + (0.30 * mood_score) + (0.20 * energy_score) + (0.10 * acousticness_score)

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        ranked = sorted(self.songs, key=lambda s: self._score(user, s), reverse=True)
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append(f"genre matches your favorite ({song.genre})")
        if song.mood == user.favorite_mood:
            reasons.append(f"mood matches your preference ({song.mood})")
        energy_diff = abs(song.energy - user.target_energy)
        if energy_diff <= 0.15:
            reasons.append(f"energy level is close to your target ({song.energy:.2f})")
        if user.likes_acoustic and song.acousticness >= 0.7:
            reasons.append(f"highly acoustic ({song.acousticness:.2f})")
        elif not user.likes_acoustic and song.acousticness <= 0.3:
            reasons.append(f"low acousticness fits your style ({song.acousticness:.2f})")
        if not reasons:
            reasons.append("overall profile similarity")
        return "Recommended because: " + ", ".join(reasons) + "."


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return them as a list of typed dictionaries."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences and return a (score, reasons) tuple."""
    reasons = []

    genre_score = 1.0 if song.get("genre") == user_prefs.get("genre") else 0.0
    if genre_score == 1.0:
        reasons.append(f"genre match ({song['genre']})")

    mood_score = 1.0 if song.get("mood") == user_prefs.get("mood") else 0.0
    if mood_score == 1.0:
        reasons.append(f"mood match ({song['mood']})")

    target_energy = user_prefs.get("target_energy", 0.5)
    energy_score = 1.0 - abs(song.get("energy", 0.5) - target_energy)
    if abs(song.get("energy", 0.5) - target_energy) <= 0.15:
        reasons.append(f"energy close to target ({song['energy']:.2f})")

    likes_acoustic = user_prefs.get("likes_acoustic", False)
    if likes_acoustic:
        acousticness_score = song.get("acousticness", 0.5)
        if acousticness_score >= 0.7:
            reasons.append(f"highly acoustic ({song['acousticness']:.2f})")
    else:
        acousticness_score = 1.0 - song.get("acousticness", 0.5)
        if song.get("acousticness", 0.5) <= 0.3:
            reasons.append(f"low acousticness ({song['acousticness']:.2f})")

    if not reasons:
        reasons.append("overall profile similarity")

    score = (0.40 * genre_score) + (0.30 * mood_score) + (0.20 * energy_score) + (0.10 * acousticness_score)
    return (score, reasons)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank all songs by score against user preferences and return the top k with explanations."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: (-x[1], x[0]["id"]))
    return scored[:k]
