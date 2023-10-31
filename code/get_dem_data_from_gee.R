library(rgee)
ee_Initialize(drive=T,gcs=T)

library(sf)
library(terra)

roi = ee$Geometry$BBox(-156.250305,18.890695,-154.714966,20.275080)

elev = ee$Image("USGS/SRTMGL1_003")$
  select('elevation')$
  clip(roi)$
  rename('elevation')

ee_as_rast(
  image = elev,
  region = roi,
  scale = 1000,
  dsn = './data/elev.tif',
  via = "drive"
)
