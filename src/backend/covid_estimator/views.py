# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from .serializers import RegionDataSerializer, LogSerializer
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
from .models import RegionData, Log
from .renderers import PlainTextRenderer
import math
import time
import json

# Create your views here.


def float_rep(x):
    """rep float to human readablbe"""
    num = "%1.9f" % x
    return num


class ListCreateRegionDataAPIView(generics.CreateAPIView):
    """posting region data"""

    serializer_class = RegionDataSerializer
    renderer_classes = (JSONRenderer, XMLRenderer)

    def get_queryset(self):
        return RegionData.objects.all().order_by("-id")

    def post(self, request, format=None):
        start_time = time.time()
        data = request.data.copy()
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = serializer.data
        impact = {}
        severeImpact = {}
        results = {}
        # currently infected
        impact["currentlyInfected"] = float_rep(response["reported_cases"] * 10)
        severeImpact["currentlyInfected"] = float_rep(response["reported_cases"] * 50)
        # infectionsByRequestedTime
        if response["period_type"].lower() == "days":
            impact["infectionsByRequestedTime"] = float_rep(
                math.ceil(
                    float(impact["currentlyInfected"])
                    * 2 ** (response["time_to_elapse"] / 3)
                )
            )
            severeImpact["infectionsByRequestedTime"] = float_rep(
                math.ceil(
                    float(severeImpact["currentlyInfected"])
                    * 2 ** (response["time_to_elapse"] / 3)
                )
            )
        if response["period_type"].lower() == "weeks":
            impact["infectionsByRequestedTime"] = float_rep(
                math.ceil(
                    float(impact["currentlyInfected"])
                    * 2 ** (response["time_to_elapse"] * 7 / 3)
                )
            )
            severeImpact["infectionsByRequestedTime"] = float_rep(
                math.ceil(
                    float(severeImpact["currentlyInfected"])
                    * 2 ** (response["time_to_elapse"] * 7 / 3)
                )
            )
        if response["period_type"].lower() == "months":
            impact["infectionsByRequestedTime"] = float_rep(
                math.ceil(
                    float(impact["currentlyInfected"])
                    * 2 ** (response["time_to_elapse"] * 30 / 3)
                )
            )
            severeImpact["infectionsByRequestedTime"] = float_rep(
                math.ceil(
                    float(severeImpact["currentlyInfected"])
                    * 2 ** (response["time_to_elapse"] * 30 / 3)
                )
            )
        # severeCasesByRequestedTime
        impact["severeCasesByRequestedTime"] = float_rep(
            math.ceil(float(impact["infectionsByRequestedTime"]) * 0.15)
        )

        severeImpact["severeCasesByRequestedTime"] = float_rep(
            math.ceil(float(severeImpact["infectionsByRequestedTime"]) * 0.15)
        )

        # hospitalBedsByRequestedTime
        impact["hospitalBedsByRequestedTime"] = float_rep(
            math.ceil(
                response["total_hosiptal_beds"] * 0.35
                - float(impact["severeCasesByRequestedTime"])
            )
        )
        severeImpact["hospitalBedsByRequestedTime"] = float_rep(
            math.ceil(
                response["total_hosiptal_beds"] * 0.35
                - float(severeImpact["severeCasesByRequestedTime"])
            )
        )
        # casesForICUByRequestedTime
        impact["casesForICUByRequestedTime"] = float_rep(
            math.ceil(float(impact["infectionsByRequestedTime"]) * 0.05)
        )

        severeImpact["casesForICUByRequestedTime"] = float_rep(
            math.ceil(float(severeImpact["infectionsByRequestedTime"]) * 0.05)
        )

        # casesForVentilatorsByRequestedTime
        impact["casesForICUByRequestedTime"] = float_rep(
            math.ceil(float(impact["infectionsByRequestedTime"]) * 0.02)
        )
        severeImpact["casesForICUByRequestedTime"] = float_rep(
            math.ceil(float(severeImpact["infectionsByRequestedTime"]) * 0.02)
        )
        # dollarsInFlight
        region_data = response.pop("region")
        if response["period_type"].lower() == "days":
            impact["dollarsInFlight"] = float_rep(
                math.ceil(
                    float(impact["infectionsByRequestedTime"])
                    * region_data["avg_daily_income_population"]
                    * region_data["avg_daily_income"]
                    * response["time_to_elapse"]
                )
            )

            severeImpact["dollarsInFlight"] = float_rep(
                math.ceil(
                    float(severeImpact["infectionsByRequestedTime"])
                    * region_data["avg_daily_income_population"]
                    * region_data["avg_daily_income"]
                    * response["time_to_elapse"]
                )
            )

        if response["period_type"].lower() == "weeks":
            impact["dollarsInFlight"] = float_rep(
                math.ceil(
                    float(impact["infectionsByRequestedTime"])
                    * region_data["avg_daily_income_population"]
                    * region_data["avg_daily_income"]
                    * response["time_to_elapse"]
                    * 7
                )
            )
            severeImpact["dollarsInFlight"] = float_rep(
                math.ceil(
                    float(severeImpact["infectionsByRequestedTime"])
                    * region_data["avg_daily_income_population"]
                    * region_data["avg_daily_income"]
                    * response["time_to_elapse"]
                    * 7
                )
            )
        results["data"] = response
        results["impact"] = impact
        results["severeImpact"] = severeImpact
        # logs
        end_time = time.time()
        duration = end_time - start_time
        Log.objects.create(
            time_stamp=round(start_time, 4),
            path=request.path,
            duration=round(duration, 2),
        )
        return Response(results, status.HTTP_201_CREATED)


class ListLogAPIView(generics.ListAPIView):
    """listing logs"""

    serializer_class = LogSerializer
    # renderer_classes = (PlainTextRenderer,)

    def get_queryset(self):
        return Log.objects.all().order_by("-id")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
