from enum import Flag, auto


__all__ = (
    "Qualification",
)


class Qualification(Flag):
    NONE = 0
    DIPLOMA = auto()
    DEGREE = auto()

    def __str__(self) -> str:
        qual = []

        if self & self.DIPLOMA:
            qual.append("Diploma")
        if self & self.DEGREE:
            qual.append("Degree")

        return " & ".join(qual)

