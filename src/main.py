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

    profiles = {
        "Late-Night Hip-Hop Worker": {
            "genre": "hip-hop", "mood": "focused",
            "target_energy": 0.78, "likes_acoustic": False
        },
        "Coffeehouse Jazz Listener": {
            "genre": "jazz", "mood": "relaxed",
            "target_energy": 0.37, "likes_acoustic": True
        },
        "Gym Workout Listener": {
            "genre": "pop", "mood": "intense",
            "target_energy": 0.93, "likes_acoustic": False
        },
        # Adversarial 1: genre and mood exist in the catalog but no song satisfies BOTH.
        # Tests whether the 0.40 genre weight always overrides the 0.30 mood weight
        # when the two signals conflict, and whether the formula handles partial matches gracefully.
        "Moody Electronic User (Adversarial)": {
            "genre": "electronic", "mood": "moody",
            "target_energy": 0.75, "likes_acoustic": False
        },
        # Adversarial 2: cold-start user with no genre or mood declared.
        # Tests the degraded-mode floor: with 70% of scoring weight unavailable (0.40 + 0.30),
        # the formula can only differentiate by energy (0.20) and acousticness (0.10),
        # producing a technically valid but practically meaningless ranked list.
        "Cold Start User (Adversarial)": {
            "genre": "", "mood": "",
            "target_energy": 0.50, "likes_acoustic": False
        },
    }

    for profile_name, user_prefs in profiles.items():
        print(f"\n{'='*55}")
        print(f"Profile: {profile_name}")
        print(f"{'='*55}")
        recommendations = recommend_songs(user_prefs, songs, k=5)
        for rec in recommendations:
            song, score, explanation = rec
            print(f"  {song['title']} ({song['genre']}/{song['mood']}) — Score: {score:.3f}")
            print(f"  Because: {explanation}")
            print()


if __name__ == "__main__":
    main()
