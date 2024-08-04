from typing import NamedTuple

import sys
import ctypes


__all__ = (
    "Range",
    "strtol"
)


if sys.platform.startswith(("linux", "darwin")):
    libc = ctypes.cdll.LoadLibrary("libc.so.6")
elif sys.platform.startswith(("win32", "cygwin")):
    libc = ctypes.cdll.msvcrt
else:
    raise RuntimeError("Unrecognized OS")


class Range(NamedTuple):
    min: int | float
    max: int | float


libc.strtol.argtypes = (ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p))
libc.strtol.restype = ctypes.c_long


def strtol(s: str) -> tuple[int, str]:
    p = ctypes.c_char_p(0)
    s = ctypes.create_string_buffer(s.encode("utf-8"))
    result: int = libc.strtol(s, ctypes.byref(p))
    return result, ctypes.string_at(p).decode("utf-8")