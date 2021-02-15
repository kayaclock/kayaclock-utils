from enum import Enum, IntEnum


# noinspection SpellCheckingInspection
class AgeCategory(Enum):
    PZ = "PZ"
    """Předžáci"""
    ZM = "ZM"
    """Žáci mladší"""
    ZS = "ZS"
    """Žáci starší"""
    DM = "DM"
    """Dorostenci mladší"""
    DS = "DS"
    """Dorostenci starší"""
    U23 = "U23"
    """Do 23 let"""
    D = "D"
    """Dospělí (muži/ženy)"""
    VM = "VM"
    """Veteráni mladší"""
    V = "V"
    """Veteráni"""
    VS = "VS"
    """Veteráni starší"""


class GenderCategory(Enum):
    M = "M"
    """Muž"""
    Z = "Z"
    """Žena"""
    X = "X"  # C2 mix
    """Mix"""
    OTHER = "OTHER"
    """Jiné"""


# noinspection SpellCheckingInspection
class BoatCategory(Enum):
    K1 = "K1"
    """Kajak"""
    C1 = "C1"
    """Kanoe"""
    C2 = "C2"
    """Kanoe dvojic"""
    OTHER = "OTHER"
    """Jiné"""


# noinspection SpellCheckingInspection
class PerformanceRating(Enum):
    MISTR = "M"
    """Mistrovská třída"""
    ONE = "1"
    TWO_PLUS = "2+"
    TWO = "2"
    THREE_PLUS = "3+"
    THREE = "3"
    NONE = "-"


# noinspection SpellCheckingInspection
class Penalisation(IntEnum):
    GOOD = 0
    TOUCH = 2
    MISS = 50


# noinspection SpellCheckingInspection
class MissReason(Enum):
    A = "A"
    """Dotyk na brance bez průjezdu"""
    B = "B"
    """Úmyslné odhození branky"""
    C = "C"
    """Zvrhnutí v brance"""
    D = "D"
    """Průjezd z nesprávné strany"""
    E = "E"
    """Vynechání branky"""
    F = "F"
    """Projel pouze jeden z C2"""
