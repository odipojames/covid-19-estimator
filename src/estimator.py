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

        impact["infectionsByRequestedTime"] = float_rep(int(
            float(impact["currentlyInfected"]) * 2 ** (data["timeToElapse"] / 3)))
        severeImpact["infectionsByRequestedTime"] = float_rep(int(
            float(impact["currentlyInfected"]) * 2**(data["timeToElapse"] / 3)))

    if data["periodType"].lower() == "weeks":
        impact["infectionsByRequestedTime"] = float_rep(int(
            float(impact["currentlyInfected"]) * 2**(data["timeToElapse"] * 7 / 3)))
        severeImpact["infectionsByRequestedTime"] = float_rep(int(
            float(impact["currentlyInfected"]) * 2**(data["timeToElapse"] * 7 / 3)))

    if data["periodType"].lower() == "months":
        impact["infectionsByRequestedTime"] = float_rep(int(
            float(impact["currentlyInfected"]) *
                  2**(data["timeToElapse"] * 30 / 3)))

        severeImpact["infectionsByRequestedTime"] = float_rep(int(
            float(severeImpact["currentlyInfected"]) *
                  2**(data["timeToElapse"] * 30 / 3)))

    results["data"]=data
    results["impact"]=impact
    results["severeImpact"]=severeImpact

    return results
