"""Data models for soil and substrate."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class SubstrateComponent(str, Enum):
    PERLITE = "perlite"
    COIR = "coir"
    PEAT = "peat"
    VERMICULITE = "vermiculite"
    COMPOST = "compost"
    ROCKWOOL = "rockwool"
    SAND = "sand"
    BARK = "bark"


@dataclass
class SubstrateComposition:
    components: dict[SubstrateComponent, float] = field(default_factory=dict)

    def __post_init__(self):
        total = sum(self.components.values())
        if self.components and abs(total - 1.0) > 0.01:
            raise ValueError(f"Component ratios must sum to 1.0, got {total:.3f}")


@dataclass
class SoilProfile:
    field_capacity: float = 0.35
    wilting_point: float = 0.10
    ph: float = 6.5
    ec_ms_cm: float = 1.5
    bulk_density_g_cm3: float = 0.6

    def __post_init__(self):
        if self.field_capacity <= self.wilting_point:
            raise ValueError("field_capacity must exceed wilting_point")
        if not 0 <= self.ph <= 14:
            raise ValueError("ph must be 0-14")
        if self.ec_ms_cm < 0:
            raise ValueError("ec_ms_cm must be non-negative")


@dataclass
class AmendmentSpec:
    name: str = ""
    dose_g_per_litre: float = 0.0
    notes: str = ""

    def __post_init__(self):
        if self.dose_g_per_litre < 0:
            raise ValueError("dose_g_per_litre must be non-negative")


@dataclass
class AmendmentSchedule:
    amendments: list[AmendmentSpec] = field(default_factory=list)
    frequency_days: int = 7
    notes: str = ""
