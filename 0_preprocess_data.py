import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
import yaml


def make_eda(df):
    first_words = sorted(df['name'].str.split(' ', expand=True)[0].unique())
    print(first_words)


def filter_makes(df, config_yml):
    df['make'] = df['name'].str.split(' ', expand=True)[0]
    df = df.loc[df['make'].isin(config_yml['keep_makes'])]
    return df


if __name__ == "__main__":
    car_dat = pd.read_csv("data/Car details v3.csv")
    print(car_dat.columns)
    make_eda(car_dat)

    # apply config filtering
    with open("config/config.yaml") as ff:
        config = yaml.safe_load(ff)
    car_dat = filter_makes(car_dat, config)
    car_dat.to_csv("data/0_processed_car_dat.csv", index=False)

    # prepare groupbys
    rename_dict = {0: 'registrations'}
    dat = {}
    dat['yr_totals'] = car_dat.groupby('year').size().reset_index().rename(columns=rename_dict)
    dat['yr_make_totals'] = car_dat.groupby(['year', 'make']).size().reset_index().rename(columns=rename_dict)
    dat['yr_make_totals_cumsum'] = (car_dat.pivot_table(index='year', columns='make', aggfunc='size').fillna(0)
                                    .cumsum(axis=1).stack().reset_index().rename(columns=rename_dict))
    print('here')

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=dat['yr_totals']['year'], y=dat['yr_totals']['registrations'],
                   mode='lines',
                   name="Total Registrations",
                   line=dict(color='black', width=2))
    )
    # Add cumulative totals
    tmp = dat['yr_make_totals_cumsum'].set_index(['year', 'make']).unstack(level=-1)
    tmp.columns = [xx[1] for xx in tmp.columns]
    for col in tmp.columns:
        fig.add_trace(
            go.Scatter(x=tmp.index.values, y=tmp[col].values,
                       mode='lines',
                       name=col,
                       opacity=.5)
        )
    fig.update_layout(template='plotly_white')
    fig.write_image("figs/POC_plotly_figure.png")
    # plot(fig)




