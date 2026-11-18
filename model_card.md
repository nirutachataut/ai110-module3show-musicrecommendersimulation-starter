# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**Simple Content-Based Music Recommender**

---

## 2. Intended Use  

This recommender ranks songs in a small catalog for a user who provides a favorite genre, favorite mood, and target energy. It assumes that exact genre and mood matches, along with similar energy levels, are useful signals of music preference. It is intended for classroom exploration, not for real-world users or production use.

---

## 3. How the Model Works  

This content-based recommender compares each song's genre, mood, and energy with the user's preferred genre, mood, and target energy. It gives a song 2.0 points for a matching genre and 1.0 point for a matching mood. It adds energy similarity points using `1.0 - abs(song_energy - target_energy)`, so songs closer to the target energy receive more points.

The system ranks songs from highest to lowest total score and recommends the top K songs. Genre is weighted more heavily than mood, so a genre match can outweigh a mood match. The system also uses only these three features and does not use collaborative filtering, which compares listening patterns across users.

---

## 4. Data  

The `data/songs.csv` file contains 20 sample songs with IDs 1 through 20: the first 10 records plus 10 additional sample records. The catalog includes pop, lofi, rock, ambient, jazz, synthwave, indie pop, reggae, blues, electronic, country, hip-hop, classical, R&B, folk, punk, and metal. Its moods include happy, chill, intense, relaxed, moody, focused, energetic, nostalgic, confident, peaceful, romantic, hopeful, and rebellious. Each row also has energy, tempo, valence, danceability, and acousticness values. The score uses only genre, mood, and energy. These small, example records do not capture the full range of music or musical taste.

---

## 5. Strengths  

The scoring rule clearly rewards the preferences it receives: a genre match is worth 2 points, a mood match is worth 1 point, and energy similarity contributes up to 1 point. This makes its ranking easy to explain. In the included sample profile, a pop song with a happy mood and energy close to 0.8 receives a high score. The current unit tests check that a matching song ranks above a non-matching one and that the explanation includes the score components.

---

## 6. Limitations and Bias 

The catalog is very small and cannot represent all genres, moods, artists, or listeners. Exact label comparisons can miss songs with related but differently named styles. Genre has twice the weight of mood, so it may outweigh a better mood or energy match. Although the data contains tempo, valence, danceability, and acousticness, the score ignores them; `likes_acoustic` is also stored on the profile but unused. The system does not use lyrics, audio analysis, listening history, or user feedback. These choices can make results narrow or repetitive and favor users whose preferences fit the available labels.

---

## 7. Evaluation  

The CLI was run with its built-in pop/happy profile and target energy 0.8; it loaded 20 songs and returned five ranked recommendations with score reasons. The unit tests check ranking, explanation contents, and that a non-positive K returns no recommendations. The final test run completed with **3 passed**. No additional profile comparisons or numeric evaluation metrics are recorded.

---

## 8. Future Work  

Possible next steps are to test more user profiles, add a small set of explicit preferences for features such as acousticness or tempo, and consider genre or mood similarities rather than only exact matches. The top results could also be checked for variety. Any changes should be compared with the current simple scoring rule so their effect is clear.

---

## 9. Personal Reflection  

The notes below describe what the implementation demonstrates, not a personal experience. Add a specific example of what you learned or found surprising if your assignment expects your own perspective.

This project demonstrates that recommendations depend on choices about which features to represent and how much weight to give each one. The score is easy to understand, but it does not represent every reason someone might like a song. A real music app would need broader data and careful evaluation, because repeated or uneven recommendations could limit what listeners discover.
