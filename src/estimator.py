import math



def estimator(data):
    results = {}
    impact = {}
    severeImpact = {}
    impact["currentlyInfected"] = float(data["reportedCases"] * 10)
    severeImpact["currentlyInfected"] = float(data["reportedCases"] * 50)

    if data["periodType"].lower() == "days":

        impact["infectionsByRequestedTime"] = float(math.ceil(
            float(impact["currentlyInfected"]) * 2 ** (data["timeToElapse"] / 3)))
        severeImpact["infectionsByRequestedTime"] = float(math.ceil(
            float(impact["currentlyInfected"]) * 2**(data["timeToElapse"] / 3)))

    if data["periodType"].lower() == "weeks":
        impact["infectionsByRequestedTime"] = float(math.ceil(
            float(impact["currentlyInfected"]) * 2**(data["timeToElapse"] * 7 / 3)))
        severeImpact["infectionsByRequestedTime"] = float(math.ceil(
            float(impact["currentlyInfected"]) * 2**(data["timeToElapse"] * 7 / 3)))

    if data["periodType"].lower() == "months":
        impact["infectionsByRequestedTime"] = float(math.ceil(
            float(impact["currentlyInfected"]) *
                  2**(data["timeToElapse"] * 30 / 3)))

        severeImpact["infectionsByRequestedTime"] = float(math.ceil(
            float(severeImpact["currentlyInfected"]) *
                  2**(data["timeToElapse"] * 30 / 3)))

    results["data"]=data
    results["impact"]=impact
    results["severeImpact"]=severeImpact

    return results
