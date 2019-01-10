import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.dates import DateFormatter
import dateutil
import pandas

def canvas_from_data(df, local_tz='US/Pacific'):
    local_zone = dateutil.tz.gettz(local_tz)
    name = df['Description'][0].strip()
    fig=Figure()
    ax=fig.add_subplot(111)
    x = df['TimeUpdated']
    y = df['CurrentTime']
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M', tz=local_zone))
    ax.set_title(name)
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    return canvas