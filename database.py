import sqlite3

DB_PATH = "maratha.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS players (
            user_id       TEXT PRIMARY KEY,
            username      TEXT,
            hon           INTEGER DEFAULT 500,
            mudra         INTEGER DEFAULT 0,
            medals        INTEGER DEFAULT 0,
            omni_shards   INTEGER DEFAULT 0,
            xp            INTEGER DEFAULT 0,
            level         INTEGER DEFAULT 1,
            selected_char INTEGER DEFAULT NULL,
            last_daily    TEXT DEFAULT NULL,
            last_hourly   TEXT DEFAULT NULL,
            boss_keys     INTEGER DEFAULT 0,
            active_saga   INTEGER DEFAULT NULL,
            created_at    TEXT DEFAULT (datetime('now'))
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS characters (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            rarity      TEXT NOT NULL,
            element     TEXT NOT NULL,
            base_hp     INTEGER DEFAULT 1000,
            base_atk    INTEGER DEFAULT 100,
            base_def    INTEGER DEFAULT 80,
            description TEXT DEFAULT '',
            banner      TEXT DEFAULT 'swarajya',
            move1_name  TEXT DEFAULT 'Strike',
            move1_power INTEGER DEFAULT 100,
            move2_name  TEXT DEFAULT 'Guard Break',
            move2_power INTEGER DEFAULT 80,
            move3_name  TEXT DEFAULT 'Charge',
            move3_power INTEGER DEFAULT 120,
            move4_name  TEXT DEFAULT 'Final Blow',
            move4_power INTEGER DEFAULT 150
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS player_characters (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     TEXT,
            char_id     INTEGER,
            level       INTEGER DEFAULT 1,
            tier        INTEGER DEFAULT 0,
            xp          INTEGER DEFAULT 0,
            is_favorite INTEGER DEFAULT 0,
            obtained_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY(user_id) REFERENCES players(user_id),
            FOREIGN KEY(char_id) REFERENCES characters(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS battle_stats (
            user_id     TEXT PRIMARY KEY,
            pvp_wins    INTEGER DEFAULT 0,
            pvp_losses  INTEGER DEFAULT 0,
            boss_wins   INTEGER DEFAULT 0,
            total_dmg   INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES players(user_id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS bosses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            title       TEXT NOT NULL,
            hp          INTEGER DEFAULT 10000,
            atk         INTEGER DEFAULT 600,
            def         INTEGER DEFAULT 300,
            reward_hon  INTEGER DEFAULT 500,
            reward_xp   INTEGER DEFAULT 200,
            description TEXT DEFAULT '',
            element     TEXT DEFAULT 'Dark'
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS sagas (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            description TEXT DEFAULT '',
            unlock_level INTEGER DEFAULT 1
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS missions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            saga_id     INTEGER NOT NULL,
            mission_num INTEGER NOT NULL,
            name        TEXT NOT NULL,
            enemy_name  TEXT NOT NULL,
            enemy_hp    INTEGER DEFAULT 2000,
            enemy_atk   INTEGER DEFAULT 150,
            enemy_def   INTEGER DEFAULT 100,
            enemy_element TEXT DEFAULT 'Dark',
            reward_hon  INTEGER DEFAULT 100,
            reward_xp   INTEGER DEFAULT 50,
            reward_keys INTEGER DEFAULT 0,
            description TEXT DEFAULT '',
            FOREIGN KEY(saga_id) REFERENCES sagas(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS player_missions (
            user_id     TEXT,
            saga_id     INTEGER,
            mission_num INTEGER,
            completed   INTEGER DEFAULT 0,
            PRIMARY KEY(user_id, saga_id, mission_num)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS tower_attempts (
            user_id     TEXT PRIMARY KEY,
            last_attempt TEXT DEFAULT NULL
        )
    """)

    # Seeds
    c.execute("SELECT COUNT(*) FROM bosses")
    if c.fetchone()[0] == 0:
        seed_bosses(c)

    c.execute("SELECT COUNT(*) FROM characters")
    if c.fetchone()[0] == 0:
        seed_characters(c)

    c.execute("SELECT COUNT(*) FROM sagas")
    if c.fetchone()[0] == 0:
        seed_sagas(c)
        seed_missions(c)

    conn.commit()
    conn.close()
    print("✅ Database initialized.")

def ensure_user(user_id, username):
    """Auto-register a player if they don't exist yet. Call at the top of every command."""
    conn = get_conn()
    conn.execute(
        "INSERT OR IGNORE INTO players (user_id, username) VALUES (?, ?)",
        (str(user_id), username)
    )
    conn.commit()
    conn.close()

def seed_bosses(c):
    bosses = [
        ("Afzal Khan",    "Adilshahi General",    8000,  550, 250, 400, 150, "The treacherous general of Bijapur Sultanate.", "Dark"),
        ("Shaista Khan",  "Mughal Viceroy",        10000, 600, 300, 600, 200, "Aurangzeb's uncle stationed at Pune.", "Dark"),
        ("Aurangzeb",     "Mughal Emperor",        15000, 750, 400, 1000, 350, "The cruel Mughal Emperor who waged war on Marathas for 27 years.", "Dark"),
        ("Siddi Jauhar",  "Adilshahi Admiral",     7000,  500, 280, 350, 130, "The admiral who besieged Panhalgad fort.", "Water"),
        ("Jai Singh I",   "Rajput-Mughal General", 9000,  620, 350, 500, 180, "The Rajput general who forced the Treaty of Purandar.", "Fire"),
    ]
    c.executemany(
        "INSERT INTO bosses (name, title, hp, atk, def, reward_hon, reward_xp, description, element) VALUES (?,?,?,?,?,?,?,?,?)",
        bosses
    )

def seed_sagas(c):
    sagas = [
        (1, "Swarajya Saga",     "Shivaji's rise — from Torna Fort to the founding of the Maratha Empire.", 1),
        (2, "Sinhagad Saga",     "Tanaji Malusare's legendary night assault to reclaim Sinhagad Fort.", 1),
        (3, "Agra Escape Saga",  "Shivaji's daring escape from Aurangzeb's captivity in Agra.", 3),
        (4, "Rajyabhishek Saga", "The grand coronation of Chhatrapati Shivaji Maharaj at Raigad.", 5),
        (5, "Sambhaji Saga",     "Chhatrapati Sambhaji Maharaj's fearless reign and sacrifice.", 8),
        (6, "Peshwa Saga",       "Bajirao I's legendary campaigns — never lost a single battle.", 12),
    ]
    c.executemany(
        "INSERT INTO sagas (id, name, description, unlock_level) VALUES (?,?,?,?)",
        sagas
    )

def seed_missions(c):
    missions = [
        # Saga 1 — Swarajya Saga
        (1,1,"First Strike",        "Bijapur Scout",      800, 80, 60,  "Earth", 80,  40,  0, "Repel the Bijapur scouts near Pune."),
        (1,2,"Torna Fort",          "Fort Guard",         1200,100,80,  "Earth", 100, 50,  0, "Capture Torna Fort — Shivaji's first conquest."),
        (1,3,"Pratapgad Battle",    "Afzal's Soldier",    1800,130,100, "Dark",  150, 70,  0, "Defeat Afzal Khan's advance troops."),
        (1,4,"Killing of Afzal Khan","Afzal Khan (Weakened)",3000,200,130,"Dark",250,100, 1, "Face Afzal Khan himself at Pratapgad!"),

        # Saga 2 — Sinhagad Saga
        (2,1,"Night Infiltration",  "Mughal Sentry",      1000,100,70,  "Dark",  90,  45,  0, "Sneak past Mughal sentries at night."),
        (2,2,"Wall Assault",        "Mughal Archer",      1500,130,90,  "Wind",  120, 60,  0, "Scale the fort walls under arrow fire."),
        (2,3,"Gate Breach",         "Mughal Commander",   2200,170,120, "Earth", 180, 80,  0, "Break through the main gate."),
        (2,4,"Udaybhan Rathod",     "Udaybhan Rathod",    4000,280,180, "Fire",  300, 120, 1, "Face the Rajput commander defending Sinhagad!"),

        # Saga 3 — Agra Escape Saga
        (3,1,"Under Surveillance",  "Mughal Guard",       1500,140,100, "Dark",  130, 65,  0, "Evade Mughal guards in Agra."),
        (3,2,"Sweet Box Ruse",      "Court Soldier",      2000,160,120, "Earth", 160, 75,  0, "Create a diversion using sweet boxes."),
        (3,3,"The Great Escape",    "Mughal Cavalry",     2800,200,150, "Wind",  220, 95,  0, "Outrun Mughal cavalry through enemy territory."),
        (3,4,"Return to Swarajya",  "Aurangzeb's General",5000,320,200, "Dark",  400, 150, 1, "Fight off Aurangzeb's pursuing army!"),

        # Saga 4 — Rajyabhishek Saga
        (4,1,"Raigad Preparation",  "Rival Sardar",       2000,160,120, "Earth", 150, 70,  0, "Quell internal rivalries before the coronation."),
        (4,2,"Coastal Defense",     "Portuguese Soldier", 2500,190,140, "Water", 190, 85,  0, "Repel Portuguese interference from the coast."),
        (4,3,"Coronation Guard",    "Mughal Assassin",    3200,230,160, "Dark",  250, 110, 0, "Stop the Mughal assassination attempt."),
        (4,4,"Jay Shivaji!",        "Jai Singh's Forces", 6000,380,250, "Fire",  500, 200, 1, "Final battle — secure the coronation!"),

        # Saga 5 — Sambhaji Saga
        (5,1,"Sambhaji's Reign",    "Mughal Vanguard",    2500,200,150, "Dark",  200, 90,  0, "Defend Swarajya against Mughal advances."),
        (5,2,"Burhanpur Raid",      "Mughal City Guard",  3000,230,170, "Fire",  240, 110, 0, "Raid Burhanpur deep in Mughal territory."),
        (5,3,"Betrayal at Sangameshwar","Ganoji Shirke",  3800,280,200, "Dark",  300, 130, 0, "Stop the traitor who betrayed Sambhaji."),
        (5,4,"Sambhaji's Defiance", "Mukarrab Khan",      7000,430,280, "Dark",  600, 220, 1, "Sambhaji refuses to bow — fight to the end!"),

        # Saga 6 — Peshwa Saga
        (6,1,"Malwa Campaign",      "Mughal Sardar",      3000,240,180, "Earth", 250, 110, 0, "Bajirao leads the Malwa campaign."),
        (6,2,"Vasai Fort Battle",   "Portuguese General", 3800,280,210, "Water", 300, 140, 0, "Capture Vasai Fort from the Portuguese."),
        (6,3,"Delhi Raid",          "Mughal Imperial Guard",5000,350,250,"Dark", 400, 170, 0, "Bajirao's lightning raid near Delhi gates!"),
        (6,4,"Battle of Bhopal",    "Nizam-ul-Mulk",      8000,500,320, "Wind",  700, 250, 1, "The decisive Battle of Bhopal — Bajirao's masterpiece!"),
    ]
    c.executemany(
        """INSERT INTO missions
           (saga_id,mission_num,name,enemy_name,enemy_hp,enemy_atk,enemy_def,
            enemy_element,reward_hon,reward_xp,reward_keys,description)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
        missions
    )

def seed_characters(c):
    characters = [
        ("Chhatrapati Shivaji Maharaj","L","Fire", 5000,500,400,"The founder of the Maratha Empire. Legendary warrior and strategist.","hindavi",
         "Bhavani Sword Strike",520,"Guerrilla Warfare",400,"Saffron Rage",600,"Jay Shivaji!",750),
        ("Bajirao I",                  "L","Wind", 4500,520,350,"Greatest Peshwa, never lost a battle in his life.","hindavi",
         "Cavalry Charge",500,"Lightning March",420,"Bhopal Slash",580,"Peshwa's Wrath",720),
        ("Chhatrapati Sambhaji Maharaj","L","Dark",4800,490,380,"Fearless son of Shivaji, fought till his last breath.","hindavi",
         "Dark Resolve",480,"Burhanpur Raid",440,"Undying Spirit",560,"Chhatrapati's Fury",700),
        ("Tarabai",                    "L","Light",4200,460,420,"Regent Queen who defied Aurangzeb after Rajaram's death.","hindavi",
         "Queen's Guard",450,"Swarajya's Light",400,"Royal Command",540,"Bhavani's Blessing",680),
        ("Tanaji Malusare",   "E","Fire", 3200,380,300,"The Lion of Sinhagad, sacrificed his life to reclaim the fort.","swarajya",
         "Ghorpad Climb",360,"Night Strike",300,"Sinhagad Charge",420,"Lion's Sacrifice",520),
        ("Murarbaji Deshpande","E","Earth",3000,360,320,"Brave commander who held Purandar fort against the Mughals.","swarajya",
         "Fort Defense",340,"Stone Wall",380,"Counter Strike",400,"Purandar's Stand",500),
        ("Netaji Palkar",     "E","Wind", 2800,370,290,"Senapati of Shivaji's cavalry forces.","swarajya",
         "Wind Slash",350,"Cavalry Rush",310,"Swift Blade",390,"Senapati's Charge",480),
        ("Hambirrao Mohite",  "E","Water",3100,355,310,"Commander-in-chief of Maratha forces under Sambhaji.","swarajya",
         "River Rush",330,"Flood Strike",300,"Konkan Tide",370,"Commander's Wave",460),
        ("Mavla Soldier",    "R","Earth",1800,200,180,"Elite infantry soldier of the Maratha army.","swarajya",
         "Shield Bash",180,"Earth Strike",160,"Fortify",200,"Mavla Rush",240),
        ("Sardar Horseman",  "R","Wind", 1600,220,160,"Swift cavalry of the Maratha forces.","swarajya",
         "Hoof Strike",200,"Wind Dash",180,"Lance Charge",210,"Cavalry Slash",260),
        ("Peshwa Guard",     "R","Fire", 1700,210,170,"Elite guard of the Peshwa court.","swarajya",
         "Guard Strike",190,"Fire Jab",170,"Peshwa's Fist",220,"Blaze Slash",250),
        ("Konkan Scout",     "R","Water",1500,190,190,"Skilled scout from the Konkan coast.","swarajya",
         "Scout Slash",170,"Mist Step",190,"Water Dart",200,"Coastal Strike",230),
        ("Foot Soldier",     "C","Earth",800, 90, 80, "Basic infantry of the Swarajya.","swarajya",
         "Basic Strike",80,"Block",70,"Thrust",90,"War Cry",110),
        ("Village Warrior",  "C","Fire", 750, 95, 75, "Brave villager who joined Shivaji's cause.","swarajya",
         "Torch Swing",85,"Fire Punch",75,"Brave Slash",95,"Village Fury",115),
        ("River Guard",      "C","Water",700, 85, 90, "Guards the river crossings of Maharashtra.","swarajya",
         "River Slash",75,"Splash",80,"Current Strike",85,"Flood Push",105),
        ("Hill Ranger",      "C","Wind", 720,100, 70, "Ranger who knows every path in the Sahyadri hills.","swarajya",
         "Wind Cut",90,"Quick Step",70,"Hill Charge",100,"Sahyadri Gust",120),
    ]
    c.executemany(
        """INSERT INTO characters
           (name,rarity,element,base_hp,base_atk,base_def,description,banner,
            move1_name,move1_power,move2_name,move2_power,
            move3_name,move3_power,move4_name,move4_power)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        characters
    )
