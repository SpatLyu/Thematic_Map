# -*- coding:utf-8 -*-
import arcpy

arcpy.env.overwriteOutput = True
lyr_name = arcpy.GetParameterAsText(0)
input_distance = arcpy.GetParameterAsText(1)
output_raster = arcpy.GetParameterAsText(2)
arcpy.env.extent = lyr_name
arcpy.env.mask = lyr_name
arcpy.env.addOutputsToMap = True

def emboss(layer,buffer_distance,out_raster):
	arcpy.Buffer_analysis(layer, "in_memory/buffer_layer", buffer_distance, "FULL", "ROUND", "NONE", "", "PLANAR")
	arcpy.gp.EucDistance_sa("in_memory/buffer_layer", "in_memory/euc_distance")
	arcpy.Clip_management("in_memory/euc_distance", "", "in_memory/clip_raster", layer, "", True, False)
	arcpy.gp.HillShade_sa("in_memory/clip_raster", out_raster, "315", "45", "NO_SHADOWS", "1")

emboss(lyr_name, input_distance, output_raster)
arcpy.RefreshActiveView()
arcpy.RefreshTOC()
