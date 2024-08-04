from enum import Enum


__all__ = (
    "States",
)


class States(Enum):
    ALL = ""
    JOHOR = 1
    KEDAH = 2
    KELANTAN = 3
    MELAKA = 4
    NEGERI_SEMBILAN = 5
    PAHANG = 6
    PERAK = 7
    PERLIS = 8
    PULAU_PINANG = 9
    SELANGOR = 10
    TERENGGANU = 11
    KUALA_LUMPUR = 12
    PUTRAJAYA = 13
    SARAWAK = 14
    SABAH = 15
    LABUAN = 16
    SINGAPORE = 17
    CHINA = 18

    def __str__(self) -> str:
        return self.name\
            .replace("_", " ")\
            .capitalize()
