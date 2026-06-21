"""Smoke tests for pyfarm-soil."""

import pytest

from pyfarm.crops import MemoryRegistry
from pyfarm.soil import (
    SoilBehavior,
    SoilCalculator,
    SoilProfile,
    SubstrateComponent,
    SubstrateComposition,
    AmendmentSpec,
    AmendmentSchedule,
)


def test_substrate_composition_valid():
    c = SubstrateComposition(components={
        SubstrateComponent.COIR: 0.7,
        SubstrateComponent.PERLITE: 0.3,
    })
    assert abs(sum(c.components.values()) - 1.0) < 0.01


def test_substrate_composition_invalid():
    with pytest.raises(ValueError):
        SubstrateComposition(components={
            SubstrateComponent.COIR: 0.5,
            SubstrateComponent.PERLITE: 0.3,
        })


def test_soil_profile_validation():
    with pytest.raises(ValueError):
        SoilProfile(field_capacity=0.1, wilting_point=0.2)
    with pytest.raises(ValueError):
        SoilProfile(ph=15)


def test_water_retention():
    comp = SubstrateComposition(components={
        SubstrateComponent.COIR: 0.6,
        SubstrateComponent.PERLITE: 0.4,
    })
    profile = SoilCalculator.water_retention(comp)
    assert profile.field_capacity > profile.wilting_point


def test_nutrient_availability():
    assert SoilCalculator.nutrient_availability_factor(6.5) == 1.0
    assert SoilCalculator.nutrient_availability_factor(4.5) == 0.3
    assert SoilCalculator.nutrient_availability_factor(9.0) == 0.3


def test_amendment_dose_low_ph():
    current = SoilProfile(ph=5.5, ec_ms_cm=1.5)
    target = SoilProfile(ph=6.5, ec_ms_cm=1.5)
    specs = SoilCalculator.amendment_dose(current, target)
    assert any(s.name == "garden_lime" for s in specs)


@pytest.mark.asyncio
async def test_recommend_substrate():
    registry = MemoryRegistry()
    behavior = SoilBehavior(registry)
    comp = await behavior.recommend_substrate("oyster-grey-strain-a")
    assert isinstance(comp, SubstrateComposition)


@pytest.mark.asyncio
async def test_amendment_schedule():
    registry = MemoryRegistry()
    behavior = SoilBehavior(registry)
    profile = SoilProfile(ph=5.8, ec_ms_cm=1.0)
    schedule = await behavior.amendment_schedule("oyster-grey-strain-a", profile, 0)
    assert isinstance(schedule, AmendmentSchedule)


@pytest.mark.asyncio
async def test_missing_cultivar():
    registry = MemoryRegistry()
    behavior = SoilBehavior(registry)
    with pytest.raises(ValueError):
        await behavior.recommend_substrate("nonexistent")
