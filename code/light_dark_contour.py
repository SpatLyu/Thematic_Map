# -*- coding:utf-8 -*-
import os
import sys
import arcpy
from arcpy.sa import *
arcpy.env.overwriteOutput = True

def light_black_contour(inDEM, contourWidth, outFC, baseContour, zFactor, altitude, azimuth, lowversion):
    try:
	outPath = os.path.dirname(outFC)
        arcpy.env.workspace = outPath
        altitude = altitude
        azimuth = azimuth
        outHillshade = Hillshade(inDEM, azimuth, altitude, "NO_SHADOWS", zFactor)
        hillshadeCalc = (ACos(Float(outHillshade) / 255)) * 57.2958
        remapRange = RemapRange([[5.0758605003356934, 9.6565171082814523,1], [9.6565171082814523, 14.237173716227211,2],
                                [14.237173716227211, 18.81783032417297,3], [18.81783032417297, 23.398486932118729,4],
                                [23.398486932118729, 27.979143540064488,5], [27.979143540064488, 32.559800148010247,6],
                                [32.559800148010247, 37.140456755956009,7], [37.140456755956009, 41.721113363901772,8],
                                [41.721113363901772, 46.301769971847534,9], [46.301769971847534, 50.882426579793297,10],
                                [50.882426579793297, 55.463083187739059,11], [55.463083187739059, 60.043739795684822,12],
                                [60.043739795684822, 64.624396403630584,13], [64.624396403630584, 69.205053011576339,14],
                                [69.205053011576339, 73.785709619522095,15], [73.785709619522095, 78.36636622746785,16],
                                [78.36636622746785, 82.947022835413605,17], [82.947022835413605, 87.527679443359375,18]])
        outReclass = Reclassify(hillshadeCalc, "Value", remapRange)
        arcpy.RasterToPolygon_conversion(outReclass, "in_memory/reclassPoly", "SIMPLIFY", "VALUE")
        Contour(inDEM, os.path.join(outPath, "outContours"), contourWidth, baseContour, zFactor)
        inFeatures = [os.path.join(outPath, "outContours"), "in_memory/reclassPoly"]
        arcpy.Intersect_analysis(inFeatures, outFC)   
    except arcpy.ExecuteError as e:
        arcpy.AddError(arcpy.GetMessages(2))

def modify_mxd(lowversion):
    mxd = arcpy.mapping.MapDocument("CURRENT")
    df = mxd.activeDataFrame
    lyr_contours = arcpy.mapping.Layer(arcpy.GetParameterAsText(2))
    layer_name = os.path.basename(arcpy.GetParameterAsText(2))
    layer_dem = arcpy.MakeRasterLayer_management(arcpy.GetParameterAsText(0), "layer_dem")
    lyr1 = os.path.join(dir_lyr, "Illuminated_Contour.lyr")
    if lowversion == "true":
        lyr2 = os.path.join(dir_lyr, "Illuminated Contours101.lyr")
    else:
        lyr2 = os.path.join(dir_lyr, "Illuminated Contours1082.lyr")
    lyr3 = os.path.join(dir_lyr, "IllumContou_dem.lyr")
    arcpy.ApplySymbologyFromLayer_management(layer_dem, lyr3)
    groupLayer = arcpy.mapping.Layer(lyr1)
    arcpy.mapping.AddLayer(df, groupLayer, "TOP")
    groupLayer = arcpy.mapping.ListLayers(mxd, "Illuminated_Contour", df)[0]
    arcpy.mapping.AddLayerToGroup(df, groupLayer, lyr_contours, "BOTTOM")
    arcpy.mapping.AddLayerToGroup(df, groupLayer, layer_dem.getOutput(0), "BOTTOM")
    layer_c2 = arcpy.mapping.ListLayers(mxd, layer_name, df)[0]
    lyr2 = arcpy.mapping.Layer(lyr2)
    arcpy.mapping.UpdateLayer(df, layer_c2, lyr2)

toolbox = os.path.abspath(sys.argv[0])
tool_dir = os.path.abspath(os.path.dirname(toolbox))
dir_lyr = os.path.join(tool_dir, "lyr")
args = tuple(arcpy.GetParameterAsText(i) for i in range(arcpy.GetArgumentCount()))
light_black_contour(*args)
modify_mxd(arcpy.GetParameterAsText(7))
