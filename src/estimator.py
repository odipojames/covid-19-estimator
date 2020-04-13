import math


def float_rep(x):
    """rep float to human readablbe"""
    num = "%1.9f" % x
    return num


def estimator(data):
    results = {}
    impact = {}
    severeImpact = {}
    impact["currentlyInfected"] = float_rep(data["reportedCases"] * 10)
    severeImpact["currentlyInfected"] = float_rep(data["reportedCases"] * 50)

    if data["periodType"].lower() == "days":

        impact["infectionsByRequestedTime"] = float_rep(
            math.ceil(
                float(impact["currentlyInfected"]) * 2 ** (data["timeToElapse"] / 3)
            )
        )
        severeImpact["infectionsByRequestedTime"] = float_rep(
            math.ceil(
                float(impact["currentlyInfected"]) * 2 ** (data["timeToElapse"] / 3)
            )
        )

    if data["periodType"].lower() == "weeks":
        impact["infectionsByRequestedTime"] = float_rep(
            math.ceil(
                float(impact["currentlyInfected"]) * 2 ** (data["timeToElapse"] * 7 / 3)
            )
        )
        severeImpact["infectionsByRequestedTime"] = float_rep(
            math.ceil(
                float(impact["currentlyInfected"]) * 2 ** (data["timeToElapse"] * 7 / 3)
            )
        )

    if data["periodType"].lower() == "months":
        impact["infectionsByRequestedTime"] = float_rep(
            math.ceil(
                float(impact["currentlyInfected"])
                * 2 ** (data["timeToElapse"] * 30 / 3)
            )
        )

        severeImpact["infectionsByRequestedTime"] = float_rep(
            math.ceil(
                float(severeImpact["currentlyInfected"])
                * 2 ** (data["timeToElapse"] * 30 / 3)
            )
        )

    impact["severeCasesByRequestedTime"] = float_re(
        math.ceil(float(impact["infectionsByRequestedTime"]) * 0.15)
    )
    severeImpact["severeCasesByRequestedTime"] = float_rep(
        math.ceil(float(severeImpact["infectionsByRequestedTime"]) * 0.15)
    )

    impact["hospitalBedsByRequestedTime"] = float_rep(
        math.ceil(
            float(data["totalHospitalBeds"]) * 0.35
            - float(impact["severeCasesByRequestedTime"])
        )
    )

    severeImpact["hospitalBedsByRequestedTime"] = float_rep(
        math.ceil(
            float(data["totalHospitalBeds"]) * 0.35
            - floa(severeImpact["severeCasesByRequestedTime"])
        )
    )

    impact["casesForICUByRequestedTime"] = float_rep(
        math.ceil(float(impact["infectionsByRequestedTime"]) * 0.5)
    )
    severeImpact["casesForICUByRequestedTime"] = float_rep(
        math.ceil(float(severeImpact["infectionsByRequestedTime"]) * 0.5)
    )

    impact["casesForVentilatorsByRequestedTime"] = float_rep(
        math.ceil(float(impact["infectionsByRequestedTime"]) * 0.2)
    )
    severeImpact["casesForVentilatorsByRequestedTime"] = float_rep(
        math.ceil(float(severeImpact["infectionsByRequestedTime"]) * 0.2)
    )

    region_data = data.pop("region")
    if data["periodType"].lower() == "days":
        impact["dollarsInFlight"] = float_rep(
            math.ceil(
                float(impact["infectionsByRequestedTime"])
                * region_data["avgDailyIncomePopulation"]
                * region_data["avgDailyIncomeInUSD"]
                * data["timeToElapse"]
            )
        )

        severeImpact["dollarsInFlight"] = float_rep(
            math.ceil(
                float(severeImpact["infectionsByRequestedTime"])
                * region_data["avgDailyIncomePopulation"]
                * region_data["avgDailyIncomeInUSD"]
                * data["timeToElapse"]
            )
        )
    if data["periodType"].lower() == "weeks":
        impact["dollarsInFlight"] = float_rep(
            math.ceil(
                float(impact["infectionsByRequestedTime"])
                * region_data["avgDailyIncomePopulation"]
                * region_data["avgDailyIncomeInUSD"]
                * data["timeToElapse"]
                * 7
            )
        )
        severeImpact["dollarsInFlight"] = float_rep(
            math.ceil(
                float(severeImpact["infectionsByRequestedTime"])
                * region_data["avgDailyIncomePopulation"]
                * region_data["avgDailyIncomeInUSD"]
                * data["timeToElapse"]
                * 7
            )
        )

    if data["periodType"].lower() == "months":
        impact["dollarsInFlight"] = float_rep(
            math.ceil(
                float(impact["infectionsByRequestedTime"])
                * region_data["avgDailyIncomePopulation"]
                * region_data["avgDailyIncomeInUSD"]
                * data["timeToElapse"]
                * 30
            )
        )
        severeImpact["dollarsInFlight"] = float_rep(
            math.ceil(
                float(severeImpact["infectionsByRequestedTime"])
                * region_data["avgDailyIncomePopulation"]
                * region_data["avgDailyIncomeInUSD"]
                * data["timeToElapse"]
                * 30
            )
        )

    results["data"] = data
    results["impact"] = impact
    results["severeImpact"] = severeImpact

    return results
