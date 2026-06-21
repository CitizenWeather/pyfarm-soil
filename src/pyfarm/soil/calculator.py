"""Soil and substrate calculations."""

from __future__ import annotations

from pyfarm.soil.models import (
    AmendmentSpec,
    SoilProfile,
    SubstrateComponent,
    SubstrateComposition,
)


class SoilCalculator:

    @staticmethod
    def water_retention(composition: SubstrateComposition) -> SoilProfile:
        """Estimate field capacity and wilting point from substrate composition."""
        fc = 0.25
        wp = 0.08

        r = composition.components
        fc += r.get(SubstrateComponent.COIR, 0) * 0.20
        fc += r.get(SubstrateComponent.PEAT, 0) * 0.18
        fc += r.get(SubstrateComponent.VERMICULITE, 0) * 0.15
        fc -= r.get(SubstrateComponent.PERLITE, 0) * 0.10
        fc -= r.get(SubstrateComponent.SAND, 0) * 0.12

        wp += r.get(SubstrateComponent.COIR, 0) * 0.05
        wp += r.get(SubstrateComponent.PEAT, 0) * 0.06

        return SoilProfile(
            field_capacity=max(0.15, min(0.70, fc)),
            wilting_point=max(0.05, min(0.25, wp)),
        )

    @staticmethod
    def nutrient_availability_factor(ph: float) -> float:
        """Return a 0-1 factor reflecting nutrient availability at given pH."""
        if 6.0 <= ph <= 7.0:
            return 1.0
        if ph < 5.0 or ph > 8.5:
            return 0.3
        if ph < 6.0:
            return 0.5 + (ph - 5.0) * 0.5
        return max(0.3, 1.0 - (ph - 7.0) * 0.4)

    @staticmethod
    def amendment_dose(
        profile: SoilProfile,
        target: SoilProfile,
    ) -> list[AmendmentSpec]:
        """Suggest amendments to move profile toward target."""
        specs: list[AmendmentSpec] = []

        ph_delta = target.ph - profile.ph
        if abs(ph_delta) > 0.3:
            if ph_delta > 0:
                specs.append(AmendmentSpec(
                    name="garden_lime",
                    dose_g_per_litre=ph_delta * 2.0,
                    notes="Raise pH with ground limestone",
                ))
            else:
                specs.append(AmendmentSpec(
                    name="elemental_sulfur",
                    dose_g_per_litre=abs(ph_delta) * 1.5,
                    notes="Lower pH with elemental sulfur",
                ))

        ec_delta = target.ec_ms_cm - profile.ec_ms_cm
        if ec_delta > 0.5:
            specs.append(AmendmentSpec(
                name="base_nutrient",
                dose_g_per_litre=ec_delta * 0.5,
                notes="Increase EC with balanced base nutrient",
            ))

        return specs
