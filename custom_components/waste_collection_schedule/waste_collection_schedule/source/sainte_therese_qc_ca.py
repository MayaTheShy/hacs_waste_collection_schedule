import datetime

from waste_collection_schedule import Collection, Icons
from waste_collection_schedule.exceptions import SourceArgumentNotFoundWithSuggestions

TITLE = "Sainte-Thérèse (QC)"
DESCRIPTION = "Source script for Ville de Sainte-Thérèse 4-zone collection schedule"
URL = "https://www.sainte-therese.ca/services/services-aux-citoyens/collectes-et-ecocentre"
COUNTRY = "ca"

SOURCE_CODEOWNERS = ["@MayaTheShy"]

TEST_CASES = {
    "Zone A (default alternating order)": {"zone": "A"},
    "Zone D (garbage first)": {"zone": "D", "first_week_collection": "garbage"},
}

ICON_MAP = {
    "Compost": Icons.ORGANIC,
    "Recyclables": Icons.RECYCLING,
    "Garbage": Icons.GENERAL_WASTE,
}

ZONE_WEEKDAY = {
    "A": 1,  # Tuesday
    "B": 2,  # Wednesday
    "C": 3,  # Thursday
    "D": 4,  # Friday
}

FIRST_WEEK_COLLECTION_VALUES = {
    "recycling": "Recyclables",
    "garbage": "Garbage",
}

PARAM_TRANSLATIONS = {
    "en": {
        "zone": "Zone",
        "first_week_collection": "First alternating collection",
    },
    "fr": {
        "zone": "Zone",
        "first_week_collection": "Première collecte en alternance",
    },
}

PARAM_DESCRIPTIONS = {
    "en": {
        "zone": "Collection zone (A, B, C, or D)",
        "first_week_collection": (
            "Collection type for the first zone day of the year: recycling or garbage"
        ),
    },
    "fr": {
        "zone": "Zone de collecte (A, B, C ou D)",
        "first_week_collection": (
            "Type de collecte pour le premier jour de zone de l'année: recycling ou garbage"
        ),
    },
}

HOW_TO_GET_ARGUMENTS_DESCRIPTION = {
    "en": (
        "Find your zone (A/B/C/D) in the Sainte-Thérèse collection calendar PDF "
        "or with the address search tool on the city page: "
        "https://www.sainte-therese.ca/services/services-aux-citoyens/collectes-et-ecocentre"
    ),
    "fr": (
        "Trouvez votre zone (A/B/C/D) dans le calendrier des collectes de Sainte-Thérèse "
        "ou avec l'outil de recherche par adresse sur la page de la ville : "
        "https://www.sainte-therese.ca/services/services-aux-citoyens/collectes-et-ecocentre"
    ),
}


class Source:
    def __init__(self, zone: str, first_week_collection: str = "recycling"):
        zone_normalized = zone.strip().upper()
        if zone_normalized not in ZONE_WEEKDAY:
            raise SourceArgumentNotFoundWithSuggestions(
                "zone", zone_normalized, list(ZONE_WEEKDAY.keys())
            )

        first_week_collection_normalized = first_week_collection.strip().lower()
        if first_week_collection_normalized not in FIRST_WEEK_COLLECTION_VALUES:
            raise SourceArgumentNotFoundWithSuggestions(
                "first_week_collection",
                first_week_collection,
                list(FIRST_WEEK_COLLECTION_VALUES.keys()),
            )

        self._zone = zone_normalized
        self._first_week_collection = first_week_collection_normalized

    def fetch(self) -> list[Collection]:
        today = datetime.date.today()
        start_year = today.year
        end_year = today.year + 1

        entries = []

        for year in range(start_year, end_year + 1):
            # Brown bin: weekly Monday for all zones
            compost_date = _first_weekday_of_year(year, 0)
            while compost_date.year == year:
                if compost_date >= today:
                    entries.append(
                        Collection(
                            date=compost_date,
                            t="Compost",
                            icon=ICON_MAP["Compost"],
                        )
                    )
                compost_date += datetime.timedelta(days=7)

            # Blue/black bins: weekly on zone day, alternating by week
            zone_weekday = ZONE_WEEKDAY[self._zone]
            zone_date = _first_weekday_of_year(year, zone_weekday)

            first_type = FIRST_WEEK_COLLECTION_VALUES[self._first_week_collection]
            second_type = (
                "Garbage" if first_type == "Recyclables" else "Recyclables"
            )

            collection_types = [first_type, second_type]
            week_index = 0
            while zone_date.year == year:
                if zone_date >= today:
                    collection_type = collection_types[week_index % 2]
                    entries.append(
                        Collection(
                            date=zone_date,
                            t=collection_type,
                            icon=ICON_MAP[collection_type],
                        )
                    )

                zone_date += datetime.timedelta(days=7)
                week_index += 1

        return sorted(entries, key=lambda entry: (entry.date, entry.t))


def _first_weekday_of_year(year: int, weekday: int) -> datetime.date:
    date = datetime.date(year, 1, 1)
    return date + datetime.timedelta(days=(weekday - date.weekday()) % 7)
