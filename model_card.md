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

The original system was tested with High-Energy Pop (`pop`, `happy`, 0.9), Chill Lofi (`lofi`, `chill`, 0.2), Deep Intense Rock (`rock`, `intense`, 0.9), Conflicting Sad Rock (`rock`, `sad`, 0.9), and Unsupported Genre (`shoegaze`, `chill`, 0.2). Their top songs were Sunrise City, Library Rain, Storm Runner, Storm Runner, and Spacewalk Thoughts, respectively. A separate weight-shift experiment changed genre from +2.0 to +1.0 and energy similarity from up to +1.0 to up to +2.0, while leaving mood at +1.0. Only the Chill Lofi top-five order changed: Spacewalk Thoughts moved from fourth to third, and Focus Flow moved from third to fourth; the other four profiles kept their order. After restoring the original weights, all 3 existing tests passed. These comparisons show how weights affect rankings, but do not prove which recommendations listeners would prefer.

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
