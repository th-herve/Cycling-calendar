from dataclasses import dataclass

@dataclass
class event:
    id: int
    season_id: int
    name: str
    single_event: bool
    scheduled: str
    scheduled_end: str
    departure_city: str
    arrival_city: str
    distance: int
    classification_id: int
    type_id: int

@dataclass
class stage:
    main_event_id: int
    stage_id: int

@dataclass
class season:
    id: int
    year: str
    gender_id: int


@dataclass
class competitor:
    id: int
    team_id: int
    last_name: str
    first_name: str
    age: int
    nationality: str
    gender_id: int


@dataclass
class team:
    id: int
    name: int

@dataclass
class classification:
    id: int
    name: int

@dataclass
class type:
    id: int
    name: int

@dataclass
class gender:
    id: int
    name: int
