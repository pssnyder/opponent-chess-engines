# 🏆 Engine Tournament Manager

**RTS Labs Chess Tournament System**  
*Continuous automated chess engine tournament on Firebase/GCP*

---

## 📋 Project Overview

An automated chess engine tournament system that runs continuously in the cloud, hosting UCI-compliant Python chess engines in non-stop round-robin tournaments. Part of the **RTS Labs** experimental application portfolio.

### Key Features

- **24/7 Automated Tournaments**: Continuous round-robin matches between chess engines
- **Live Game Viewer**: Real-time chess board display with customizable piece sets
- **ELO Rating System**: Fair engine comparison independent of play time
- **Admin Panel**: Upload and manage engines via Google Authentication
- **Multi-tenant Architecture**: Designed as a sub-project of the RTS Labs platform
- **Cost-efficient Cloud Infrastructure**: Optimized for long-running games on GCP

---

## 🏗️ Architecture

### Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | Cloud Run (Python) | Tournament manager & game coordinator |
| **Frontend** | Firebase Hosting | Live game viewer & admin panel |
| **Database** | Firestore | Engine metadata, game state, ELO ratings |
| **Storage** | Cloud Storage | Engine Python files |
| **Authentication** | Firebase Auth | Google Sign-In for admin panel |
| **Game Engine** | python-chess | UCI protocol implementation |

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Firebase Project                          │
│                   rts-labs-f3981                             │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────────┐    ┌─────────────┐
│   Firebase   │    │   Cloud Storage  │    │  Firestore  │
│   Hosting    │    │                  │    │             │
│              │    │  Engine Python   │    │ chess_*     │
│ - Viewer     │    │  Files (.py)     │    │ collections │
│ - Admin UI   │    │                  │    │             │
└──────┬───────┘    └────────┬─────────┘    └──────┬──────┘
       │                     │                      │
       │                     │                      │
       └─────────────────────┼──────────────────────┘
                             │
                             ▼
                    ┌────────────────────┐
                    │    Cloud Run       │
                    │                    │
                    │ Tournament Manager │
                    │ - Game Runner      │
                    │ - ELO Calculator   │
                    │ - Engine Loader    │
                    │ - Scheduler        │
                    └────────────────────┘
```

---

## 🎮 Tournament System

### Match Formats

**Standard Matches** (Random selection):
- **1+1**: Bullet (1 minute + 1 second increment)
- **3+2**: Blitz (3 minutes + 2 second increment)
- **5+5**: Rapid (5 minutes + 5 second increment)
- **10+1**: Classical-lite (10 minutes + 1 second increment)

**Daily Classical Tournament**:
- **30+1**: Classical (30 minutes + 1 second increment)
- **Format**: 3-game match between the two closest-rated engines
- **Schedule**: Once per day at scheduled time

### Tournament Structure

- **Format**: Round-robin (all engines play each other)
- **Continuous Operation**: Matches run 24/7
- **Live Display**: One game shown on frontend at a time
- **Time Controls**: Randomly selected from predefined formats

### ELO Rating System

Engines are ranked using standard ELO rating calculations:
- **Fair Comparison**: Independent of total games played
- **Initial Estimates**:
  - `MaterialOpponent_v1.0`: ~1200-1400 ELO (tested against rated engines)
  - `RandomOpponent_v1.0`: ~100-400 ELO (baseline random moves)
- **Dynamic Updates**: Ratings adjust after each completed game

---

## 📁 Project Structure

```
engine-tournament-manager/
├── README.md                       # This file
├── engines/                        # Local engine copies
│   ├── CaptureOpponent_v1.0/
│   ├── CoverageOpponent_v1.0/
│   ├── MaterialOpponent_v1.0/
│   ├── PositionalOpponent_v1.0/
│   └── RandomOpponent_v1.0/
│
├── frontend/                       # Firebase Hosting site
│   ├── public/
│   │   ├── index.html             # Live game viewer
│   │   ├── admin.html             # Admin panel
│   │   ├── js/
│   │   │   ├── chess-board.js     # Board rendering
│   │   │   ├── firebase-config.js # Firebase SDK setup
│   │   │   └── admin-panel.js     # Engine management
│   │   ├── css/
│   │   │   └── styles.css         # RTS brand styling
│   │   └── images/
│   │       └── pieces/            # PNG chess piece sets
│   └── firebase.json
│
├── backend/                        # Cloud Run container
│   ├── main.py                    # FastAPI server + tournament loop
│   ├── tournament_manager.py      # Round-robin coordinator
│   ├── engine_loader.py           # Load engines from Cloud Storage
│   ├── game_runner.py             # UCI game execution
│   ├── elo_system.py              # ELO rating calculator
│   ├── scheduler.py               # Daily classical match scheduler
│   ├── requirements.txt           # Python dependencies
│   └── Dockerfile                 # Container definition
│
├── infrastructure/                 # Deployment & configuration
│   ├── deploy.sh                  # Deployment automation
│   ├── firestore.rules            # Database security rules
│   ├── storage.rules              # Storage bucket rules
│   └── cloudbuild.yaml            # CI/CD configuration
│
└── docs/
    ├── ARCHITECTURE.md            # Detailed architecture
    ├── DEPLOYMENT.md              # Deployment instructions
    └── API.md                     # Backend API documentation
```

---

## 🎨 Frontend Design

### RTS Brand Styling

Following **RTS Technology & Solutions** brand guidelines:

**Public-Facing Colors**:
- Primary: RTS Deep Blue (`#0A1628`)
- Accent: RTS Bright Cyan (`#00D4FF`)
- Success: RTS Success Green (`#00FF88`)
- Background: RTS Light Gray (`#F8FAFC`)
- Text: RTS Professional Gray (`#6B7280`)

**Typography**:
- Primary: Inter (clean, professional)
- Technical: JetBrains Mono (code, data)

### Chess Board Features

- **Customizable Piece Sets**: PNG images easily swappable
- **Customizable Board Colors**: Light/dark square color selection
- **Live Move Updates**: Real-time game state from Firestore
- **Move History**: PGN notation display
- **Game Info**: Current players, time controls, ELO ratings

### Scoreboard Display

- **ELO Rankings**: Sorted list of all engines
- **Recent Results**: Latest game outcomes
- **Head-to-Head Stats**: Win/loss/draw records between engines
- **Performance Trends**: ELO rating graphs over time

---

## 🔒 Firestore Collections

All collections use `chess_` prefix for multi-tenant namespace separation:

### `chess_engines`
```javascript
{
  engineId: "material_opponent_v1_0",
  name: "MaterialOpponent v1.0",
  version: "1.0",
  description: "Material evaluation focused engine",
  elo: 1350,
  gamesPlayed: 247,
  wins: 142,
  losses: 89,
  draws: 16,
  uploadedAt: timestamp,
  active: true,
  storageUrl: "gs://bucket/engines/material_opponent.py"
}
```

### `chess_games`
```javascript
{
  gameId: "game_20251103_001",
  whiteEngineId: "material_opponent_v1_0",
  blackEngineId: "random_opponent_v1_0",
  timeControl: "3+2",
  status: "in_progress", // in_progress, completed, error
  currentFen: "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
  pgn: "1. e4 e5 2. Nf3...",
  moveHistory: ["e2e4", "e7e5", "g1f3"],
  result: null, // "1-0", "0-1", "1/2-1/2"
  startTime: timestamp,
  endTime: null,
  whiteTimeRemaining: 180,
  blackTimeRemaining: 180
}
```

### `chess_tournaments`
```javascript
{
  tournamentId: "roundrobin_20251103",
  type: "round_robin", // round_robin, classical_daily
  status: "active",
  startTime: timestamp,
  endTime: null,
  participants: ["engine_id_1", "engine_id_2", ...],
  games: ["game_id_1", "game_id_2", ...],
  standings: {
    "engine_id_1": { wins: 5, losses: 2, draws: 1, elo: 1400 }
  }
}
```

### `chess_config`
```javascript
{
  configId: "system",
  timeControls: ["1+1", "3+2", "5+5", "10+1"],
  classicalSchedule: "00:00 UTC",
  classicalTimeControl: "30+1",
  minEngines: 2,
  tournamentCycleMinutes: 30
}
```

---

## 🚀 Deployment

### Prerequisites

- Google Cloud Project: `rts-labs-f3981`
- Firebase project initialized
- gcloud CLI authenticated
- Firebase CLI installed

### Initial Setup

```bash
# Authenticate with Google Cloud
gcloud auth login
gcloud config set project rts-labs-f3981

# Initialize Firebase
firebase login
firebase use rts-labs-f3981

# Create Cloud Storage bucket
gsutil mb gs://rts-labs-chess-engines

# Deploy Firestore indexes and rules
firebase deploy --only firestore

# Build and deploy Cloud Run container
cd backend
gcloud builds submit --tag gcr.io/rts-labs-f3981/chess-tournament-manager
gcloud run deploy chess-tournament-manager \
  --image gcr.io/rts-labs-f3981/chess-tournament-manager \
  --platform managed \
  --region us-central1 \
  --min-instances 1 \
  --memory 1Gi \
  --allow-unauthenticated

# Deploy frontend
cd ../frontend
firebase deploy --only hosting
```

### Cost Estimates

- **Cloud Run** (always-on, 1 instance): ~$15-30/month
- **Firestore** (reads/writes): ~$5-10/month
- **Cloud Storage**: <$1/month
- **Firebase Hosting**: Free tier sufficient
- **Total**: ~$20-40/month for continuous operation

---

## 🔮 Future Enhancements

### Phase 2: Human Challenges
- Authenticate via Chess.com or Lichess OAuth
- Pull verified player ratings
- Allow rated players to challenge engines
- Track human vs engine results

### Phase 3: Multi-Project Expansion
- Additional RTS Labs experimental projects
- Shared authentication across sub-projects
- Unified navigation for labs platform

### Phase 4: Advanced Features
- Concurrent game display (multiple boards)
- Engine analytics dashboard
- Custom opening book integration
- Live commentary generation (AI analysis)
- Twitch/YouTube streaming integration

---

## 📊 Current Engines

| Engine Name | Version | Estimated ELO | Strategy |
|-------------|---------|---------------|----------|
| RandomOpponent | v1.0 | 100-400 | Random legal moves |
| MaterialOpponent | v1.0 | 1200-1400 | Material evaluation (tested) |
| CaptureOpponent | v1.0 | TBD | Capture prioritization |
| CoverageOpponent | v1.0 | TBD | Board coverage focus |
| PositionalOpponent | v1.0 | TBD | Positional evaluation |

*Accurate ELO ratings will be established through tournament play*

---

## 🤝 Contributing

This is an experimental project under **RTS Technology & Solutions**. Engines are developed separately in the parent repository's `build/` directory and copied here for deployment.

### Adding New Engines

1. Develop engine in `opponent-chess-engines/build/`
2. Ensure UCI compliance
3. Copy to `engine-tournament-manager/engines/`
4. Upload via admin panel or manually to Cloud Storage
5. System auto-detects and adds to tournament rotation

---

## 📄 License

Part of the RTS Technology & Solutions portfolio.  
**Company**: RTS Technology & Solutions LLC  
**Purpose**: Educational demonstration and portfolio showcase  
**Contact**: [RTS Website](https://rapidtechconsultants.com)

---

## 🔗 Related Projects

- **Parent Repository**: opponent-chess-engines (engine development)
- **RTS Labs Platform**: rts-labs-f3981 (multi-project host)
- **RTS Website**: rapidtechconsultants.com (main company site)

---

**Last Updated**: November 3, 2025  
**Status**: Architecture Complete - Implementation In Progress  
**Firebase Project**: rts-labs-f3981  
**Maintainer**: RTS Technology & Solutions
