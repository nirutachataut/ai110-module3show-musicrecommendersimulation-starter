# 🎵 Music Recommender Simulation

## Project Summary

This project is a small content-based music recommender. It compares songs in a CSV catalog with a user's favorite genre, favorite mood, and target energy. Genre and mood matches earn points, and songs with energy closer to the target earn more points. The program ranks the songs, returns the top five, and explains each score. The catalog contains 20 sample songs.

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

Run the tests with:

```bash
pytest
```

---

## Sample Recommendation Output

Earlier sample output captured with the 20-song catalog and the pop/happy profile at target energy 0.8, before the CLI was expanded to run five profiles:

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

I tested the original weights with five user profiles and also ran a temporary weight-shift experiment. The experiment reduced the genre bonus from +2.0 to +1.0 and increased maximum energy similarity from +1.0 to +2.0, while leaving the mood bonus at +1.0. Only the Chill Lofi top-five order changed: Spacewalk Thoughts moved from fourth to third, and Focus Flow moved from third to fourth; the other four profiles kept their order. After restoring the original weights, all 3 existing tests passed. These runs show that weights affect rankings, but do not prove that the recommendations are more accurate because there are no listener ratings or other ground-truth results.

---

## Limitations and Risks

The catalog has only 20 sample songs, so it cannot represent the range of real music or listeners. The recommender uses exact genre and mood labels and does not analyze audio, lyrics, listening history, or feedback. Genre has twice the weight of mood, so it can dominate the ranking. The `likes_acoustic`, tempo, valence, danceability, and acousticness fields are not part of the score. As a result, recommendations may be repetitive or miss songs that a person would enjoy for reasons the model does not measure. This is a classroom simulation, not a production recommendation service.

---

## Reflection

The model card describes the system's data, strengths, limitations, and evaluation approach:

[**Model Card**](model_card.md)

I learned that music recommendation systems use more than just genre to suggest songs. I found it interesting how mood, energy, and scoring weights can affect which songs get recommended. In this version, genre is worth twice as much as mood, and energy similarity can add another point.

The catalog and profile are simplified. The system cannot learn from listening behavior or explain preferences beyond the three features in its score. Missing genres, uneven data, and repeated exposure to similar recommendations could make results less useful for some listeners.

## Stress Testing with Diverse User Profiles

This evaluation checks how the existing content-based scoring rule behaves for distinct preferences, a conflicting mood/energy combination, and a genre that is not present in the catalog. The scoring weights and logic were not changed: exact genre matches add 2.0 points, exact mood matches add 1.0 point, and energy similarity adds up to 1.0 point.

The five profiles tested were:

1. **High-Energy Pop** — pop, happy, energy 0.9
2. **Chill Lofi** — lofi, chill, energy 0.2
3. **Deep Intense Rock** — rock, intense, energy 0.9
4. **Conflicting Sad Rock** — rock, sad, energy 0.9; the catalog has no sad mood label
5. **Unsupported Genre** — shoegaze, chill, energy 0.2; the catalog has no shoegaze genre

### High-Energy Pop

Top five: Sunrise City, Gym Hero, Rooftop Lights, Storm Runner, and Silver Lining.

```text
=== High-Energy Pop ===
Preferences: {'genre': 'pop', 'mood': 'happy', 'energy': 0.9}
Top 5 recommendations:

1. Sunrise City - Neon Echo
   Score: 3.92
   Reasons:
     - genre match (+2.0)
     - mood match (+1.0)
     - energy similarity (+0.9)

2. Gym Hero - Max Pulse
   Score: 2.97
   Reasons:
     - genre match (+2.0)
     - energy similarity (+1.0)

3. Rooftop Lights - Indigo Parade
   Score: 1.86
   Reasons:
     - mood match (+1.0)
     - energy similarity (+0.9)

4. Storm Runner - Voltline
   Score: 0.99
   Reasons:
     - energy similarity (+1.0)

5. Silver Lining - Circuit Bloom
   Score: 0.99
   Reasons:
     - energy similarity (+1.0)
```

### Chill Lofi

Top five: Library Rain, Midnight Coding, Focus Flow, Spacewalk Thoughts, and Silent Cathedral.

```text
=== Chill Lofi ===
Preferences: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.2}
Top 5 recommendations:

1. Library Rain - Paper Lanterns
   Score: 3.85
   Reasons:
     - genre match (+2.0)
     - mood match (+1.0)
     - energy similarity (+0.9)

2. Midnight Coding - LoRoom
   Score: 3.78
   Reasons:
     - genre match (+2.0)
     - mood match (+1.0)
     - energy similarity (+0.8)

3. Focus Flow - LoRoom
   Score: 2.80
   Reasons:
     - genre match (+2.0)
     - energy similarity (+0.8)

4. Spacewalk Thoughts - Orbit Bloom
   Score: 1.92
   Reasons:
     - mood match (+1.0)
     - energy similarity (+0.9)

5. Silent Cathedral - Arden Choir
   Score: 0.98
   Reasons:
     - energy similarity (+1.0)
```

### Deep Intense Rock

Top five: Storm Runner, Gym Hero, Silver Lining, Neon Skyline, and Last Train Riot.

```text
=== Deep Intense Rock ===
Preferences: {'genre': 'rock', 'mood': 'intense', 'energy': 0.9}
Top 5 recommendations:

1. Storm Runner - Voltline
   Score: 3.99
   Reasons:
     - genre match (+2.0)
     - mood match (+1.0)
     - energy similarity (+1.0)

2. Gym Hero - Max Pulse
   Score: 1.97
   Reasons:
     - mood match (+1.0)
     - energy similarity (+1.0)

3. Silver Lining - Circuit Bloom
   Score: 0.99
   Reasons:
     - energy similarity (+1.0)

4. Neon Skyline - Nova Static
   Score: 0.98
   Reasons:
     - energy similarity (+1.0)

5. Last Train Riot - Black Circuit
   Score: 0.95
   Reasons:
     - energy similarity (+1.0)
```

### Conflicting Sad Rock

Top five: Storm Runner, Silver Lining, Neon Skyline, Gym Hero, and Last Train Riot.

```text
=== Conflicting Sad Rock ===
Preferences: {'genre': 'rock', 'mood': 'sad', 'energy': 0.9}
Top 5 recommendations:

1. Storm Runner - Voltline
   Score: 2.99
   Reasons:
     - genre match (+2.0)
     - energy similarity (+1.0)

2. Silver Lining - Circuit Bloom
   Score: 0.99
   Reasons:
     - energy similarity (+1.0)

3. Neon Skyline - Nova Static
   Score: 0.98
   Reasons:
     - energy similarity (+1.0)

4. Gym Hero - Max Pulse
   Score: 0.97
   Reasons:
     - energy similarity (+1.0)

5. Last Train Riot - Black Circuit
   Score: 0.95
   Reasons:
     - energy similarity (+1.0)
```

### Unsupported Genre

Top five: Spacewalk Thoughts, Library Rain, Midnight Coding, Silent Cathedral, and Coffee Shop Stories.

```text
=== Unsupported Genre ===
Preferences: {'genre': 'shoegaze', 'mood': 'chill', 'energy': 0.2}
Top 5 recommendations:

1. Spacewalk Thoughts - Orbit Bloom
   Score: 1.92
   Reasons:
     - mood match (+1.0)
     - energy similarity (+0.9)

2. Library Rain - Paper Lanterns
   Score: 1.85
   Reasons:
     - mood match (+1.0)
     - energy similarity (+0.9)

3. Midnight Coding - LoRoom
   Score: 1.78
   Reasons:
     - mood match (+1.0)
     - energy similarity (+0.8)

4. Silent Cathedral - Arden Choir
   Score: 0.98
   Reasons:
     - energy similarity (+1.0)

5. Coffee Shop Stories - Slow Stereo
   Score: 0.83
   Reasons:
     - energy similarity (+0.8)
```

### Evaluation

The first three profiles produce generally fitting results: the pop profile starts with two pop songs, the lofi profile ranks lofi/chill songs first, and Storm Runner exactly matches the rock/intense profile. Genre's 2-point weight has a visible effect: Gym Hero, a pop song, is second for Deep Intense Rock because it matches the mood and energy but not the genre, while the genre match gives Storm Runner an additional 2 points. In the lofi profile, mood and genre matches together keep Library Rain and Midnight Coding above non-lofi songs, while small energy differences determine their order.

The sad/high-energy profile cannot satisfy its mood preference because no song is labeled sad. It instead returns a high-energy rock track first because the exact genre match still earns 2 points; the recommendation is not evidence that the system understood sadness. The unsupported shoegaze profile does not error or warn: it falls back to ranking songs using the represented chill mood and energy, making this output look reasonable while silently ignoring the requested genre. Exact-match scoring also treats related but differently named labels as unrelated. Finally, tempo, valence, danceability, acousticness, and the profile's `likes_acoustic` preference do not affect these rankings. These results illustrate the rule's simplicity and limited coverage; they do not justify changing its weights before evaluating the original behavior.

## Step 3: Weight Shift Experiment

I compared the original scores with a temporary weight shift using the same five profiles and the same 20-song dataset. The original weights were genre **+2.0**, mood **+1.0**, and energy similarity up to **+1.0**. The experimental weights were genre **+1.0**, mood **+1.0**, and energy similarity up to **+2.0**, calculated as `2.0 * (1.0 - abs(song_energy - target_energy))`.

All dataset and profile energy values are between 0 and 1, so the experimental energy similarity is between 0 and 2. The maximum possible total is 1 genre point + 1 mood point + 2 energy points = **4.0**. Higher energy similarity means the song's energy is closer to the target, not that the song simply has high energy.

The tables show the actual top five results before and during the experiment. `G`, `M`, and `E` record the genre, mood, and energy contributions shown by the program; a dash means there was no matching genre or mood reason. The reason contributions are rounded to one decimal as in the terminal output, while the total score uses the unrounded energy value.

### High-Energy Pop

| Rank | Original result | Experimental result |
|---|---|---|
| 1 | Sunrise City — 3.92 (G +2.0, M +1.0, E +0.9) | Sunrise City — 3.84 (G +1.0, M +1.0, E +1.8) |
| 2 | Gym Hero — 2.97 (G +2.0, M —, E +1.0) | Gym Hero — 2.94 (G +1.0, M —, E +1.9) |
| 3 | Rooftop Lights — 1.86 (G —, M +1.0, E +0.9) | Rooftop Lights — 2.72 (G —, M +1.0, E +1.7) |
| 4 | Storm Runner — 0.99 (G —, M —, E +1.0) | Storm Runner — 1.98 (G —, M —, E +2.0) |
| 5 | Silver Lining — 0.99 (G —, M —, E +1.0) | Silver Lining — 1.98 (G —, M —, E +2.0) |

### Chill Lofi

| Rank | Original result | Experimental result |
|---|---|---|
| 1 | Library Rain — 3.85 (G +2.0, M +1.0, E +0.9) | Library Rain — 3.70 (G +1.0, M +1.0, E +1.7) |
| 2 | Midnight Coding — 3.78 (G +2.0, M +1.0, E +0.8) | Midnight Coding — 3.56 (G +1.0, M +1.0, E +1.6) |
| 3 | Focus Flow — 2.80 (G +2.0, M —, E +0.8) | Spacewalk Thoughts — 2.84 (G —, M +1.0, E +1.8) |
| 4 | Spacewalk Thoughts — 1.92 (G —, M +1.0, E +0.9) | Focus Flow — 2.60 (G +1.0, M —, E +1.6) |
| 5 | Silent Cathedral — 0.98 (G —, M —, E +1.0) | Silent Cathedral — 1.96 (G —, M —, E +2.0) |

### Deep Intense Rock

| Rank | Original result | Experimental result |
|---|---|---|
| 1 | Storm Runner — 3.99 (G +2.0, M +1.0, E +1.0) | Storm Runner — 3.98 (G +1.0, M +1.0, E +2.0) |
| 2 | Gym Hero — 1.97 (G —, M +1.0, E +1.0) | Gym Hero — 2.94 (G —, M +1.0, E +1.9) |
| 3 | Silver Lining — 0.99 (G —, M —, E +1.0) | Silver Lining — 1.98 (G —, M —, E +2.0) |
| 4 | Neon Skyline — 0.98 (G —, M —, E +1.0) | Neon Skyline — 1.96 (G —, M —, E +2.0) |
| 5 | Last Train Riot — 0.95 (G —, M —, E +1.0) | Last Train Riot — 1.90 (G —, M —, E +1.9) |

### Conflicting Sad Rock

| Rank | Original result | Experimental result |
|---|---|---|
| 1 | Storm Runner — 2.99 (G +2.0, M —, E +1.0) | Storm Runner — 2.98 (G +1.0, M —, E +2.0) |
| 2 | Silver Lining — 0.99 (G —, M —, E +1.0) | Silver Lining — 1.98 (G —, M —, E +2.0) |
| 3 | Neon Skyline — 0.98 (G —, M —, E +1.0) | Neon Skyline — 1.96 (G —, M —, E +2.0) |
| 4 | Gym Hero — 0.97 (G —, M —, E +1.0) | Gym Hero — 1.94 (G —, M —, E +1.9) |
| 5 | Last Train Riot — 0.95 (G —, M —, E +1.0) | Last Train Riot — 1.90 (G —, M —, E +1.9) |

### Unsupported Genre

| Rank | Original result | Experimental result |
|---|---|---|
| 1 | Spacewalk Thoughts — 1.92 (G —, M +1.0, E +0.9) | Spacewalk Thoughts — 2.84 (G —, M +1.0, E +1.8) |
| 2 | Library Rain — 1.85 (G —, M +1.0, E +0.9) | Library Rain — 2.70 (G —, M +1.0, E +1.7) |
| 3 | Midnight Coding — 1.78 (G —, M +1.0, E +0.8) | Midnight Coding — 2.56 (G —, M +1.0, E +1.6) |
| 4 | Silent Cathedral — 0.98 (G —, M —, E +1.0) | Silent Cathedral — 1.96 (G —, M —, E +2.0) |
| 5 | Coffee Shop Stories — 0.83 (G —, M —, E +0.8) | Coffee Shop Stories — 1.66 (G —, M —, E +1.7) |

Only the Chill Lofi ordering changed in the displayed top five: Spacewalk Thoughts moved from fourth to third, ahead of Focus Flow, as its chill mood and closer energy gained more relative influence than Focus Flow's lofi genre match. The other four top-five orders stayed the same, although the scores changed. The experiment made energy differences count more, but it did not automatically make recommendations more accurate. For example, it improved Spacewalk Thoughts' rank for Chill Lofi, while other high-energy matches still appear for profiles where genre or mood does not match.

The experimental `python3 -m pytest` run reported **1 failed, 2 passed**. The failure was the existing explanation test expecting the original `genre match (+2.0)` reason, while the experiment correctly reported `genre match (+1.0)`. After restoring the original scoring weights, `python3 -m pytest` reported **3 passed**. The original scoring algorithm is the final implementation; the temporary experimental weights were not retained.


