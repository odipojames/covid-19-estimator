import math


def estimator(data):
    results = {}
    impact = {}
    severeImpact = {}
    impact["currentlyInfected"] = "%1.9f" %(data["reportedCases"] * 10)
    severeImpact["currentlyInfected"] = "%1.9f" %(data["reportedCases"] * 50)

    if data["periodType"].lower() == "days":
        impact["infectionsByRequestedTime"] ="%1.9f" % math.ceil(
            impact["currentlyInfected"] * float(2 ** (data["timeToElapse"]) / 3)
        )
        severeImpact["infectionsByRequestedTime"] = "%1.9f" %math.ceil(
            impact["currentlyInfected"] * (2 ** (data["timeToElapse"]) / 3)
        )

    if data["periodType"].lower() == "weeks":
        impact["infectionsByRequestedTime"] ="%1.9f" % math.ceil(
            impact["currentlyInfected"] * (2 ** (data["timeToElapse"] * 7) / 3)
        )
        severeImpact["infectionsByRequestedTime"] = "%1.9f" %math.ceil(
            impact["currentlyInfected"] * (2 ** (data["timeToElapse"] * 7) / 3)
        )

    if data["periodType"].lower() == "months":
        impact["infectionsByRequestedTime"] = "%1.9f" %math.ceil(
            impact["currentlyInfected"] *
            (2 ** (data["timeToElapse"] * 30) / 3)
        )
        severeImpact["infectionsByRequestedTime"] = "%1.9f" %math.ceil(
            impact["currentlyInfected"] *
            (2 ** (data["timeToElapse"] * 30) / 3)
        )

    impact["severeCasesByRequestedTime"] = "%1.9f" %math.ceil(
        impact["infectionsByRequestedTime"] * 0.15
    )
    severeImpact["severeCasesByRequestedTime"] = "%1.9f" %math.ceil(
        severeImpact["infectionsByRequestedTime"] * 0.15
    )

    impact["hospitalBedsByRequestedTime"]="%1.9f" %math.ceil(data["totalHospitalBeds"]*0.35-impact["severeCasesByRequestedTime"])

    severeImpact["hospitalBedsByRequestedTime"]="%1.9f" %math.ceil(data["totalHospitalBeds"]*0.35-severeImpact["severeCasesByRequestedTime"])

    impact["casesForICUByRequestedTime"] = "%1.9f" %math.ceil(impact["infectionsByRequestedTime"] * 0.5)
    severeImpact["casesForICUByRequestedTime"] = "%1.9f" %math.ceil(
        severeImpact["infectionsByRequestedTime"] * 0.5
    )

    impact["casesForVentilatorsByRequestedTime"] = "%1.9f" %math.ceil(
        impact["infectionsByRequestedTime"] * 0.2
    )
    severeImpact["casesForVentilatorsByRequestedTime"] = "%1.9f" %math.ceil(
        severeImpact["infectionsByRequestedTime"] * 0.2
    )

    region_data = data.pop("region")
    if data["periodType"].lower() == "days":
        impact["dollarsInFlight"] = "%1.9f" %(
            (
                impact["infectionsByRequestedTime"]
                * region_data["avgDailyIncomePopulation"]
            )
            * region_data["avgDailyIncomeInUSD"]
            * data["timeToElapse"]
        )
        severeImpact["dollarsInFlight"] = "%1.9f" %(
            (
                severeImpact["infectionsByRequestedTime"]
                * region_data["avgDailyIncomePopulation"]
            )
            * region_data["avgDailyIncomeInUSD"]
            * data["timeToElapse"]
        )
    if data["periodType"].lower() == "weeks":
        impact["dollarsInFlight"] = "%1.9f" %(
            (
                impact["infectionsByRequestedTime"]
                * region_data["avgDailyIncomePopulation"]
            )
            * region_data["avgDailyIncomeInUSD"]
            * data["timeToElapse"]
            * 7
        )
        severeImpact["dollarsInFlight"] = "%1.9f" %(
            (
                severeImpact["infectionsByRequestedTime"]
                * region_data["avgDailyIncomePopulation"]
            )
            * region_data["avgDailyIncomeInUSD"]
            * data["timeToElapse"]
            * 7
        )

    if data["periodType"].lower() == "months":
        impact["dollarsInFlight"] = "%1.9f" %(
            (
                impact["infectionsByRequestedTime"]
                * region_data["avgDailyIncomePopulation"]
            )
            * region_data["avgDailyIncomeInUSD"]
            * data["timeToElapse"]
            * 30
        )
        severeImpact["dollarsInFlight"] = "%1.9f" %(
            (
                severeImpact["infectionsByRequestedTime"]
                * region_data["avgDailyIncomePopulation"]
            )
            * region_data["avgDailyIncomeInUSD"]
            * data["timeToElapse"]
            * 30
        )

    results["data"] = data
    results["impact"] = impact
    results["severeImpact"] = severeImpact

    return results
