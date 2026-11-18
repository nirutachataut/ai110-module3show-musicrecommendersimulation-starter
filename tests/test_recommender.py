from src.recommender import Song, UserProfile, Recommender

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    rec.songs.reverse()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    assert results[0].title == "Test Pop Track"
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"
    assert results[1].title == "Chill Lofi Loop"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert "Score: 4.00" in explanation
    assert "genre match (+2.0)" in explanation
    assert "mood match (+1.0)" in explanation
    assert "energy similarity (+1.0)" in explanation


def test_recommend_returns_empty_for_non_positive_k():
    rec = make_small_recommender()

    assert rec.recommend(
        UserProfile("pop", "happy", 0.8, False),
        k=0,
    ) == []
