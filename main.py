""" Run cellular automata. """

import json
from cv2 import imread
from functools import partial
from process_images import load_config
from functools import reduce
from itertools import islice
from multiprocessing import Pool, Lock
from sklearn.metrics import mean_squared_error
from cellular_automata import CellularAutomata


def load_rules(rpath):
    """ Load rules from file. """

    arr = []
    match_list = {}
    with open(rpath, "r") as f:
        arr = json.load(f)
        for ruleset in arr:
            match_list[f'{ruleset[0]}'] = ruleset
    return match_list


def compare_rmse(im_compare, im_predict):
    """ Get RMSE of two images. """

    rmse = mean_squared_error(im_compare, im_predict)
    print(rmse)
    return rmse


def chunks(data, SIZE=10000):
    """ Split dict into chunks. """
    
    it = iter(data)
    for _ in range(0, len(data), SIZE):
        yield {k: data[k] for k in islice(it, SIZE)}


def get_best(val1, val2):
    """ Reducer. """

    if val1[0] > val2[0]:
        return val2
    else:
        return val1


def find_best(chunk, img_compare, img_noisy):
    """ Mapper. """
    
    print("Starting.")
    compare = np.copy(img_compare)
    field = np.copy(img_noisy)

    gens = 10

    best_err = [None, None]
    for r in chunk.keys():
        ca = CellularAutomata(field, {r: chunk[r][0]})
        for _ in range(gens):
            ca.evolve()

        rule_err = compare_rmse(compare, ca.field)

        if best_err[0] is None:
            best_err = [rule_err, r]
        elif best_err[0] > rule_err:
            best_err = [rule_err, r]

    print(f'Found best: {best_err}')
    return best_err


if __name__ == "__main__":
    rules = load_rules("rules.json")
    settings = load_config("settings.json")
    split_size = settings["split_size"]
    compare_path = settings["paths"]["samples"]["processed"]
    noisy_path = settings["paths"]["samples"]["noisy"]

    # Load as grayscale.
    fpath = "satellite_2.jpg"
    img = cv.imread(compare_path + fpath, cv.IMREAD_GRAYSCALE)
    noisy = cv.imread(noisy_path + fpath, cv.IMREAD_GRAYSCALE)

    best_rules = {}
    while len(best_rules) < 100:
        splits = list(chunks(rules, split_size))

        mapper = find_best
        reducer = get_best

        chunk_args = []

        for split in splits:
            #temp = []
            for key in split.keys():
                chunk_args.append(({key: split[key]}, img, noisy))
            # chunk_args.append(temp)

        with Pool(4) as pool:
            mapped = pool.starmap(mapper, chunk_args)

        best_rule = reduce(reducer, mapped)
        key = best_rule[1]

        # Temporary.
        temp = best_rules

        # Add rule to best rules.
        best_rules[key] = rules[key]
        # Remove from rules.
        rules.pop(key, None)

        i = 0
        if i != 0:
            for best in best_rules.keys():
                no_best = best_rules
                del no_best[best]

                ca = CellularAutomata(noisy, no_best)
                for _ in range(10):
                    ca.evolve()
                ca_rmse = compare_rmse(img, ca.field)
                ca_rmse = compare_rmse(img, ca.field)
            else:
                ca_rmse = best_rule[0]
