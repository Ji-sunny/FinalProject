import numpy as np

def nmae_10(y_pred, dataset, capacity):
    y_true = dataset.get_label()

    absolute_error = abs(y_true - y_pred)
    absolute_error /= capacity

    target_idx = np.where(y_true >= capacity * 0.1)

    nmae = 100 * absolute_error[target_idx].mean()

    return 'score', nmae, False


def sola_nmae(answer, pred, capacity):
    absolute_error = np.abs(answer - pred)

    absolute_error /= capacity

    target_idx = np.where(answer >= capacity * 0.1)

    nmae = 100 * absolute_error[target_idx].mean()

    return nmae