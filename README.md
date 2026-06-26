# 🚩 Swarajya Bot — Maratha Empire Discord RPG

A Dragon Ball OV-inspired Discord RPG bot with Maratha Empire theme.

## Phase 1 Features

| Command | Description |
|---|---|
| `!start` | Begin your Swarajya journey |
| `!profile` / `!pf` | View your Sardar profile with rank, level, XP, currencies |
| `!bal` | Check Hon, Mudra, Medals, Omni Shards |
| `!daily` | Claim 500 Hon daily reward |
| `!roll` | Claim 100 Hon hourly chest |
| `!leaderboard` / `!lb` | Top 10 richest players |
| `!summon [1/2]` | Summon a warrior (300 Hon) |
| `!multi [1/2]` | 10x summon (2700 Hon) |
| `!banner` | View summon banners |
| `!chars [page]` | Paginated warrior inventory |
| `!gallery [page]` | Browse all warriors |
| `!info <ID>` | Detailed warrior info with scaled stats |
| `!select <ID>` | Equip a warrior |
| `!fav <ID>` | Favourite/unfavourite a warrior |
| `!favs` | View favourite warriors |

## Characters (16 seeded)

| Rarity | Warriors |
|---|---|
| 🟡 Legendary | Shivaji Maharaj, Bajirao I, Sambhaji Maharaj, Tarabai |
| 🟣 Epic | Tanaji Malusare, Murarbaji, Netaji Palkar, Hambirrao |
| 🔵 Rare | Mavla Soldier, Sardar Horseman, Peshwa Guard, Konkan Scout |
| ⚪ Common | Foot Soldier, Village Warrior, River Guard, Hill Ranger |

## Setup

1. Get your bot token from https://discord.com/developers/applications
2. Enable **Message Content Intent**
3. Add your token to `.env`
4. Run:

```bash
pip install -r requirements.txt
python main.py
```

## Project Structure

```
maratha_bot/
├── main.py          # Bot entry point
├── database.py      # SQLite DB setup & seeding
├── config.py        # Rarities, rates, economy constants
├── requirements.txt
├── .env
├── maratha.db       # Auto-created on first run
└── cogs/
    ├── general.py   # start, profile, bal, daily, roll, leaderboard
    └── characters.py # summon, multi, chars, gallery, info, select, fav
```

## Coming Next (Phase 2)

- `!fight @user` — PvP battles
- `!boss <name>` — Fight Mughal bosses (Afzal Khan, Aurangzeb, etc.)
- `!mohim` — Story missions
- `!gadkille` — Tower challenge
- `!sangam` — Fuse warriors
- `!clan` — Create/join clans
- `!market` — Player marketplace
- `!trade @user` — Direct trades
