from models.simple_ann import SimpleANN
import pandas as pd
import numpy as np
import datatools.evaluation as eval
import datatools.preprocessing as prep
import matplotlib.pyplot as plt

if __name__ == '__main__':
    config={
        'model': {
            'path': ""
        },
        'data': {
            'path': "",
            'delimiter': ",",
            'decimal': "."
        }

    }

    steps=[4, 8, 12, 16, 20]
    data=pd.read_csv(
        config['data']['path'],
        delimiter=config['data']['delimiter'],
        decimal=config['data']['decimal'],
        header=0
    ).to_numpy()
    X, y = prep.window_time_series(data[:,1:8], 32, steps)

    model=SimpleANN()
    model.load(config['model']['path'])

    eval.evaluate_mae(model, X, y, steps)

    plt.hist(eval.evaluate_time(model, X), bins=100)
    plt.title("Calculation Time Density Distribution")
    plt.xlabel("Time / s")
    plt.ylabel("Frequency")
    plt.show()