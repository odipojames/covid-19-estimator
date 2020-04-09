import math

def estimator(data):
    results = {}
    impact = {}
    severeImpact = {}
    impact["currentlyInfected"] = data["reportedCases"] * 10
    severeImpact["currentlyInfected"] = data["reportedCases"] * 50

    if data["periodType"].lower() == "days":
        impact["infectionsByRequestedTime"] = math.ceil(
            impact["currentlyInfected"] * (2**(data["timeToElapse"]) / 3))
        severeImpact["infectionsByRequestedTime"] = math.ceil(
            impact["currentlyInfected"] * (2**(data["timeToElapse"]) / 3))

    if data["periodType"].lower() == "weeks":
        impact["infectionsByRequestedTime"] = math.ceil(
            impact["currentlyInfected"] * (2**(data["timeToElapse"] * 7) / 3))
        severeImpact["infectionsByRequestedTime"] = math.ceil(
            impact["currentlyInfected"] * (2**(data["timeToElapse"] * 7) / 3))

    if data["periodType"].lower() == "months":
        impact["infectionsByRequestedTime"] = math.ceil(
            impact["currentlyInfected"] * (2**(data["timeToElapse"] * 30) / 3))
        severeImpact["infectionsByRequestedTime"] = math.ceil(
            impact["currentlyInfected"] * (2**(data["timeToElapse"] * 30) / 3))
    impact["severeCasesByRequestedTime"] = impact["infectionsByRequestedTime"] * 0.15
    severeImpact["severeCasesByRequestedTime"] = severeImpact["infectionsByRequestedTime"] * 0.15
    impact["hospitalBedsByRequestedTime"] - \
        (data["totalHosiptalBeds"] * 0.35 -
         impact["severeCasesByRequestedTime"])
    severeImpact["hospitalBedsByRequestedTime"] - \
        (data["totalHosiptalBeds"] * 0.35 -
         severeImpact["severeCasesByRequestedTime"])
    impact["casesForICUByRequestedTime"] = impact["infectionsByRequestedTime"] * 0.5
    severeImpact["casesForICUByRequestedTime"] = severeImpact["infectionsByRequestedTime"] * 0.5

    impact["casesForVentilatorsByRequestedTime"] = impact["infectionsByRequestedTime"] * 0.2
    severeImpact["casesForVentilatorsByRequestedTime"] = severeImpact["infectionsByRequestedTime"] * 0.2

    region_data = data.pop("region")
    if data["periodType"].lower() == "days":
        impact["dollarsInFlight"] = (impact["infectionsByRequestedTime"] * region_data["avgDailyIncomePopulation"]
                                     ) * region_data["avgDailyIncomeInUSD"] * data["timeToElapse"]
        severeImpact["dollarsInFlight"] = (severeImpact["infectionsByRequestedTime"] *
                                           region_data["avgDailyIncomePopulation"]) * region_data["avgDailyIncomeInUSD"] * data["timeToElapse"]
    if data["periodType"].lower() == "weeks":
        impact["dollarsInFlight"] = (impact["infectionsByRequestedTime"] * region_data["avgDailyIncomePopulation"]
                                     ) * region_data["avgDailyIncomeInUSD"] * data["timeToElapse"] * 7
        severeImpact["dollarsInFlight"] = (severeImpact["infectionsByRequestedTime"] *
                                           region_data["avgDailyIncomePopulation"]) * region_data["avgDailyIncomeInUSD"] * data["timeToElapse"] * 7

    if data["periodType"].lower() == "months":
        impact["dollarsInFlight"] = (impact["infectionsByRequestedTime"] * region_data["avgDailyIncomePopulation"]
                                     ) * region_data["avgDailyIncomeInUSD"] * data["timeToElapse"] * 30
        severeImpact["dollarsInFlight"] = (severeImpact["infectionsByRequestedTime"] *
                                           region_data["avgDailyIncomePopulation"]) * region_data["avgDailyIncomeInUSD"] * data["timeToElapse"] * 30

    results["data"] = data
    results["impact"] = impact
    results["severeImpact"] = severeImpact

    return results
