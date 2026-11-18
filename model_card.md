# Model Card: VibeFinder 1.0

## 1. Model Name

**VibeFinder 1.0** is a beginner-friendly music recommendation simulation.

## 2. Goal / Task

VibeFinder 1.0 recommends songs using a listener's preferred genre, mood, and target energy. It compares those preferences with each song's labels and energy value, then ranks songs that have similar characteristics.

## 3. Data Used

The `data/songs.csv` file contains 20 sample songs. It includes each song's title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness, but the scoring algorithm uses only genre, mood, and energy. The catalog has 17 genres: lofi appears three times, pop twice, and 15 genres once each. This small sample does not cover every style or mood; for example, it has no sad-mood songs.

## 4. Algorithm Summary

An exact genre match adds 2.0 points, and an exact mood match adds 1.0 point. Energy similarity adds up to 1.0 point using `1.0 - abs(song_energy - target_energy)`, so a closer energy match earns more points. The maximum score is 4.0. The system sorts songs from highest to lowest score and returns the top K songs.

## 5. Observed Behavior / Biases

In the original Chill Lofi results, the three lofi songs ranked first, second, and third. Focus Flow (lofi, focused, energy 0.40) ranked above Spacewalk Thoughts (ambient, chill, energy 0.28), showing how the 2-point genre match can outweigh a mood match and closer energy. Gym Hero (pop, intense, energy 0.93) ranked second for High-Energy Pop because it matched pop and had energy close to 0.9, even though its mood did not match happy. Storm Runner ranked first for Conflicting Sad Rock with 2.99 points from its rock match and energy similarity; no song matched the requested sad mood. Repeatedly recommending the same style is a possible filter-bubble risk, but these tests do not show what would happen over repeated use because the system does not track listening history.

## 6. Evaluation Process

The original scoring rule was evaluated by running `python3 -m src.main` against the 20-song CSV. This CLI runs the three requested profiles and two edge cases. Scores use +2.0 for a matching genre, +1.0 for a matching mood, and up to +1.0 for energy similarity. The recommendation scores and reason components below are from that run.

**Profiles and top five recommendations**

- **High-Energy Pop** (`genre=pop`, `mood=happy`, `energy=0.9`)
  1. Sunrise City - Neon Echo — 3.92 (genre +2.0, mood +1.0, energy +0.9)
  2. Gym Hero - Max Pulse — 2.97 (genre +2.0, energy +1.0)
  3. Rooftop Lights - Indigo Parade — 1.86 (mood +1.0, energy +0.9)
  4. Storm Runner - Voltline — 0.99 (energy +1.0)
  5. Silver Lining - Circuit Bloom — 0.99 (energy +1.0)
- **Chill Lofi** (`genre=lofi`, `mood=chill`, `energy=0.2`)
  1. Library Rain - Paper Lanterns — 3.85 (genre +2.0, mood +1.0, energy +0.9)
  2. Midnight Coding - LoRoom — 3.78 (genre +2.0, mood +1.0, energy +0.8)
  3. Focus Flow - LoRoom — 2.80 (genre +2.0, energy +0.8)
  4. Spacewalk Thoughts - Orbit Bloom — 1.92 (mood +1.0, energy +0.9)
  5. Silent Cathedral - Arden Choir — 0.98 (energy +1.0)
- **Deep Intense Rock** (`genre=rock`, `mood=intense`, `energy=0.9`)
  1. Storm Runner - Voltline — 3.99 (genre +2.0, mood +1.0, energy +1.0)
  2. Gym Hero - Max Pulse — 1.97 (mood +1.0, energy +1.0)
  3. Silver Lining - Circuit Bloom — 0.99 (energy +1.0)
  4. Neon Skyline - Nova Static — 0.98 (energy +1.0)
  5. Last Train Riot - Black Circuit — 0.95 (energy +1.0)
- **Conflicting Sad Rock** (`genre=rock`, `mood=sad`, `energy=0.9`)
  1. Storm Runner - Voltline — 2.99 (genre +2.0, energy +1.0)
  2. Silver Lining - Circuit Bloom — 0.99 (energy +1.0)
  3. Neon Skyline - Nova Static — 0.98 (energy +1.0)
  4. Gym Hero - Max Pulse — 0.97 (energy +1.0)
  5. Last Train Riot - Black Circuit — 0.95 (energy +1.0)
- **Unsupported Genre** (`genre=shoegaze`, `mood=chill`, `energy=0.2`)
  1. Spacewalk Thoughts - Orbit Bloom — 1.92 (mood +1.0, energy +0.9)
  2. Library Rain - Paper Lanterns — 1.85 (mood +1.0, energy +0.9)
  3. Midnight Coding - LoRoom — 1.78 (mood +1.0, energy +0.8)
  4. Silent Cathedral - Arden Choir — 0.98 (energy +1.0)
  5. Coffee Shop Stories - Slow Stereo — 0.83 (energy +0.8)

**Pairwise comparisons**

1. **High-Energy Pop vs. Chill Lofi:** Sunrise City leads the pop profile and Library Rain leads the lofi profile. Their top fives share no songs; genre and mood matches plus the different target energies favor different parts of the catalog.
2. **High-Energy Pop vs. Deep Intense Rock:** Sunrise City leads pop and Storm Runner leads rock. Three songs overlap (Gym Hero, Storm Runner, and Silver Lining); Gym Hero ranks second in both lists, receiving a mood match for rock/intense and a genre match for pop/happy.
3. **High-Energy Pop vs. Conflicting Sad Rock:** Sunrise City leads pop and Storm Runner leads sad rock. Storm Runner, Silver Lining, and Gym Hero overlap; no catalog song matches sad, so the sad-rock profile gets no mood-match points.
4. **High-Energy Pop vs. Unsupported Genre:** Sunrise City leads pop and Spacewalk Thoughts leads shoegaze. Their top fives share no songs; the shoegaze request earns no genre points, leaving chill mood and energy to rank the results.
5. **Chill Lofi vs. Deep Intense Rock:** Library Rain leads lofi and Storm Runner leads rock. These top fives share no songs; their target energies (0.2 and 0.9) and exact genre/mood matches differ.
6. **Chill Lofi vs. Conflicting Sad Rock:** Library Rain leads lofi and Storm Runner leads sad rock. These top fives share no songs; the lofi profile has exact genre and chill matches, while no song matches the sad mood.
7. **Chill Lofi vs. Unsupported Genre:** Library Rain leads lofi and Spacewalk Thoughts leads shoegaze. Four songs overlap (Spacewalk Thoughts, Library Rain, Midnight Coding, and Silent Cathedral). Both profiles have chill mood and energy 0.2; the lofi genre match raises Library Rain and Midnight Coding above Spacewalk Thoughts for the supported-genre profile.
8. **Deep Intense Rock vs. Conflicting Sad Rock:** Both rank Storm Runner first and contain the same five songs, but the remaining order changes: Gym Hero is second for intense and fourth for sad; Silver Lining and Neon Skyline move up for sad. The profiles share rock and energy 0.9; the available intense mood match benefits Gym Hero, while no song matches sad.
9. **Deep Intense Rock vs. Unsupported Genre:** Storm Runner leads rock and Spacewalk Thoughts leads shoegaze. Their top fives share no songs; both the genre/mood preferences and target energies differ.
10. **Conflicting Sad Rock vs. Unsupported Genre:** Storm Runner leads sad rock and Spacewalk Thoughts leads shoegaze. Their top fives share no songs; neither requested genre (shoegaze in one profile) nor sad mood is represented, so available matches and energy similarity determine the rankings.

**Surprising results and limitations**

Storm Runner is first for both Deep Intense Rock (3.99) and Conflicting Sad Rock (2.99): the first profile gets genre and mood points, while the latter gets genre points but has no matching sad mood in the catalog. Gym Hero is second for Deep Intense Rock despite being labeled pop, because it matches intense and has energy near the 0.9 target. For Chill Lofi, Focus Flow (lofi, focused, energy 0.40) outranks Spacewalk Thoughts (ambient, chill, energy 0.28) because the genre bonus outweighs Spacewalk Thoughts' mood match and closer energy. The unsupported shoegaze profile receives no genre-match points or warning; it ranks by chill mood and energy instead. These results show exact-match and genre-weight biases in this small catalog, but they do not establish which songs listeners would prefer.

In the earlier weight-shift experiment, genre was reduced from +2.0 to +1.0 and maximum energy similarity increased from +1.0 to +2.0. Only the Chill Lofi top-five order changed: Spacewalk Thoughts moved from fourth to third and Focus Flow from third to fourth. This shows weight changes can affect rankings, not that they improve accuracy. The final implementation retains the original weights.

## 7. Intended Use and Non-Intended Use

VibeFinder 1.0 is intended for beginner-friendly learning about how song features and scoring weights affect recommendations. It is not intended to replace professional streaming recommendation systems or to predict every listener's preferences accurately.

## 8. Ideas for Improvement

- Add more songs and a wider range of genres and moods.
- Use listener feedback to test whether different scoring weights are more useful.
- Explore additional features, such as tempo or valence, if they are useful to users.

## Personal Reflection

During this project, my biggest learning moment was understanding how a simple scoring system can recommend songs based on someone's preferences. Before this project, I didn't realize that comparing features like genre, mood, and energy could make such a difference in recommendations.

Using AI tools helped me understand the code, build the scoring functions, and fix errors. However, I also learned that I needed to double-check the AI's suggestions by running the program and testing the results to make sure everything worked correctly.

What surprised me most was how a simple algorithm could still recommend songs that matched different musical tastes. I also noticed that changing the importance of certain features could affect which songs appeared first.

If I continued working on this project, I would add more songs from different genres, include features like tempo, and allow users to adjust their preferences to get better recommendations.
