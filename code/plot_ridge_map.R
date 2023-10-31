# setwd('./dailywork/Thematic_Map')
library(sf)
library(terra)
library(ggridges)
library(tidyverse)

rast('./data/elev.tif') |> 
  project(crs('epsg:32626')) |> 
  as.data.frame(xy=TRUE, na.rm=TRUE) |> 
  as_tibble() |> 
  mutate(class = cut_number(y, n = 3)) -> dem_df

ggplot() +
  geom_ridgeline(
    data = dem_df, aes(
      x = x, y = y,
      group = y,
      height = elevation,
      color = class
    ),
    scale = 25,
    fill = "black",
    size = .5,
    show.legend = FALSE
  ) +
  theme_void() +
  theme(plot.background = element_rect(fill = "grey20")) +
  scale_color_manual(values = alpha(
    c(
      "#007A33",
      "white",
      "#007A33"
    ),
    .95
  ))