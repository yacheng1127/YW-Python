Modvsobs
======

Sphinx Website:

http://www.nefsc.noaa.gov/epd/ocean/MainPage/py/sphinx_modvsobs/_build/html/index.html

--'annualplot.py' reads in modeled data and observed data then plots annual average figure.

--'assimilation_separate.py' since assimilation began in 2008, this program separates whole data with year 2008 then plots obs-mod difference figure of before and after assimilation.  

--'befaftassplot.py' takes the data of 2008 as an example,plots observed, before assimilation and after assimilation lines to see the data development. 

--'befaftasstab.py' makes an output file to show the result of mean/max/min/std/rms values of obs-beforeassimilation and obs-afterassimilation. The output file name is "versus_aft_bef_ass.csv".

--"creat_diffplot.py"plots monthly temperature difference between obs-mod at 11 sites.Reads in "modvsobs.py"output file.

--'daplot.py' reads in "modvsobs.py" output file and then plots observed and modeled daily data figure.

--'distance_affect.py' creats a lineplot to show the assimilation influence change with distance. Also creats file named "distance_affect.csv" to record difference change of before and after assimilation.

--'distanceaffect_plot.py' reads in out put files of 'distance_affect.py' then plots distance affect on several sites.

--'endaplot.py' reads in "modvsobs.py" output file and NERACOOS temperature file then plots observed versus modeled data figure.

--'getsite.py' is the program employed to get the specified sites information.'site.csv' is its input file and 'ProcessedSite.csv'is output file

--'mcplot.py' reads in "modvsobs.py" output file and then plots observed and modeled monthly average data figure.

--'modvsobs.py' is the main program employed to get model and observed data and compares them then plots figure and generates output files.

--'modvsobsneracoos.py' gets the NERACOOS and observed data, compares them and generates output files.

--'scatterplot.py'can plot scotter figure which show the regression equation and different coefficients.

--'sitemap.py' is the program plots a map show the sites which we processed their data.'ProcessedSite.csv' is its input file.(getsite.py creat "ProcessedSite.csv")

--'surface_bottom_plot.py' plots lineplot to show the serface and bottom temperature difference with modeled data. reads in "modvsobs.py" output files.

--'totalcalculate.py'reads in "modvsobs.py" output file and calculate the difference mean/max/min/std/rms values at special sites."totalcalculate.csv"is its output file.

--'warmcold.py' is the program plot a map show the difference at sites which we processed.red represents obs-mod>=0, blue represents obs-mod<0, the bigger point is, the bigger difference is.reads in "totalcalculate.csv" and "site.csv",output file is "warmcold.csv" 



