"""pyfarm-soil: Substrate composition and amendment scheduling."""

from pyfarm.soil.behavior import SoilBehavior
from pyfarm.soil.calculator import SoilCalculator
from pyfarm.soil.models import (
    AmendmentSchedule,
    AmendmentSpec,
    SoilProfile,
    SubstrateComponent,
    SubstrateComposition,
)

__version__ = "0.1.0"

__all__ = [
    "SubstrateComponent",
    "SubstrateComposition",
    "SoilProfile",
    "AmendmentSpec",
    "AmendmentSchedule",
    "SoilCalculator",
    "SoilBehavior",
]
