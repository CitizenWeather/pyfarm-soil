"""Soil behavior."""

from __future__ import annotations

from pyfarm.crops.registry import CultivarRegistry
from pyfarm.soil.calculator import SoilCalculator
from pyfarm.soil.models import (
    AmendmentSchedule,
    SoilProfile,
    SubstrateComponent,
    SubstrateComposition,
)

_DEFAULT_COMPOSITIONS: dict[str, SubstrateComposition] = {
    "mushroom": SubstrateComposition(components={
        SubstrateComponent.COIR: 0.6,
        SubstrateComponent.PERLITE: 0.2,
        SubstrateComponent.VERMICULITE: 0.2,
    }),
    "microgreen": SubstrateComposition(components={
        SubstrateComponent.COIR: 0.7,
        SubstrateComponent.PERLITE: 0.3,
    }),
    "default": SubstrateComposition(components={
        SubstrateComponent.COIR: 0.5,
        SubstrateComponent.PERLITE: 0.3,
        SubstrateComponent.VERMICULITE: 0.2,
    }),
}


class SoilBehavior:

    def __init__(self, registry: CultivarRegistry):
        self.registry = registry
        self.calculator = SoilCalculator()

    async def recommend_substrate(self, cultivar_id: str) -> SubstrateComposition:
        """Recommend a substrate composition for the given cultivar."""
        cultivar = await self.registry.get_cultivar(cultivar_id)
        if not cultivar:
            raise ValueError(f"Cultivar {cultivar_id} not found")
        key = cultivar.crop_type.value
        return _DEFAULT_COMPOSITIONS.get(key, _DEFAULT_COMPOSITIONS["default"])

    async def amendment_schedule(
        self,
        cultivar_id: str,
        current_profile: SoilProfile,
        stage_index: int,
    ) -> AmendmentSchedule:
        """Compute amendment schedule for current stage."""
        cultivar = await self.registry.get_cultivar(cultivar_id)
        if not cultivar:
            raise ValueError(f"Cultivar {cultivar_id} not found")

        target = SoilProfile(ph=6.5, ec_ms_cm=2.0)
        amendments = self.calculator.amendment_dose(current_profile, target)

        return AmendmentSchedule(
            amendments=amendments,
            frequency_days=7,
            notes=f"Stage {stage_index}",
        )
