import pickle

@custom
def load_model(*args, **kwargs):
    with open('model.bin', 'rb') as f:
        dv, model = pickle.load(f)
        print(dv)
        print(model)
    # return dv, model
    return (dv, model)


