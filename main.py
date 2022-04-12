from pandas_datareader import data
import datetime
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from bokeh.resources import CDN

end = datetime.date.today()
start = end - datetime.timedelta(days=60)

df=data.DataReader(name="GOOG", data_source="yahoo", start=start, end=end)               


date_increase = df.index[df.Close > df.Open]
date_decrease = df.index[df.Close < df.Open]

def inc_dec(c, o):
    if c > o:
        value = "Increase"
    elif c < o:
        value = "Decrease"
    else: 
        value = "Equal"
    return value

df["Status"] = [inc_dec(c, o) for c, o in zip(df.Close, df.Open)]
df["Middle"]=(df.Open+df.Close)/2
df["height"]=abs(df.Close-df.Open)

p = figure(x_axis_type='datetime', width=1000, height=300, sizing_mode="scale_width")
p.title="CandleStick Chart"
p.grid.grid_line_alpha=0.3

hours_12 = 12*60*60*1000

p.segment(df.index, df.High, df.index, df.Low, color="black")

p.rect(df.index[df.Status=="Increase"], df.Middle[df.Status=="Increase"], 
       hours_12, df.height[df.Status=="Increase"], fill_color="#98EF5A", line_color = "Black")

p.rect(df.index[df.Status=="Decrease"], df.Middle[df.Status=="Decrease"], 
       hours_12, df.height[df.Status=="Decrease"], fill_color="#E74C3C", line_color = "Black")

script1, div1 = components(p)
cdn_js = CDN.js_files
cdn_css = CDN.css_files
