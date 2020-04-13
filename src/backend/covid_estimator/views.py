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
import math
import time
import json

# Create your views here.



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
        impact["currentlyInfected"] = float(response["reported_cases"] * 10)
        severeImpact["currentlyInfected"] = float(response["reported_cases"] * 50)
        # infectionsByRequestedTime
        if response["period_type"].lower() == "days":
            impact["infectionsByRequestedTime"] = math.ceil(
                float(
                    float(impact["currentlyInfected"])
                    * 2 ** (response["time_to_elapse"] / 3)
                )
            )
            severeImpact["infectionsByRequestedTime"] = math.ceil(
                float(
                    float(severeImpact["currentlyInfected"])
                    * 2 ** (response["time_to_elapse"] / 3)
                )
            )
        if response["period_type"].lower() == "weeks":
            impact["infectionsByRequestedTime"] = math.ceil(
                float(
                    float(impact["currentlyInfected"])
                    * 2 ** (response["time_to_elapse"] * 7 / 3)
                )
            )
            severeImpact["infectionsByRequestedTime"] = math.ceil(
                float(
                    float(severeImpact["currentlyInfected"])
                    * 2 ** (response["time_to_elapse"] * 7 / 3)
                )
            )
        if response["period_type"].lower() == "months":
            impact["infectionsByRequestedTime"] = math.ceil(
                float(
                    float(impact["currentlyInfected"])
                    * 2 ** (response["time_to_elapse"] * 30 / 3)
                )
            )
            severeImpact["infectionsByRequestedTime"] = math.ceil(
                float(
                    float(severeImpact["currentlyInfected"])
                    * 2 ** (response["time_to_elapse"] * 30 / 3)
                )
            )
        # severeCasesByRequestedTime
        impact["severeCasesByRequestedTime"] = math.ceil(
            float(float(impact["infectionsByRequestedTime"]) * 0.15)
        )

        severeImpact["severeCasesByRequestedTime"] = math.ceil(
            float(float(severeImpact["infectionsByRequestedTime"]) * 0.15)
        )

        # hospitalBedsByRequestedTime
        impact["hospitalBedsByRequestedTime"] = math.ceil(
            float(
                response["total_hosiptal_beds"] * 0.35
                - float(impact["severeCasesByRequestedTime"])
            )
        )
        severeImpact["hospitalBedsByRequestedTime"] = math.ceil(
            float(
                response["total_hosiptal_beds"] * 0.35
                - float(severeImpact["severeCasesByRequestedTime"])
            )
        )
        # casesForICUByRequestedTime
        impact["casesForICUByRequestedTime"] = math.ceil(
            float(float(impact["infectionsByRequestedTime"]) * 0.05)
        )

        severeImpact["casesForICUByRequestedTime"] = math.ceil(
            float(float(severeImpact["infectionsByRequestedTime"]) * 0.05)
        )

        # casesForVentilatorsByRequestedTime
        impact["casesForICUByRequestedTime"] = math.ceil(
            float(float(impact["infectionsByRequestedTime"]) * 0.02)
        )
        severeImpact["casesForICUByRequestedTime"] = math.ceil(
            float(float(severeImpact["infectionsByRequestedTime"]) * 0.02)
        )
        # dollarsInFlight
        region_data = response.pop("region")
        if response["period_type"].lower() == "days":
            impact["dollarsInFlight"] = math.ceil(
                float(
                    float(impact["infectionsByRequestedTime"])
                    * region_data["avg_daily_income_population"]
                    * region_data["avg_daily_income"]
                    * response["time_to_elapse"]
                )
            )

            severeImpact["dollarsInFlight"] = math.ceil(
                float(
                    float(severeImpact["infectionsByRequestedTime"])
                    * region_data["avg_daily_income_population"]
                    * region_data["avg_daily_income"]
                    * response["time_to_elapse"]
                )
            )

        if response["period_type"].lower() == "weeks":
            impact["dollarsInFlight"] = math.ceil(
                float(
                    float(impact["infectionsByRequestedTime"])
                    * region_data["avg_daily_income_population"]
                    * region_data["avg_daily_income"]
                    * response["time_to_elapse"]
                    * 7
                )
            )
            severeImpact["dollarsInFlight"] = math.ceil(
                float(
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
    # renderer_classes = (Plamath.ceilextRenderer,)

    def get_queryset(self):
        return Log.objects.all().order_by("-id")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
