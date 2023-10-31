# -*- coding: utf-8 -*-
import arcpy
from arcpy.sa import *
arcpy.env.overwriteOutput = True

input_dem = arcpy.GetParameterAsText(0)
output_ridge = arcpy.GetParameterAsText(1)
cellsize = arcpy.GetParameterAsText(2)

def calcul_ridge(inDEM,outRidge,cellSize):
    direction_ns = FocalStatistics(inDEM, NbrRectangle(cellSize, 1, "CELL"), 'MAXIMUM')
    direction_ew = FocalStatistics(inDEM, NbrRectangle(1, cellSize, "CELL"), 'MAXIMUM')
    ridge = (Raster(inDEM) == direction_ns) | (Raster(inDEM) == direction_ew)
    SetNull(ridge,ridge,"Value = 0").save(outRidge)
    
calcul_ridge(input_dem,output_ridge,cellsize)