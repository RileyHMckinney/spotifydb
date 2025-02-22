-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Rankings Table (Users rate/review songs)
CREATE TABLE IF NOT EXISTS user_rankings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    track_id VARCHAR(255) REFERENCES tracks(id) ON DELETE CASCADE,
    rating INTEGER CHECK (rating BETWEEN 1 AND 10), -- Adjustable range
    review TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, track_id)
);

-- Follow Relationships Table (Users follow each other)
CREATE TABLE IF NOT EXISTS follows (
    id SERIAL PRIMARY KEY,
    follower_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    followed_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (follower_id, followed_id)
);

-- User Tier Lists Table
CREATE TABLE IF NOT EXISTS user_tier_lists (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, name)
);

-- Tier List Songs Table (Tracks in Tier Lists)
CREATE TABLE IF NOT EXISTS tier_list_songs (
    id SERIAL PRIMARY KEY,
    tier_list_id INTEGER REFERENCES user_tier_lists(id) ON DELETE CASCADE,
    track_id VARCHAR(255) REFERENCES tracks(id) ON DELETE CASCADE,
    tier TEXT NOT NULL CHECK (tier IN ('S', 'A', 'B', 'C', 'D', 'F')),
    UNIQUE (tier_list_id, track_id)
);
