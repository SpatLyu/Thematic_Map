library(rayshader)
library(terra)
library(tidyverse)

rast('./data/elev.tif') |> 
  as.data.frame(xy=TRUE,na.rm=TRUE) |> 
  as_tibble() -> elev

ggplot(data = elev) +
  geom_tile(aes(x = x, y = y, fill = elevation)) +
  geom_contour(aes(x = x, y = y, z = elevation), color = "black") +
  scale_x_continuous("Long", expand = c(0, 0)) +
  scale_y_continuous("Lat", expand = c(0, 0)) +
  scale_fill_gradientn("Elevation", colours = terrain.colors(10)) +
  coord_fixed() -> ggtopo

plot_gg(ggtopo, width = 7, height = 4, raytrace = FALSE, preview = TRUE)
plot_gg(ggtopo, multicore = TRUE, raytrace = TRUE, width = 7, height = 4, 
        scale = 300, windowsize = c(1400, 866), zoom = 0.6, phi = 30, theta = 30)