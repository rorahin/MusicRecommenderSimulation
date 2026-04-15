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
    # Switch scoring mode here — one line change.
    # Available: BALANCED | GENRE_FIRST | MOOD_FIRST | ENERGY_FOCUSED | DISCOVERY
    SCORING_MODE = "BALANCED"

    songs = load_songs("data/songs.csv")

    profiles = {
        # Profile 1: Late-night focused hip-hop worker.
        # Wants vocal-heavy tracks (not instrumental), some spoken word (rap),
        # moderate-to-high tempo, and high danceability.
        "Late-Night Hip-Hop Worker": {
            "genre": "hip-hop",
            "mood": "focused",
            "target_energy": 0.78,
            "likes_acoustic": False,
            "target_tempo": 0.37,        # ~95 BPM normalized: (95-58)/(158-58) = 0.37
            "target_danceability": 0.80,
            "wants_popular": True,
            "wants_instrumental": False,
            "target_speechiness": 0.20,  # expects some rap/spoken word
        },
        # Profile 2: Coffeehouse jazz listener.
        # Prefers acoustic, relaxed, slow-tempo, mostly instrumental with light vocals.
        "Coffeehouse Jazz Listener": {
            "genre": "jazz",
            "mood": "relaxed",
            "target_energy": 0.37,
            "likes_acoustic": True,
            "target_tempo": 0.32,        # ~90 BPM normalized: (90-58)/(158-58) = 0.32
            "target_danceability": 0.50,
            "wants_popular": False,
            "wants_instrumental": False,  # jazz vocals are appreciated
            "target_speechiness": 0.07,
        },
        # Profile 3: Gym workout listener.
        # Wants high energy, high danceability, fast tempo, popular tracks, minimal acoustics.
        "Gym Workout Listener": {
            "genre": "pop",
            "mood": "intense",
            "target_energy": 0.93,
            "likes_acoustic": False,
            "target_tempo": 0.74,        # ~132 BPM normalized: (132-58)/(158-58) = 0.74
            "target_danceability": 0.88,
            "wants_popular": True,
            "wants_instrumental": False,
            "target_speechiness": 0.06,
        },
        # Adversarial 1: genre and mood exist in the catalog but no song satisfies BOTH.
        # Tests whether the 0.35 genre weight always overrides the 0.25 mood weight
        # when the two signals conflict, and whether the formula handles partial matches gracefully.
        "Moody Electronic User (Adversarial)": {
            "genre": "electronic",
            "mood": "moody",
            "target_energy": 0.75,
            "likes_acoustic": False,
            "target_tempo": 0.82,        # ~140 BPM normalized: (140-58)/(158-58) = 0.82
            "target_danceability": 0.90,
            "wants_popular": False,
            "wants_instrumental": True,  # electronic/IDM skew
            "target_speechiness": 0.04,
        },
        # Adversarial 2: cold-start user with no genre or mood declared.
        # Tests the degraded-mode floor: with 60% of scoring weight unavailable (0.35 + 0.25),
        # the formula can only differentiate by energy (0.15), acousticness (0.08),
        # tempo (0.07), danceability (0.04), and the 3 new features (0.06 combined),
        # producing a technically valid but practically limited ranked list.
        "Cold Start User (Adversarial)": {
            "genre": "",
            "mood": "",
            "target_energy": 0.50,
            "likes_acoustic": False,
            "target_tempo": 0.50,
            "target_danceability": 0.50,
            "wants_popular": True,
            "wants_instrumental": False,
            "target_speechiness": 0.05,
        },
    }

    for profile_name, user_prefs in profiles.items():
        print(f"\n{'='*60}")
        print(f"Profile: {profile_name}  |  Mode: {SCORING_MODE}")
        print(f"{'='*60}")
        recommendations = recommend_songs(user_prefs, songs, k=5, mode=SCORING_MODE)
        for rec in recommendations:
            song, score, explanation = rec
            print(f"  {song['title']} ({song['genre']}/{song['mood']}) — Score: {score:.3f}")
            print(f"  Because: {explanation}")
            print()


if __name__ == "__main__":
    main()
