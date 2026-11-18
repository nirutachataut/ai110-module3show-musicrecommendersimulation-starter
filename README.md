# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This project is a small content-based music recommender. It compares songs in a CSV catalog with a user's favorite genre, favorite mood, and target energy. Genre and mood matches earn points, and songs with energy closer to the target earn more points. The program ranks the songs, returns the top five, and shows why each one received its score. The local sample catalog contains 20 songs.

---

## How The System Works

### System overview

This system uses content-based filtering: it compares each song’s attributes with a user’s musical preferences. Songs that better match the user’s favorite genre and mood, and whose energy is closer to the user’s target, receive higher scores. The command-line app uses dictionaries loaded from the CSV file. The `Song`, `UserProfile`, and `Recommender` classes provide an object-oriented version of the same scoring rule.

**Song features**

The `Song` class represents these attributes from `data/songs.csv`:

- `id` — an identifier for the song
- `title` — the song title
- `artist` — the performing artist
- `genre` — the musical style, such as pop or lo-fi
- `mood` — a descriptive feeling, such as happy or chill
- `energy` — a numeric value from 0 to 1 representing intensity
- `tempo_bpm` — the song’s tempo in beats per minute
- `valence` — a numeric value from 0 to 1 representing a more positive or more subdued feeling
- `danceability` — a numeric value from 0 to 1 representing how suitable the rhythm is for dancing
- `acousticness` — a numeric value from 0 to 1 representing how acoustic or electronic the song sounds

**UserProfile features**

The `UserProfile` class stores a `favorite_genre`, a `favorite_mood`, a `target_energy`, and a `likes_acoustic` preference. The scoring rule does not currently use `likes_acoustic`. The command-line app supplies the first three preferences in a dictionary.

### Scoring recipe

For each song, start with a score of 0 and apply these rules:

- Add **2.0 points** if the song’s genre matches the user’s favorite genre.
- Add **1.0 point** if the song’s mood matches the user’s favorite mood.
- Add energy similarity points using `1 - abs(song_energy - target_energy)`. Song and target energy are assumed to range from 0.0 to 1.0, so a closer energy match earns more points.

Add these points together to get the song’s final recommendation score.

### Ranking process

The program will read every song from `data/songs.csv`, calculate and store each song’s total score, then sort all songs from highest to lowest score. It will return the first **K** songs as the Top K recommendations.

### Potential biases and limitations

- Genre has twice the weight of mood, so a genre match can outweigh a better mood match.
- Exact genre and mood matching may miss songs with similar qualities but different labels.
- Using only genre, mood, and energy cannot capture every part of a person’s musical taste. Other available features, such as tempo or danceability, could be considered later.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Captured by running `python3 -m src.main` with the local 20-song catalog:

```text
Loading songs from data/songs.csv...
Loaded songs: 20

Top recommendations:

1. Sunrise City - Neon Echo
   Score: 3.98
   Reasons:
     - genre match (+2.0)
     - mood match (+1.0)
     - energy similarity (+1.0)

2. Gym Hero - Max Pulse
   Score: 2.87
   Reasons:
     - genre match (+2.0)
     - energy similarity (+0.9)

3. Rooftop Lights - Indigo Parade
   Score: 1.96
   Reasons:
     - mood match (+1.0)
     - energy similarity (+1.0)

4. Subway Pulse - Metro Flow
   Score: 0.96
   Reasons:
     - energy similarity (+1.0)

5. Night Drive Loop - Neon Echo
   Score: 0.95
   Reasons:
     - energy similarity (+0.9)
```

---

## Experiments You Tried

No separate scoring experiments are recorded for this version. The command-line example uses a pop, happy profile with a target energy of 0.8, and the scoring weights remain at 2.0 for genre and 1.0 for mood.

---

## Limitations and Risks

The catalog has only 20 sample songs, so it cannot represent the range of real music or listeners. The recommender uses exact genre and mood labels and does not analyze audio, lyrics, listening history, or feedback. Genre has twice the weight of mood, so it can dominate the ranking. The `likes_acoustic`, tempo, valence, danceability, and acousticness fields are not part of the score. As a result, recommendations may be repetitive or miss songs that a person would enjoy for reasons the model does not measure. This is a classroom simulation, not a production recommendation service.

---

## Reflection

The model card describes the system's data, strengths, limitations, and evaluation approach:

[**Model Card**](model_card.md)

This project shows how a recommender turns a few preferences into a ranked list by assigning each song a score. Small choices in the scoring rule matter: genre receives more weight than mood, and exact labels treat similar genres as different. A recommendation can therefore look precise while reflecting only a small part of someone's taste.

The catalog and profile are both simplified. The system cannot learn from listening behavior or explain preferences beyond the three features in its score. In a larger system, missing genres, uneven data, and repeated exposure to similar recommendations could make the results less useful for some listeners. Testing with more songs and different profiles would help show where the scoring rule works and where it needs improvement.

If the assignment requires a personal example, add one specific thing you learned or found surprising; that experience cannot be inferred from the code or tests.


