CREATE TABLE event (
    id INTEGER PRIMARY KEY,
    season_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    single_event INTEGER NOT NULL CHECK(single_event <= 1),
    scheduled TEXT,
    scheduled_end Text,
    departure_city Text,
    arrival_city Text,
    distance INTEGER,
    classification_id id,
    type_id id,

    FOREIGN KEY (season_id) REFERENCES season(id),
    FOREIGN KEY (classification_id) REFERENCES classification(id),
    FOREIGN KEY (type_id) REFERENCES type(id)
);

-- TODO Implement stronger checks for this table (with a trigger)
-- event.id can only reference either as main_event_id or stage_id
CREATE TABLE stage (
    main_event_id INTEGER PRIMARY KEY,
    stage_id INTEGER NOT NULL UNIQUE check(stage_id != main_event_id),

    FOREIGN KEY (main_event_id) REFERENCES event(id),
    FOREIGN KEY (stage_id) REFERENCES event(id)
);

CREATE TABLE season (
    id INTEGER PRIMARY KEY,
    year TEXT NOT NULL CHECK(length(year) = 4),
    gender_id INTEGER,

    FOREIGN KEY(gender_id) REFERENCES gender(id)
);

create TABLE competitor (
    id INTEGER primary key,
    team_id INTEGER, 
    last_name TEXT NOT NULL,
    first_name TEXT NOT NULL,
    age INTEGER,
    nationality TEXT,
    gender_id INTEGER,

    FOREIGN KEY(team_id) REFERENCES team(id),
    FOREIGN KEY(gender_id) REFERENCES gender(id)
);

CREATE TABLE team (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE classification (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE type (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

create TABLE gender (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL CHECK (name IN ('man', 'woman'))
);

