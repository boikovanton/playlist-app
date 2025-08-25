"""Seed the Supabase Postgres database with 1000 songs."""

from app import app
from models import db, Song
import random


# ---- Fake data pools ----
ARTISTS = [
    "The Beatles", "Led Zeppelin", "Pink Floyd", "The Rolling Stones",
    "Queen", "Michael Jackson", "Madonna", "Prince", "Taylor Swift",
    "Kendrick Lamar", "Adele", "Beyonce", "Drake", "Coldplay", "U2"
]

WORDS = [
    "Love", "Dream", "Fire", "Moon", "Star", "Sky", "Rain", "Light",
    "Shadow", "Heart", "Dance", "Magic", "Time", "Forever", "World"
]


# ---- Helper functions ----
def make_title(i: int) -> str:
    """Generate a pseudo-random song title using WORDS and index."""
    return f"{random.choice(WORDS)} {random.choice(WORDS)}"


def make_artist(i: int) -> str:
    """Pick a pseudo-random artist name."""
    return random.choice(ARTISTS)


# ---- Main seeding function ----
def main():
    with app.app_context():
        # Sanity check: which DB are we connected to?
        print(f"Connected to host: {db.engine.url.host}")

        added = 0
        for i in range(1000):
            title = make_title(i)
            artist = make_artist(i)

            # Avoid duplicates (title + artist combo)
            exists = Song.query.filter_by(title=title, artist=artist).first()
            if not exists:
                song = Song(title=title, artist=artist)
                db.session.add(song)
                added += 1

        db.session.commit()
        print(f"✅ Seeding complete. Added {added} new songs.")


if __name__ == "__main__":
    main()
