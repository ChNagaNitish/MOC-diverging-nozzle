set terminal postscript color enhanced font "Times-Roman,30.0"
set output "Nozzle_Contour.eps"
set size 1,1
#####################################
set encoding utf8

#set   autoscale                        # scale axes automatically
unset log                              # remove any log-scaling
unset label                            # remove any previous labels
#set xr [-0.5:15]
#set yr [-0.5:5]
set xtic auto                          # set xtics automatically
set ytic auto                          # set ytics automatically
#set xtics add ("140" 140)
#set mxtics 10
#set mytics 10
#set grid
#set title "M_{entry} = 1.0, M_{exit} = 2.5"

#set label "Yield Point" at 0.003,260
#set arrow from 0.0028,250 to 0.003,280
set datafile separator " "
#stats 'mach.dat'
#max_col = STATS_columns
unset key
unset xtics
unset ytics
unset border
set style line 12 lc rgb 'black' lt 1 lw 0.5
set style line 13 lc rgb 'black' lt 1 dt 1 lw 0.01
set grid xtics ytics mxtics mytics ls 12, ls 13
unset grid
#plot "data_1.dat" using 1:2 title "Nozzle" with l lw 6 lc rgb 'red'
plot "nozzle_contour.dat" using 1:2 title "Nozzle" with l lw 4 lc rgb 'black'