from orchestrator.modules.actuators.custom_experiments import custom_experiment
from orchestrator.schema.property import ConstitutiveProperty
from orchestrator.schema.domain import PropertyDomain, VariableTypeEnum

# per-gram ingredient characteristics
INGREDIENTS = {
    "sugar": {
        "kcal": 4.0,
        "sugar": 1.0,       # pure sugar
        "protein": 0.0,
        "fiber": 0.0,       # no fiber
        "fat": 0.0,         # no fat
        "potassium": 0.0,   # negligible
        "cost": 0.005,      # ~0.5 cents per gram
        "allergen": False,  # possible allergen
    },
    "oats": {
        "kcal": 3.9,
        "sugar": 0.01,      # ~1g sugar per 100g
        "protein": 0.13,    # ~13g protein per 100g
        "fiber": 0.11,      # ~11g fiber per 100g
        "fat": 0.07,        # ~7g fat per 100g
        "potassium": 0.36,  # ~360mg per 100g
        "cost": 0.004,      # ~0.4 cents per gram
        "allergen": False,  # possible allergen
    },
    "walnut": {
        "kcal": 6.5,
        "sugar": 0.02,      # ~2g sugar per 100g
        "protein": 0.15,    # ~15g protein per 100g
        "fiber": 0.07,      # ~7g fiber per 100g
        "fat": 0.65,        # ~65g fat per 100g
        "potassium": 0.44,  # ~440mg per 100g
        "cost": 0.02,       # ~2 cents per gram
        "allergen": True,   # possible allergen
    },
    "banana": {
        "kcal": 3.5,
        "sugar": 0.53,      # ~53g sugar per 100g
        "protein": 0.03,    # ~3g protein per 100g
        "fiber": 0.09,      # ~9g fiber per 100g
        "fat": 0.01,        # ~1g fat per 100g
        "potassium": 1.49,  # ~1490mg per 100g (very high!)
        "cost": 0.015,      # ~1.5 cents per gram
        "allergen": False,  # possible allergen
    },
}

# Possible shapes for bar
SHAPES = {
    0: "rectangular",
    1: "cube",
    2: "sphere",
    3: "star",
}


@custom_experiment(
    required_properties=[
        ConstitutiveProperty(
            identifier="sugar",
            propertyDomain=PropertyDomain(
                variableType=VariableTypeEnum.CONTINUOUS_VARIABLE_TYPE,
                domainRange=[0, 15.8]
            )
        ),
        ConstitutiveProperty(
            identifier="oats",
            propertyDomain=PropertyDomain(
                variableType=VariableTypeEnum.CONTINUOUS_VARIABLE_TYPE,
                domainRange=[1.5, 57.2]
            )
        ),
        ConstitutiveProperty(
            identifier="walnut",
            propertyDomain=PropertyDomain(
                variableType=VariableTypeEnum.CONTINUOUS_VARIABLE_TYPE,
                domainRange=[0, 23.1]
            )
        ),
        ConstitutiveProperty(
            identifier="banana",
            propertyDomain=PropertyDomain(
                variableType=VariableTypeEnum.CONTINUOUS_VARIABLE_TYPE,
                domainRange=[0, 34.2]
            )
        ),
        ConstitutiveProperty(
            identifier="shape",
            propertyDomain=PropertyDomain(
                variableType=VariableTypeEnum.DISCRETE_VARIABLE_TYPE,
                domainRange=[0, 3],
                interval=1
            )
        ),
    ],
    output_property_identifiers=[
        "kcal", "sugar", "protein", "fiber", "fat", "potassium", "cost", "allergen", "shape"
    ],
    metadata={'description': 'Get details about a food bar based on makeup.'},
    use_ray=True,
)
def bar_details(sugar: float, oats: float, walnut: float, banana: float, shape: int) -> dict[str, float | bool]:
    """"Get details about food bar based on amount of ingredients used."""
    amounts = {
        "sugar": sugar,
        "oats": oats,
        "walnut": walnut,
        "banana": banana,
    }

    details = {
        "kcal": 0.0,
        "sugar": 0.0,
        "protein": 0.0,
        "fiber": 0.0,
        "fat": 0.0,
        "potassium": 0.0,
        "cost": 0.0,
        "allergen": False,
        "shape": shape,
    }

    for ingredient, grams in amounts.items():
        for dd in details:
            if dd == "shape":
                continue
            if dd == "allergen":
                if grams > 0:
                    # If any allergen is present, this will become True
                    details[dd] |= INGREDIENTS[ingredient][dd]
                continue
            details[dd] += INGREDIENTS[ingredient][dd] * grams

    return details
