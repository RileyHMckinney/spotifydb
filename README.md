# 🎵 Music Ranking Social Platform

## Overview
This project is a **social media platform for music listeners** where users can:
- Rank their **top songs, albums, and artists**.
- Follow other users and compare rankings.
- Like and comment on songs, albums, and artists.
- Create and share playlists.

The platform uses the **Spotify API** to fetch and store music data while allowing users to engage with each other.

---

## Features
- **User Rankings**: Users can create and update ranked lists of their favorite songs, albums, or artists.
- **Following System**: Users can follow each other and view rankings from people they follow.
- **Playlists**: Users can create, edit, and share their playlists.
- **Likes & Comments**: Users can like and comment on songs, albums, and artists.
- **Social Feed**: Users see updates when people they follow interact with music.

---

## Tech Stack
- **Backend**: Flask (Python)
- **Frontend**: React (JavaScript)
- **Database**: PostgreSQL (Relational)
- **Cloud Hosting**: AWS (Planned)
- **APIs Used**: Spotify API for music data

---

## Database Schema
The database includes the following **core entities**:

### **Users**
Stores information about registered users.
- `user_id` (Primary Key)
- `username`, `email`, `password_hash`
- `profile_picture_url`, `bio`
- `follower_count`, `following_count`

### **Artists**
Stores artist details fetched from Spotify.
- `artist_id` (Primary Key)
- `spotify_id` (Spotify Reference)
- `name`, `genres`, `popularity`, `image_url`

### **Albums**
Stores album details.
- `album_id` (Primary Key)
- `spotify_id`
- `name`, `release_date`, `total_tracks`, `cover_url`
- `artist_id` (Foreign Key)

### **Tracks**
Stores song details.
- `track_id` (Primary Key)
- `spotify_id`
- `name`, `duration_ms`, `explicit`, `popularity`, `preview_url`
- `album_id` (Foreign Key)
- `artist_id` (Foreign Key)

### **User Rankings**
Tracks user rankings of songs, albums, or artists.
- `ranking_id` (Primary Key)
- `user_id` (Foreign Key)
- `ranking_type` (`song`, `album`, `artist`)
- `ranking_list` (JSON)
- `created_at`, `updated_at`

### **User Follows**
Tracks who follows who.
- `follow_id` (Primary Key)
- `follower_id` (Foreign Key → Users)
- `following_id` (Foreign Key → Users)
- `created_at`

### **User Likes**
Stores likes for songs, albums, and artists.
- `like_id` (Primary Key)
- `user_id` (Foreign Key)
- `entity_type` (`song`, `album`, `artist`)
- `entity_id` (Foreign Key)
- `created_at`

### **User Playlists**
Stores user-created playlists.
- `playlist_id` (Primary Key)
- `user_id` (Foreign Key)
- `name`, `description`
- `is_public`, `created_at`

### **Playlist Tracks**
Links tracks to user playlists.
- `playlist_id` (Foreign Key)
- `track_id` (Foreign Key)
- `order_index`

---

## Installation

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/path/to/your/repo.git
cd path/to/your/repo
```

### **2️⃣ Set Up Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Set Up Database**
```bash
psql -U your_user -d your_database -f schema.sql
```

### **5️⃣ Run the Flask Backend**
```bash
flask run
```

### **6️⃣ Start the React Frontend**
```bash
cd client
npm install
npm start
```

---

## **API Endpoints**
### **Authentication**
- `POST /api/register` → Create a new user
- `POST /api/login` → Authenticate a user

### **User Actions**
- `GET /api/user/:id` → Get user profile
- `POST /api/user/follow` → Follow/unfollow a user
- `GET /api/user/:id/followers` → Get followers
- `GET /api/user/:id/following` → Get following list

### **Rankings**
- `POST /api/ranking` → Create a ranking
- `GET /api/ranking/:user_id` → Get user rankings
- `PUT /api/ranking/:id` → Update ranking

### **Music Data**
- `GET /api/artist/:id` → Get artist details
- `GET /api/album/:id` → Get album details
- `GET /api/track/:id` → Get track details

---

## Future Plans
- **User Discoverability**: Recommend new users to follow based on ranking similarity.
- **Analytics Dashboard**: Show trends on most ranked songs/albums.
- **Mobile App**: Develop a React Native version.

---

## Contributors
- Riley McKinney - Developer

---

## License
This project is licensed under the MIT License.

