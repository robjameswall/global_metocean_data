# Fetch the latest ww3 forecast

library(rNOMADS)

model.list <- NOMADSRealTimeList("grib")
wave.idx <- which(model.list$name == "Wave")
wave.url <- model.list$url[wave.idx]
wave.latest.url <- CrawlModels(url = wave.url, depth = 2)
wave.model.info <- ParseModelPage(wave.latest.url[1])

# Download all ww3 (including multi) or just standard forecast (FALSE)
dl_all <- TRUE

if(dl_all){
  nww3_f <- wave.model.info$pred[grepl("nww3", wave.model.info$pred)]
} else {
  nww3_f <- wave.model.info$pred[grepl("nww3", wave.model.info$pred) & !grepl("multi", wave.model.info$pred)]
}


wave.forecast <- GribGrab(model.url = wave.latest.url[1],
                          preds = nww3_f,
                          levels = wave.model.info$levels,
                          variables = wave.model.info$variables,
                          tidy = TRUE,
                          local.dir = "data/")

