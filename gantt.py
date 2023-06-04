import time
import plotly as py
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def read_result():
    df = pd.read_csv('output.csv', dtype='str')
    df = df.fillna('')
    return df

def assign_color4jobs(df):
    machineMap = dict()
    job_set = set()
    i = 1
    for (columnName, columnData) in df.iteritems():
        machineMap[columnName] = i
        job_set = job_set.union(columnData.values)
        i += 1
    job_set.discard('')

    jobMap = dict()
    for job in job_set:
        jobMap[job] = 'rgb({0})'.format(str(list(np.random.choice(range(256), size=3)))[1:-1])
    return jobMap, machineMap

def create_draw_defination():
    df = []
    for index in range(len(n_job_id)):
        operation = {}
        # 机器，纵坐标
        operation['Task'] = n_bay_text.__getitem__(index)
        operation['Start'] = start_time.__add__(n_start_time.__getitem__(index) * millis_seconds_per_hour)
        operation['Finish'] = start_time.__add__(
            (n_start_time.__getitem__(index) + n_duration_time.__getitem__(index)) * millis_seconds_per_hour)
        # 工件，
        # job_num = op.index(n_job_id.__getitem__(index)) + 1
        operation['Resource'] = n_job_id.__getitem__(index)
        # operation['Complete'] = n_bay_start.__getitem__(index)+1
        df.append(operation)
    df.sort(key=lambda x: x["Task"], reverse=True)
    print(df)
    return df


def draw_prepare():
    df = create_draw_defination()
    return ff.create_gantt(df, colors=colors, index_col='Resource',
                           title='Gantt Plot`', show_colorbar=True,
                           group_tasks=True, data=n_duration_time,
                           showgrid_x=True, showgrid_y=True)


def add_annotations(fig):
    y_pos = 0
    for index in range(len(n_job_id)):
        # 机器，纵坐标
        y_pos = n_bay_start.__getitem__(index)

        x_start = start_time.__add__(n_start_time.__getitem__(index) * millis_seconds_per_hour)
        x_end = start_time.__add__(
            (n_start_time.__getitem__(index) + n_duration_time.__getitem__(index)) * millis_seconds_per_hour)
        x_pos = (x_end - x_start) / 2 + x_start

        # 工件，
        # job_num = op.index(n_job_id.__getitem__(index)) + 1
        # text = 'J(' + str(job_num) + "," + str(get_op_num(job_num)) + ")=" + str(n_duration_time.__getitem__(index))
        # text = 'T' + str(job_num) + str(get_op_num(job_num))
        text = ""
        text_font = dict(size=14, color='black')
        fig['layout']['annotations'] += tuple(
            [dict(x=x_pos, y=y_pos, text=text, textangle=-30, showarrow=False, font=text_font)])


def draw_gantt():
    fig = draw_prepare()
    add_annotations(fig)
    py.offline.plot(fig, filename='gantt.html')


if __name__ == '__main__':

    out_df = read_result()
    jobMap, machineMap = assign_color4jobs(out_df)

    millis_seconds_per_hour = 1000 * 60 * 60
    start_time = time.time() * 1000

    n_start_time = []
    n_end_time = []
    n_duration_time = []
    n_bay_start = []
    n_bay_text = []
    n_job_id = []
    colors = []

    for machine in out_df.columns:
        timeline = dict(out_df[machine])

        for hour, job in timeline.items():
            if job == '':
                continue
            if job == timeline.get(hour-1, None):
                continue

            timeBegin = hour

            i = 0
            curr_t = hour
            while timeline.get(curr_t, None) == job:
                curr_t += 1
                i += 1

            timeEnd = curr_t
            duration = i
            n_start_time.append(timeBegin)
            n_end_time.append(timeEnd)
            n_duration_time.append(duration)
            n_bay_start.append(machineMap[machine])
            n_bay_text.append(machine)
            n_job_id.append('Job'+job)
            color = jobMap[job]
            colors.append(color)
    draw_gantt()
