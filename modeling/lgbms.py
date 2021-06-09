import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from score import nmae_10, sola_nmae

def lgbm(data, x, y, params):
    X = data[x]
    y = data[y]

    train_x, val_x, train_y, val_y = train_test_split(X, y, test_size=0.15, random_state=1217)

    train_x = train_x.to_numpy()
    train_y = train_y.to_numpy()

    val_x = val_x.to_numpy()
    val_y = val_y.to_numpy()

    train_dataset = lgb.Dataset(train_x, train_y)
    val_dataset = lgb.Dataset(val_x, val_y)

    model = lgb.train(params, train_dataset, 10000, val_dataset, feval=nmae_10, verbose_eval=500,
                      early_stopping_rounds=100)
    pred = model.predict(val_x)

    pred_pd = pd.DataFrame(pred)
    pred = pred_pd[0].map(lambda x: 0 if x < 10 else x).to_numpy()

    # plt.figure(figsize=(20, 5))
    # plt.plot(val_y, label='true')
    # plt.plot(pred, label='pred')
    # plt.legend()
    # plt.show()

    nmae = sola_nmae(val_y, pred)
    rmse = np.sqrt(mean_squared_error(val_y, pred))

    print('CV Score : ', nmae)
    print("rmse: ", rmse)

    return (model, nmae, pred, 0)


def lgbm365(data, x, y, params):
    train = data.iloc[:-24 * 365]
    val = data.iloc[-24 * 365:]

    train_x = train[x].to_numpy()
    train_y = train[y].to_numpy()

    val_x = val[x].to_numpy()
    val_y = val[y].to_numpy()

    train_dataset = lgb.Dataset(train_x, train_y)
    val_dataset = lgb.Dataset(val_x, val_y)

    model = lgb.train(params, train_dataset, 1000, val_dataset, feval=nmae_10, verbose_eval=500,
                      early_stopping_rounds=100)
    pred = model.predict(val_x)

    pred_pd = pd.DataFrame(pred)
    pred = pred_pd[0].map(lambda x: 0 if x < 5 else x).to_numpy()

    # plt.figure(figsize=(20, 5))
    # plt.plot(val_y, label='true')
    # plt.plot(pred, label='pred')
    # plt.legend()
    # plt.show()

    nmae = sola_nmae(val_y, pred)
    rmse = np.sqrt(mean_squared_error(val_y, pred))

    print('CV Score : ', nmae)
    print("rmse: ", rmse)

    #    fig, ax = plt.subplots(figsize=(10, 12))
    #    plot_importance(model, ax=ax)

    fcst = val.copy()
    fcst["fcst"] = pred

    return (model, nmae, pred, fcst)
